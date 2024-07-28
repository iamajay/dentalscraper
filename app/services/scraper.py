import os
import json
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List
from sqlalchemy.orm import Session
from app.models import Product, NotificationType, NotificationConfigDB
from app.utils.cache import cache
from app.utils.notifications import TerminalNotification, EmailNotification
from app.config import Config
from app.database import SessionLocal
from app.utils.logger import logger

class Scraper:
    def __init__(self, page_limit: int, proxy: str = None):
        self.page_limit = page_limit
        self.proxy = proxy
        self.base_url = "https://dentalstall.com/shop/"

        # Initialize the appropriate notification class based on DB config
        self.notification = self.get_notification_instance()

    def get_notification_instance(self):
        db = SessionLocal()
        db_config = db.query(NotificationConfigDB).first()
        db.close()

        if db_config:
            notification_type = NotificationType(db_config.notification_type)
            recipients = db_config.recipients.split(",")
        else:
            config = Config.DEFAULT_NOTIFICATION_CONFIG
            notification_type = config["notification_type"]
            recipients = config["recipients"]

        if notification_type == NotificationType.email:
            return EmailNotification(recipients=recipients)
        else:
            return TerminalNotification()

    async def fetch_page(self, session, url):
        retries = 5
        delay = 2

        for attempt in range(retries):
            try:
                async with session.get(url, proxy=self.proxy) as response:
                    if response.status == 404:
                        logger.error(f"Page not found: {url}")
                        return None
                    response.raise_for_status()
                    return await response.text()
            except aiohttp.ClientError as e:
                logger.error(f"Error fetching {url}: {e}")
                if attempt < retries - 1:
                    logger.info(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                    delay *= 2
                else:
                    logger.error(f"Failed to fetch {url} after {retries} attempts.")
                    return None

    async def scrape_page(self, session, page_number: int):
        url = f"{self.base_url}page/{page_number}/"
        html = await self.fetch_page(session, url)
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        products = []

        for product in soup.select('.product'):
            title_tag = product.select_one('.woo-loop-product__title a')
            title = title_tag.text.strip() if title_tag else 'N/A'
            price_tag = product.select_one('.price ins .woocommerce-Price-amount.amount bdi')
            if not price_tag:
                price_tag = product.select_one('.price .woocommerce-Price-amount.amount bdi')
            price = float(price_tag.text.strip().replace('₹', '').replace(',', '')) if price_tag else 0.0
            image_tag = product.select_one('.mf-product-thumbnail img')
            image_url = image_tag['data-lazy-src'] if image_tag else 'N/A'
            if price == 0.0:
                logger.error(f"Error: Missing price for a product on page {page_number}, maybe item out of stock")
                continue
            products.append(Product(product_title=title, product_price=price, path_to_image=image_url))

        return products

    async def scrape(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.scrape_page(session, page) for page in range(1, self.page_limit + 1)]
            results = await asyncio.gather(*tasks)
            products = [item for sublist in results for item in sublist]
            return products

    async def cache_products(self, products: List[Product]):
        new_products = []
        for product in products:
            cached_price = await cache.get(product.product_title)
            if cached_price is None or float(cached_price) != product.product_price:
                await cache.set(product.product_title, product.product_price)
                new_products.append(product)
        return new_products

    async def save_to_db(self, products: List[Product]):
        try:
            with open('products.json', 'r') as f:
                existing_products = json.load(f)
        except (FileNotFoundError,json.JSONDecodeError):
            existing_products = []
        existing_products.extend([product.dict() for product in products])
        with open('products.json', 'w') as f:
            json.dump(existing_products, f, indent=4)

    async def run(self):
        products = await self.scrape()
        updated_products = await self.cache_products(products)
        await self.save_to_db(updated_products)
        updated_count = len(updated_products)
        self.notification.send(f"{updated_count} products were scraped and updated in DB")
        return updated_count
