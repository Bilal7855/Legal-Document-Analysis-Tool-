from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from fastapi.middleware.cors import CORSMiddleware 

import os

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS configuration
origins = ["http://localhost:8001"]  # Replace with your allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Google API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Google API Key is not set. Please check your .env file.")

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(model="models/embedding-001", api_key=api_key)

def get_pdf_text(pdf_files: List[UploadFile]) -> str:
    text = ""
    for pdf_file in pdf_files:
        try:
            pdf_reader = PdfReader(pdf_file.file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error processing PDF: {str(e)}")
    return text

def get_text_chunks(text: str) -> List[str]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks: List[str]):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)

    index_dir = "faiss_index"
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    try:
        vector_store.save_local(index_dir)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving FAISS index: {str(e)}")

def get_conversational_chain():
    prompt_template = """Answer the question as detailed as possible from the provided context. If the answer is not in the provided context, just say, "Answer is not available in the context". Don't provide the wrong answer.\n\n
     context:\n{context}\n
      Question:\n{question}\n

     Answer:
     """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

@app.post("/upload")
async def upload_files(pdf_files: List[UploadFile] = File(...)):
    try:
        if not pdf_files:
            raise HTTPException(status_code=400, detail="No files provided.")
        raw_text = get_pdf_text(pdf_files)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        return {"message": "Files processed and vector store created successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/query")
async def query_document(question: str = Form(...)):
    try:
        if not question:
            raise HTTPException(status_code=400, detail="Question is required.")
        embeddings = get_embeddings()
        if not os.path.isfile("faiss_index/index.faiss"):
            raise FileNotFoundError("FAISS index file is missing.")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(question)
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": question}, return_only_outputs=True)
        return {"answer": response["output_text"]}
    except Exception as e:
        return {"error": str(e)}
