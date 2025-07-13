import os
import streamlit as st
from dotenv import load_dotenv

# -----------------------
# Load environment variables
# -----------------------

load_dotenv(".env")  # Load from .env file

# Set required environment variables for LangChain and OpenAI
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

# -----------------------
# Import chatbot components
# -----------------------

from src.document_loader import load_and_process_document
from src.graph_wrapper import build_graph

# -----------------------
# Initialize chatbot (cached)
# -----------------------

@st.cache_resource
def get_chatbot():
    """
    Load the vector store and initialize the LangGraph chatbot.
    """
    file_path = "./data/ley-769-de-2002-codigo-nacional-de-transito_preprocessed.txt"
    vector_store = load_and_process_document(file_path)
    graph = build_graph(vector_store)
    return graph

graph = get_chatbot()

# -----------------------
# Streamlit UI
# -----------------------

st.title("Chatbot Código Nacional de Tránsito de Colombia")
user_input = st.text_input("Haz tu pregunta sobre tránsito:")

# -----------------------
# Handle user input and response streaming
# -----------------------

if user_input:
    for step in graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode="values"
    ):
        st.write(step["messages"][-1].content)
