# QA Bot

## Overview
The QA Bot is an interactive question-answering application that utilizes the Streamlit framework for the frontend, along with Pinecone and Cohere APIs for document retrieval and natural language processing, respectively. This application enables users to upload PDF documents and ask questions about the content within those documents, receiving real-time answers based on the extracted information. 

This project is designed to showcase how modern AI and machine learning techniques can be leveraged to create user-friendly applications.

## Features
- **Document Upload:** Users can easily upload PDF documents for analysis.
- **Interactive Q&A:** Ask questions related to the document content and receive accurate answers in real-time.
- **User-Friendly Interface:** Built with Streamlit for a seamless user experience.
- **Dockerized Deployment:** The entire application is packaged in a Docker container, ensuring easy deployment and scalability.

## Technologies Used
- **Python 3.9:** The primary programming language for the application.
- **Streamlit:** A powerful framework for building interactive web applications using Python.
- **Pinecone:** A vector database that enables fast and efficient retrieval of document embeddings.
- **Cohere API:** Utilized for natural language processing tasks to understand and generate responses.
- **Docker:** Used for containerizing the application, making it easy to run on any system with Docker installed.

## Installation

### Prerequisites
To run the application, ensure you have the following installed:
- **Docker:** Follow the instructions on the [Docker website](https://docs.docker.com/get-docker/) to install Docker on your machine.
- **API Keys:**
  - **Pinecone:** Sign up at [Pinecone](https://www.pinecone.io/) and create an API key.
  - **Cohere:** Sign up at [Cohere](https://cohere.ai/) and obtain your API key.

### Building the Docker Image
1. **Clone the Repository:**
   Start by cloning this repository to your local machine:
   ```bash
   git clone https://github.com/rahuljoshi1814/qa-bot.git
   cd qa-bot
2. **Build the Docker Image: Build the Docker image by running the following command in your terminal:**
    docker build -t qa-bot .
   
### Running the Application
Once the image is built successfully, you can run the application using Docker.
1. Run the Docker Container: Execute the following command to start the application:
   docker run -p 8501:8501 -e PINECONE_API_KEY=your_pinecone_key -e COHERE_API_KEY=your_cohere_key qa-bot
-- Port Mapping: The application will be accessible on port 8501 of your localhost.
-- Environment Variables: Make sure to replace your_pinecone_key and your_cohere_key with your actual API keys.
2. Access the Application: Open your web browser and navigate to http://localhost:8501. You should see the QA bot interface ready for interaction.

### Usage
1. Upload a Document: Use the upload feature to add a PDF document that you want to query.

2. Ask Questions: Type your questions in the input field. For example, "What is the main topic of this document?" or "Summarize the key points."

3. Receive Answers: Click on the "Ask" button to get answers derived from the document's content. The responses are generated based on the context of the document, thanks to the Cohere API's natural language processing capabilities.
   
