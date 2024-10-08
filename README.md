﻿# SEO Web Crawler with Django, Celery, and Redis
![image](https://github.com/user-attachments/assets/ad8fcad9-7962-49fd-9569-ba8829bf13e6)

This project is a web crawler built using Django for the backend, Celery for task management, and Redis as the message broker. The application allows you to start and stop web crawling tasks, where each task involves fetching and parsing web pages.

## Project Features

- **Web Crawler**: Fetches and parses web pages to extract information such as headings, meta tags, links, etc.
- **Task Management**: Uses Celery to handle asynchronous tasks, ensuring non-blocking operations for crawling multiple pages.
- **Task Control**: Provides API endpoints to start and stop tasks.
- **Redis Integration**: Redis serves as the message broker for task management using Celery.
- **Django REST Framework**: Exposes a simple API for controlling crawler tasks.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Task Queue**: Celery
- **Message Broker**: Redis
- **Database**: PostgreSQL (or SQLite for development)
- **Containerization**: Docker, Docker Compose

## Setup and Installation

### Prerequisites

1. **Docker & Docker Compose**: Ensure you have Docker and Docker Compose installed on your system.
2. **Python**: You can run this project in a virtual environment without Docker if preferred.

### Step-by-Step Setup

#### 1. Clone the repository

```bash
git clone https://github.com/yourusername/web-crawler.git
cd web-crawler
```
#### 2. Set up environment variables
Create .env file in the project root to store environment variables:
```POSTGRES_DB=webcrawler_db
URL_QUEUE_DB=webcrawler_queue_db
POSTGRES_USER=webcrawler_user
POSTGRES_PASSWORD=9YqHj84&slLmX2Qa
DB_HOST=db
DB_PORT=5432

REDIS_HOST=redis
REDIS_PORT=6379

DEBUG=True
SECRET_KEY=zig298239

DATABASE_URL=postgres://webcrawler_user:9YqHj84&slLmX2Qa@db:5432/webcrawler_db
URL_QUEUE_DATABASE_URL=postgres://webcrawler_user:9YqHj84&slLmX2Qa@db:5432/webcrawler_queue_db
```

#### 3. Build and run the project using Docker
Make sure Docker is running on your machine. Then, to build and run the Docker containers, run:
```
docker-compose up --build
```
This will build and run the following services:
- **web**: The Django web application
- **db**: PostgreSQL database
- **redis**: Redis message broker
- **celery**: Celery worker for task execution

#### 4. Access the application
- **Django Admin Panel**: ```http://localhost:8000/admin/```
- **API Endpoints**: ```http://localhost:8000/api/```

# API Endpoints
## 1. Add URL to the Queue
- **Endpoint**: `http://localhost:8000/api/add-url/`
- **Method**: `POST`
- **Description**: This endpoint is used to add a new URL to the crawling queue.
- **Request Body** (JSON):
    ```json
    {
      "url": "https://example.com"
    }
    ```
- **Response**:
    - **Success**: HTTP 200 OK
    ```json
    {
      "message": "URL added to queue successfully!",
      "url": "https://example.com"
    }
    ```
    - **Error**: HTTP 400 Bad Request
    ```json
    {
      "error": "Invalid URL or URL already exists in the queue"
    }
    ```
  
## 2. Clear the URL Queue
- **Endpoint**: `http://localhost:8000/api/clear-queue/`
- **Method**: `POST`
- **Description**: This endpoint clears all URLs from the queue, effectively resetting the crawler queue.
- **Request Body**: None
- **Response**:
    - **Success**: HTTP 200 OK
    ```json
    {
      "message": "URL queue cleared successfully!"
    }
    ```
    - **Error**: HTTP 500 Internal Server Error
    ```json
    {
      "error": "An error occurred while clearing the queue."
    }
    ```
  
## 3. Start the Web Crawler

- **Endpoint**: `http://localhost:8000/api/start-crawler/`
- **Method**: `GET`
- **Description**: This endpoint starts the web crawler. It creates a Celery task that begins crawling the URLs stored in the queue. The task is executed asynchronously, and a task ID is returned to track the task.
- **Response**:
    - **Success**: HTTP 200 OK
    ```json
    {
      "message": "Crawler task started successfully!",
      "task_id": "<task_id>"
    }
    ```
    - **Error**: HTTP 500 Internal Server Error
    ```json
    {
      "error": "An error occurred while starting the crawler."
    }
    ```

- **Notes**:
  - Each time the crawler starts, a new task ID is generated.

# Project Structure
- **url_queue**: Django app handling the queueing of URLs for parsing.
- **crawler_manager**: Django app managing Celery tasks for crawling URLs.
- **Dockerfile**: Docker configuration for the Django app.
- **docker-compose.yml**: Docker Compose setup for the project including Redis, PostgreSQL, Celery, and Django services.
