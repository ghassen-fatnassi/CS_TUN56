import os
import aiohttp
import asyncio
import logging
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Updated imports
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema import Document

import bs4
from PyPDF2 import PdfReader
from io import BytesIO
from dotenv import load_dotenv

from asyncio import Lock
from contextlib import asynccontextmanager

# --------------------- Load Environment Variables ---------------------
load_dotenv()

USER_AGENT = os.getenv("USER_AGENT", "ZephyrRAGSystem/1.0 (contact@example.com)")
VECTORSTORE_DIR = os.getenv("VECTORSTORE_DIR", "faiss_index")

# --------------------- Configuration ---------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for shared resources
llm: Optional[HuggingFaceEndpoint] = None
embedding_model: Optional[SentenceTransformerEmbeddings] = None
text_splitter: Optional[RecursiveCharacterTextSplitter] = None
vectorstore: Optional[FAISS] = None  # Explicitly set to None initially
vectorstore_lock = Lock()

# --------------------- Lifespan Event Handlers ---------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm, embedding_model, text_splitter, vectorstore
    logger.info("Initializing models and resources...")

    try:
        llm = HuggingFaceEndpoint(
            endpoint_url="https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
            temperature=0.7,
            model_kwargs={
                "api_key": HUGGINGFACE_API_KEY,
                "max_length": 512,
            }
        )
        embedding_model = SentenceTransformerEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        
        load_vectorstore()
        logger.info("Startup initialization completed.")

        yield

    finally:
        save_vectorstore()
        logger.info("Shutdown complete. Vector store saved.")

# --------------------- FastAPI Initialization ---------------------

app = FastAPI(title="Zephyr-7B RAG System API", lifespan=lifespan)

# --------------------- CORS Middleware ---------------------
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------- Pydantic Models ---------------------

class ParseRequest(BaseModel):
    urls: List[str]

class AnswerRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    source_documents: List[str]

# --------------------- Helper Functions ---------------------

async def fetch_and_process_url(session: aiohttp.ClientSession, url: str) -> List[Document]:
    documents = []
    try:
        async with session.get(url) as response:
            if response.status != 200:
                logger.error(f"Failed to fetch URL {url}: HTTP {response.status}")
                return documents

            content = await response.read()
            content_type = response.headers.get('Content-Type', '')

            if 'application/pdf' in content_type:
                reader = PdfReader(BytesIO(content))
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        documents.append(Document(
                            page_content=text,
                            metadata={"source": url, "page": i + 1}
                        ))
            else:
                text = content.decode('utf-8', errors='ignore')
                soup = bs4.BeautifulSoup(text, 'html.parser')
                cleaned_text = soup.get_text()
                documents.append(Document(
                    page_content=cleaned_text,
                    metadata={"source": url}
                ))
    except Exception as e:
        logger.error(f"Failed to fetch or process URL {url}: {e}")

    return documents

async def load_data_async(urls: List[str]) -> List[Document]:
    documents = []
    headers = {
        "User-Agent": USER_AGENT
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [fetch_and_process_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error processing URL: {result}")
            elif result:
                documents.extend(result)
    return documents

def save_vectorstore():
    global vectorstore
    if vectorstore:
        os.makedirs(VECTORSTORE_DIR, exist_ok=True)
        vectorstore.save_local(VECTORSTORE_DIR)
        logger.info(f"Vector store saved to '{VECTORSTORE_DIR}'.")
    else:
        logger.warning("Attempted to save vector store, but it is not initialized.")

def load_vectorstore():
    global vectorstore
    if os.path.exists(VECTORSTORE_DIR) and os.path.isdir(VECTORSTORE_DIR):
        try:
            vectorstore = FAISS.load_local(VECTORSTORE_DIR, embedding_model)
            logger.info(f"Vector store loaded from '{VECTORSTORE_DIR}'.")
        except Exception as e:
            logger.error(f"Failed to load vector store from '{VECTORSTORE_DIR}': {e}")
            vectorstore = None
    else:
        vectorstore = None  # Ensure vectorstore is None if loading fails
        logger.info("No existing vector store found. Initialized to None.")

# --------------------- API Endpoints ---------------------

@app.post("/parse", summary="Parse and process a list of URLs")
async def parse_urls(request: ParseRequest):
    global vectorstore
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided.")

    logger.info(f"Received URLs to parse: {request.urls}")

    try:
        documents = await load_data_async(request.urls)
        if not documents:
            raise HTTPException(status_code=400, detail="No valid documents found from the provided URLs.")

        async with vectorstore_lock:
            # Initialize or add to the vectorstore as needed
            if vectorstore is None:
                split_documents = text_splitter.split_documents(documents)
                vectorstore = FAISS.from_documents(split_documents, embedding_model)
                logger.info(f"Initialized vector store with {len(split_documents)} documents.")
            else:
                split_documents = text_splitter.split_documents(documents)
                vectorstore.add_documents(split_documents)
                logger.info(f"Added {len(split_documents)} documents to the vector store.")

            save_vectorstore()

        return {"message": "URLs parsed and vector store updated successfully."}

    except Exception as e:
        logger.error(f"Error during parsing: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred during parsing: {e}")

@app.post("/answer", response_model=AnswerResponse, summary="Get answer based on parsed content")
async def get_answer(request: AnswerRequest):
    if vectorstore is None:
        raise HTTPException(status_code=400, detail="Vector store not initialized. Please parse URLs first.")

    if not request.question:
        raise HTTPException(status_code=400, detail="No question provided.")

    logger.info(f"Received question: {request.question}")

    try:
        prompt_template = PromptTemplate(
            template="""
            You are an expert in analyzing information from multiple sources. Provide a concise answer based on the following context.
            Context: {context}
            Question: {question}
            Answer:
            """,
            input_variables=["context", "question"]
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt_template}
        )

        response = qa_chain.invoke({"query": request.question})
        answer = response['result'].strip() if response['result'].strip() else "Sorry, I don't know."

        source_docs = [doc.metadata.get('source') for doc in response['source_documents']]

        logger.info(f"Answer generated: {answer}")
        return AnswerResponse(answer=answer, source_documents=source_docs)

    except Exception as e:
        logger.error(f"Error during answering: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while generating the answer: {e}")

# --------------------- Run the Server ---------------------

if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8080))

    uvicorn.run(app, host=HOST, port=PORT)
