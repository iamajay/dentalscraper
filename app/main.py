from fastapi import FastAPI
from app.routers import scrape, notifications
from app.database import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(scrape.router, prefix="/api", tags=["scrape"])
app.include_router(notifications.router, prefix="/api", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "Welcome to DentScraper API"}
