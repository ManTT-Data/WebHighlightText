import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import sys
import io

# Get API gemini
os.environ["GOOGLE_API_KEY"] = 'AIzaSyBy7olYxlX8bHNXZ3AffnvR8FNth7KRIQ8'
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Get chatbot model
llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.4)

# Get embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create prompt
prompt_trans = PromptTemplate(
    template = """Context:{context}\n
    System:\n
    You are a chatbot that translate user's input to {output_language} base on the context provided.\n
    User's input:\n{input}""",
)

prompt_definition = PromptTemplate(
    template = """Context:{context}\n
    System:\n
    You are a chatbot that answer user's request in {output_language} base on the context provided.\n
    User's input:\n Explain the meaning of "{input}" in this sentence: {sentence}.""",
)

# Get data from database
db = FAISS.load_local('datasource/db_faiss', embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs = {"k":7}, max_tokens_limit=1024)

# Create RAG chain
prompt_trans_chain = create_stuff_documents_chain(llm, prompt_trans)
rag_chain_trans = create_retrieval_chain(retriever, prompt_trans_chain)

prompt_def_chain = create_stuff_documents_chain(llm, prompt_definition)
rag_chain_def = create_retrieval_chain(retriever, prompt_def_chain)

input = "It performs mathematical calculations and logical operations at high speed, and it controls the other parts of the computer. What is (It) in this sentence?"
def translate(output_language, input):
    result = rag_chain_trans.invoke({"output_language": output_language, "input": input})
    answer = result["answer"]
    return answer

def definition(output_language, sentence, input):
    result = rag_chain_def.invoke({"output_language": output_language, "sentence": sentence, "input": input})
    answer = result["answer"]
    return answer

def check_retrieval():
    retrieval_results = retriever.get_relevant_documents(input)
    print("Retrieved documents:")
    for doc in retrieval_results:
        print(doc)

# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# print(definition("Vietnamese", input, "other parts of the computer"))

