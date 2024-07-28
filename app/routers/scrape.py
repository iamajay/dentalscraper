from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models import ScrapeSettings
from app.services.scraper import Scraper
from app.config import Config

router = APIRouter()


@router.post("/scrape")
async def scrape(settings: ScrapeSettings, token: str = Depends(get_current_user)):
    scraper = Scraper(page_limit=settings.page_limit, proxy=settings.proxy)
    updated_count = await scraper.run()
    return {"message": f"Scraped and updated {updated_count} products"}
