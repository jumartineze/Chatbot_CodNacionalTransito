"""Package installer for Chatbot_CodNacionalTransito"""

from setuptools import find_packages, setup

setup(
    name="Chatbot_CodNacionalTransito",
    version="0.1",
    description="Chatbot para responder preguntas sobre el Código Nacional de Tránsito de Colombia.",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "langchain==0.3.26",
        "langchain-community==0.3.26",
        "langchain-openai==0.3.12",
        "langgraph==0.3.24",
        "python-dotenv>=1.1.0,<2.0.0",
        "tiktoken>=0.9.0,<1.0.0",
        "chromadb>=1.0.0,<1.1.0",
        "streamlit>=1.33.0,<2.0.0"
    ],
)
