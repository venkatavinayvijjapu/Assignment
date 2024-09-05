from fastapi import FastAPI, File, UploadFile, APIRouter
from starlette.responses import JSONResponse
from pathlib import Path
import os
import uuid
from langchain_community.document_loaders import PyPDFLoader
from sentence_transformers import SentenceTransformer
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
# Initialize FastAPI app and ChromaDB client
app = FastAPI()
router = APIRouter()
client = chromadb.Client()
UPLOAD_DIRECTORY = Path("upload")
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)  # Ensure the upload directory exists

# Create a ChromaDB collection
messages_collection = client.create_collection("messages_collection")

# Load Sentence Transformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

class URLRequest(BaseModel):
    url: str
@router.post("/process_url/")
async def process_pdf(request: URLRequest):
    # Validate file type
  

    # Extract and clean text from the PDF
    try:
        url=request.url
        loader = WebBaseLoader(url)
        
        # Load the web page content
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(data)
        print(f"Loaded {len(documents)} documents from {url}")
        print(documents)
        # return document_chunks
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Failed to process PDF file: {str(e)}"})

    # Generate a unique chat_id
    chat_id = str(uuid.uuid4())
    messages_collection = client.create_collection(chat_id)


    # Prepare documents, embeddings, and metadata for storing in ChromaDB
    doc_texts = [doc.page_content for doc in documents]
    embeddings = model.encode(doc_texts, convert_to_tensor=False)
    metadatas = [
        {
            'page_number': doc.metadata.get('page_number', idx + 1),
            'chat_id': chat_id  # Store chat_id in metadata
        } 
        for idx, doc in enumerate(documents)
    ]
    ids = [str(uuid.uuid4()) for _ in documents]

    # Store the documents and embeddings in the ChromaDB collection
    messages_collection.add(
        documents=doc_texts,
        embeddings=embeddings.tolist(),
        metadatas=metadatas,
        ids=ids,
    )

    # Return the chat_id and success message
    return JSONResponse(status_code=200, content={
        "chat_id": chat_id,
        "message": "PDF content processed and stored successfully."
    })
