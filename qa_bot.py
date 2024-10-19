import os
import cohere
import nltk
import hashlib
import logging
import pandas as pd
import PyPDF2
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Initialize Cohere and Pinecone with API keys from environment variables
cohere_api_key = os.getenv("COHERE_API_KEY", "wPSktdXU3ePg4RYT7eFO8xdoZK2rW0ipE7qyK0fa")  # Use your Cohere API key here
pinecone_api_key = os.getenv("PINECONE_API_KEY", "67a15eeb-138f-40cc-b612-04a1edb888ec")  # Use your Pinecone API key here

# Initialize Cohere and Pinecone clients
def initialize_services():
    try:
        cohere_api = cohere.Client(cohere_api_key)
        pc = Pinecone(api_key=pinecone_api_key)
        return cohere_api, pc
    except Exception as e:
        raise Exception(f"Failed to initialize services: {str(e)}")

# Create or connect to Pinecone index
def initialize_index(pc, index_name="genai"):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,  # Match with the embedding model dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    index = pc.Index(index_name)
    return model, index

# Preprocess text function
def preprocess_text(text):
    if pd.isnull(text):
        return ""
    text = str(text).lower()
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return " ".join(words)

# PDF text extraction function
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Split document text into smaller chunks
def split_text_into_chunks(text, chunk_size=500):
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

# Log feedback function
def log_feedback(query, response, feedback):
    logging.basicConfig(filename="feedback.log", level=logging.INFO)
    logging.info(f"Query: {query}, Response: {response}, Feedback: {feedback}")

# Handle query to Pinecone and Cohere
def handle_query(query, model, index, cohere_api):
    query_embedding = model.encode(query)
    
    try:
        results = index.query(vector=query_embedding.tolist(), top_k=5, include_metadata=True)
        relevant_docs = "\n".join([match['metadata']['text'] for match in results['matches']])
    except Exception as e:
        raise Exception(f"Error querying Pinecone: {str(e)}")
    
    if relevant_docs:
        prompt = f"Question: {query}\n\nRelevant Documents:\n{relevant_docs}\n\nAnswer:"
        try:
            cohere_response = cohere_api.generate(
                model="command-xlarge-nightly",
                prompt=prompt,
                max_tokens=300 if len(relevant_docs) > 500 else 150
            )
            generated_answer = cohere_response.generations[0].text.strip()
            return generated_answer, relevant_docs
        except Exception as e:
            raise Exception(f"Error generating response from Cohere: {str(e)}")
    return None, None
