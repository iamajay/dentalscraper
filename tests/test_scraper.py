import unittest
import asyncio
from unittest.mock import patch, MagicMock
from aiohttp import ClientResponse, ClientSession
from app.services.scraper import Scraper
from app.models import Product

class TestScraper(unittest.TestCase):
    
    @patch('aiohttp.ClientSession.get')
    def test_fetch_page_success(self, mock_get):
        html_content = '<html></html>'
        mock_response = MagicMock(ClientResponse)
        mock_response.status = 200
        mock_response.text = asyncio.coroutine(lambda: html_content)
        mock_get.return_value.__aenter__.return_value = mock_response

        scraper = Scraper(page_limit=1)
        async def run_test():
            async with ClientSession() as session:
                result = await scraper.fetch_page(session, 'http://example.com')
                self.assertEqual(result, html_content)

        asyncio.run(run_test())

    @patch('aiohttp.ClientSession.get')
    def test_fetch_page_failure(self, mock_get):
        mock_response = MagicMock(ClientResponse)
        mock_response.status = 404
        mock_get.return_value.__aenter__.return_value = mock_response

        scraper = Scraper(page_limit=1)
        async def run_test():
            async with ClientSession() as session:
                result = await scraper.fetch_page(session, 'http://example.com')
                self.assertIsNone(result)

        asyncio.run(run_test())

    def test_scrape_page(self):
        html_content = '''
        <li class="product">
            <div class="woo-loop-product__title"><a>Product 1</a></div>
            <span class="price"><ins><span class="woocommerce-Price-amount amount"><bdi><span class="woocommerce-Price-currencySymbol">₹</span>1000.00</bdi></span></ins></span>
            <div class="mf-product-thumbnail"><img data-lazy-src="http://example.com/image1.jpg"/></div>
        </li>
        '''
        scraper = Scraper(page_limit=1)
        async def run_test():
            async with ClientSession() as session:
                with patch.object(scraper, 'fetch_page', return_value=html_content):
                    products = await scraper.scrape_page(session, 1)
                    expected_product = Product(product_title='Product 1', product_price=1000.0, path_to_image='http://example.com/image1.jpg')
                    self.assertEqual(products, [expected_product])

        asyncio.run(run_test())


if __name__ == '__main__':
    unittest.main()
