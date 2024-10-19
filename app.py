import streamlit as st
import hashlib
from qa_bot import (
    initialize_services, initialize_index, preprocess_text, extract_text_from_pdf,
    split_text_into_chunks, handle_query, log_feedback
)

# Streamlit UI setup
st.title("Interactive QA Bot")

# File upload
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Initialize services and index
cohere_api, pc = initialize_services()
model, index = initialize_index(pc)

if uploaded_file is not None:
    # Extract and process text from PDF
    extracted_text = extract_text_from_pdf(uploaded_file)
    preprocessed_text = preprocess_text(extracted_text)

    # Generate a dynamic document ID based on the file name
    doc_id = hashlib.md5(uploaded_file.name.encode()).hexdigest()

    # Split text into chunks and embed each chunk
    text_chunks = split_text_into_chunks(preprocessed_text)
    for idx, chunk in enumerate(text_chunks):
        document_embedding = model.encode([chunk])[0]
        index.upsert(vectors=[{
            "id": f"{doc_id}_{idx}",
            "values": document_embedding.tolist(),
            "metadata": {"text": chunk}
        }])
    st.success("Document uploaded and processed!")

# Query input
query = st.text_input("Ask a question based on the uploaded document:")

if query:
    try:
        generated_answer, relevant_docs = handle_query(query, model, index, cohere_api)
        if generated_answer and relevant_docs:
            st.subheader("Answer:")
            st.write(generated_answer)
            
            st.subheader("Relevant Document Segments:")
            st.write(relevant_docs)
        else:
            st.error("No relevant document segments found.")
    except Exception as e:
        st.error(str(e))

# Collect user feedback
feedback = st.radio("Was this response helpful?", options=["Yes", "No"])
if feedback:
    st.write("Thank you for your feedback!" if feedback == "Yes" else "We will improve!")
    
# Log feedback for future analysis
if query:
    log_feedback(query, generated_answer, feedback)
