from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import os
from io import BytesIO
from typing import List
from docx import Document
import PyPDF2
from fastapi.responses import JSONResponse
import logging

# Initialize FastAPI
app = FastAPI()

# Initialize the Sentence-Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize ChromaDB client
client = chromadb.Client()
collection = client.create_collection("document_collection")

# Helper function to extract text from PDF
def extract_text_from_pdf(file: BytesIO) -> str:
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        # Process file content here if needed
        return JSONResponse(content={"filename": file.filename, "content": content.decode("utf-8")})
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Helper function to extract text from DOCX
def extract_text_from_docx(file: BytesIO) -> str:
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

# Helper function to extract text from TXT
def extract_text_from_txt(file: BytesIO) -> str:
    return file.read().decode('utf-8')

# Function to process the uploaded document
def process_document(file: UploadFile) -> str:
    extension = file.filename.split('.')[-1].lower()
    contents = file.file.read()

    if extension == "pdf":
        return extract_text_from_pdf(BytesIO(contents))
    elif extension == "docx":
        return extract_text_from_docx(BytesIO(contents))
    elif extension == "txt":
        return extract_text_from_txt(BytesIO(contents))
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

# API to ingest a document
@app.post("/ingest_document/")
async def ingest_document(file: UploadFile = File(...)):
    try:
        text = process_document(file)
        embedding = model.encode(text).tolist()  # Generate embedding using the sentence transformer
        
        # Store in ChromaDB
        metadata = {"filename": file.filename}
        collection.add(
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding],
            ids=[file.filename]
        )
        return {"message": "Document ingested successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting document: {str(e)}")

# API to query the database
@app.get("/query/")
async def query_document(query: str, top_k: int = 3):
    try:
        query_embedding = model.encode(query).tolist()  # Query embedding
        
        # Perform similarity search in ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return {"results": results["documents"], "metadata": results["metadatas"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying documents: {str(e)}")

# To run the server using: uvicorn main:app --reload

@app.post("/upload/")
async def upload_file(file: UploadFile):
    return {"filename": file.filename}