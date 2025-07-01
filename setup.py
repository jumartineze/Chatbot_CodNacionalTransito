"""Package installer"""

from setuptools import find_packages, setup  # type: ignore

setup(
    name="Chatbot_CodNacionalTransito",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain==0.3.26",
        "langchain-community==0.3.26",
        "langchain-openai==0.3.12",
        "langgraph==0.3.24",
        "chromadb==1.0.0",
        "python-dotenv==1.1.0",
        "tiktoken==0.9.0"
    ],
)
