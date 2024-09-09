# YTS Movie Scraper and Dashboard

**YTS Movie Scraper and Dashboard** is a full-stack application that scrapes movie data from YTS, stores it in a PostgreSQL database, and displays it on a Streamlit dashboard. The system is built using FastAPI for backend processing, Streamlit for the UI, Docker for containerization, and GitHub Actions for continuous integration and scheduled scraping.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Components](#components)
3. [Setup and Installation](#setup-and-installation)
4. [Running the Application](#running-the-application)
5. [CI/CD Pipeline with GitHub Actions](#cicd-pipeline-with-github-actions)
6. [Key Considerations](#key-considerations)
7. [Future Enhancements](#future-enhancements)

## Architecture Overview

The project follows a microservices architecture, separating concerns between data scraping, backend data processing, database management, and frontend visualization. This separation is implemented through a multi-container Docker setup that enables independent scaling and better resource management.

### High-Level Design

1. **Data Scraping Service**: A Python script (`yts-scraper.py`) scrapes movie data from YTS and exports it to an Excel file (`output.xlsx`).
2. **Backend API**: A FastAPI application (`api`) exposes an endpoint to receive the scraped data via a POST request and store it in Streamlit's session state for visualization.
3. **Data Storage**: A PostgreSQL database stores movie data and can be extended to include more sophisticated queries or analytics.
4. **Frontend UI**: A Streamlit application (`streamlit_app.py`) displays the scraped movie data in a user-friendly dashboard, allowing interactive exploration.
5. **CI/CD Pipeline**: GitHub Actions automate the scraping process on a daily basis and push the results to the Streamlit app.

### Architecture Diagram

```plaintext
+------------------+         +-----------------+       +-----------------------+
|   Data Scraper   |  --->   |   FastAPI API   |  ---> |   PostgreSQL Database  |
| (yts-scraper.py) |         |   (upload-data) |       |     (movies_db)       |
+------------------+         +-----------------+       +-----------------------+
                                 |                       |
                                 |                       |
                                 V                       V
                          +-----------------+        +-----------------+
                          | Streamlit App   |        | GitHub Actions  |
                          | (Visualization) |        | (CI/CD Pipeline)|
                          +-----------------+        +-----------------+
```

## Components

### 1. **FastAPI Backend (`streamlit_app.py`)**

- **Endpoints**:
  - `POST /upload-data/`: Accepts scraped movie data in CSV format and stores it in Streamlit's session state.
- **Threading**: Uses a background thread to run the FastAPI server alongside the Streamlit app.

### 2. **Streamlit Frontend (`streamlit_app.py`)**

- Displays the movie data in a table format using `st.dataframe`.
- Dynamically updates the data received from the FastAPI backend.

### 3. **Data Scraping Script (`yts-scraper.py`)**

- Scrapes movie data from YTS and stores it in `output.xlsx`.
- The script can be extended to scrape additional metadata or to scrape from multiple sources.

### 4. **Docker Configuration**

- **Dockerfile**: Defines the environment for the Streamlit application, installing necessary dependencies.
- **docker-compose.yaml**: Orchestrates multiple services:
  - `streamlit`: Runs the Streamlit application.
  - `db`: Runs the PostgreSQL database.

### 5. **CI/CD Pipeline (`.github/workflows`)**

- **GitHub Actions**:
  - Triggers on `push`, `pull_request`, and a daily cron schedule.
  - Automates data scraping and updates the Streamlit app with fresh data.

## Setup and Installation

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/yts-movie-scraper.git
cd yts-movie-scraper
```

### 2. **Environment Setup**

Ensure you have Docker, Docker Compose, and Python installed on your system.

### 3. **Build and Start Docker Containers**

```bash
docker-compose build
docker-compose up
```

This command will start two services:
- **Streamlit**: Available at `http://localhost:8501`
- **PostgreSQL Database**: Running internally within the Docker network.

## Running the Application

### 1. **Data Scraping**

The scraping process is automated via the GitHub Actions workflow. However, to run it locally:

```bash
python yts-scraper.py
```

### 2. **Start FastAPI Server**

The FastAPI server runs in a background thread when the Streamlit app is launched. To manually test:

```bash
uvicorn api:api --host 0.0.0.0 --port 8000
```

### 3. **Launch Streamlit Dashboard**

To run the Streamlit app locally:

```bash
streamlit run streamlit_app.py
```

## CI/CD Pipeline with GitHub Actions

The GitHub Actions workflow automates the following:

1. **Scraping Movies**: Runs the `yts-scraper.py` script daily.
2. **Data Transformation**: Converts the scraped data into CSV format.
3. **Data Upload**: Sends the transformed data to the FastAPI endpoint (`/upload-data/`).

### Workflow Configuration

- **Scheduled Runs**: The workflow is set to run daily at 3 AM UTC.
- **Secrets Management**: Use GitHub Secrets to securely store the Streamlit app URL (`STREAMLIT_APP_URL`).

## Key Considerations

1. **Data Validation**: The FastAPI backend uses Pydantic models for input validation. Ensure all incoming data meets the expected schema.
2. **Concurrency**: The FastAPI and Streamlit servers are run concurrently; monitor resource utilization to avoid conflicts.
3. **Error Handling**: Implement comprehensive error handling in the data scraper to handle edge cases like network failures or changes in the YTS API.

## Future Enhancements

1. **Advanced Analytics**: Integrate more complex data analysis features using `pandas` or SQL queries in the backend.
2. **Automated Data Persistence**: Save incoming data directly into PostgreSQL and fetch it for visualization.
3. **Real-time Updates**: Implement WebSockets to provide real-time updates to the Streamlit dashboard.
4. **User Authentication**: Add user authentication to the Streamlit app to secure access to sensitive data.

## Conclusion

This project demonstrates a robust microservices-based architecture for scraping and visualizing movie data. It leverages modern technologies like FastAPI, Docker, and GitHub Actions to create a scalable and maintainable solution. The clear separation of concerns, containerization, and automation ensure smooth operation and easy extensibility.

Feel free to explore, contribute, or provide feedback to improve CineScrape!

