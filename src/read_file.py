#@title Setting up the Auth
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
import google.generativeai as genai
import qdrant_client
import sys
import io
import os

os.environ["GOOGLE_API_KEY"] = 'AIzaSyBy7olYxlX8bHNXZ3AffnvR8FNth7KRIQ8'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def read_local():
    path_pdf = "D:/workspace/translator-app-gpt-4o-streamlit-main/datasource/file_pdf"
    pdf_loader = PyPDFDirectoryLoader(path_pdf, extract_images= False)

    docs = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)

    docs = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.from_documents(
        documents = docs,
        embedding=embeddings # passing in the embedder model
    )
    db.save_local('app/datasource/db_faiss')

def read_db():
    path_pdf = "D:/workspace/translator-app-gpt-4o-streamlit-main/datasource/file_pdf"
    pdf_loader = PyPDFDirectoryLoader(path_pdf, extract_images= False)

    docs = pdf_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)

    docs = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Qdrant.from_documents(
        docs,
        embeddings,
        url="https://50b39a49-abbe-4a22-8920-43bcc89ad9c3.europe-west3-0.gcp.cloud.qdrant.io:6333",
        prefer_grpc=False,
        collection_name="report",
        api_key="NQtcF8AIh0lhQy3kIqEO87PeTsxXeG7g2x3hW9Rd_T3sPbwUvtUrMw",
    )

    return vectorstore

def load_db():
    client = qdrant_client.QdrantClient(
        url="https://50b39a49-abbe-4a22-8920-43bcc89ad9c3.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key="NQtcF8AIh0lhQy3kIqEO87PeTsxXeG7g2x3hW9Rd_T3sPbwUvtUrMw"
    )
    
    # Lấy tất cả các điểm (points) từ collection
    scroll_result = client.scroll(
        collection_name="report",
        with_vectors=True  # Đảm bảo lấy cả các vector
    )
    
    all_points = scroll_result[0]
    while scroll_result[1] is not None:
        scroll_result = client.scroll(
            collection_name="report",
            offset=scroll_result[1],
            with_vectors=True
        )
        all_points.extend(scroll_result[0])
    print(all_points)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Qdrant.from_points(
        points=all_points,
        embeddings=embeddings
    )
    return vectorstore

load_db()