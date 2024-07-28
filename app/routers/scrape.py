from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models import ScrapeSettings
from app.services.scraper import Scraper
from app.config import Config

router = APIRouter()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != Config.STATIC_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )
    return credentials.credentials

@router.post("/scrape")
async def scrape(settings: ScrapeSettings, token: str = Depends(get_current_user)):
    scraper = Scraper(page_limit=settings.page_limit, proxy=settings.proxy)
    updated_count = await scraper.run()
    return {"message": f"Scraped and updated {updated_count} products"}
