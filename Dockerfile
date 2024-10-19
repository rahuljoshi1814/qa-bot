# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's caching mechanism
COPY requirements.txt .

# Install pip and any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt  # Correct command

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Streamlit uses
EXPOSE 8501

# Environment variables (replace with your actual API keys or use build arguments)
ENV PINECONE_API_KEY=67a15eeb-138f-40cc-b612-04a1edb888ec
ENV COHERE_API_KEY=wPSktdXU3ePg4RYT7eFO8xdoZK2rW0ipE7qyK0fa

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
