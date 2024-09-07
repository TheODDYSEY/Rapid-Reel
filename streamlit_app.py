import streamlit as st
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from threading import Thread
import pandas as pd
from io import StringIO

# Initialize FastAPI app
api = FastAPI()

# Define a Pydantic model to validate incoming data
class MovieData(BaseModel):
    data: str  # Expected to be a CSV-like string

# Function to run FastAPI server
def run_server():
    uvicorn.run(api, host="0.0.0.0", port=8000)

# Create a background thread to run FastAPI
thread = Thread(target=run_server)
thread.start()

# Define the FastAPI endpoint to accept POST requests
@api.post("/upload-data/")
async def upload_data(request: Request, movie_data: MovieData):
    csv_data = StringIO(movie_data.data)
    df = pd.read_csv(csv_data)
    st.session_state['data'] = df  # Store data in Streamlit session state
    return {"status": "Data received successfully!"}

# Streamlit UI
st.title('YTS Movie Scraper')
st.write('The scraped movie data will be displayed here.')

# Display the data if available
if 'data' in st.session_state:
    st.dataframe(st.session_state['data'])
else:
    st.write("No data received yet.")
