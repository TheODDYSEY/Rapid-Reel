# Use a smaller base image for Python
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements file first (to leverage Docker's caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
