# DentScraper

DentScraper is a web scraping service built using FastAPI to scrape product data from a dental supplies website. The service supports configurable scraping settings, notification configurations, and data caching.

## Project Structure

- `app/`: Contains the main application code.
  - `models.py`: Defines the data models.
  - `services/`: Contains service classes like the scraper.
  - `utils/`: Contains utility functions, cache, notifications, and logger.
  - `database.py`: Database setup and connection.
  - `config.py`: Configuration settings.
- `tests/`: Contains test cases for the application.
- `main.py`: Entry point to run the scraper.

## Setup

1. **Clone the repository:**

    ```bash
    cd dentscraper
    ```

2. **Install dependencies:**

    ```bash
    pip3 install -r requirements.txt
    ```

3. **Run the FastAPI application:**

    ```bash
    uvicorn app.main:app --reload
    ```

## API Endpoints

- **Scrape Products:**

    ```http
    POST /api/scrape
    ```

    Request body:
    ```json
    {
        "page_limit": 1,
        "proxy": ""
    }
    ```

- **Set Notification Configuration:**

    ```http
    POST /api/notification/config
    ```

    Request body:
    ```json
    {
        "notification_type": "email",
        "recipients": ["example@example.com"]
    }
    ```

- **Get Notification Configuration:**

    ```http
    GET /api/notification/config
    ```

## Notes

- Configure the static token in `app/config.py`.
- Implement email and SMS sending logic in `app/utils/notifications.py`.

## License

MIT License
