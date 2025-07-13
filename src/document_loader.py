import re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# ----------------------------
# Global Configuration
# ----------------------------

# Regex to match article headers (e.g., "ARTÍCULO 5")
HEADER_PATTERN = re.compile(
    r"^(?:ART[IÍ]CULO)\s+\d+[^\w]*?(?=[A-ZÁÉÍÓÚÑ])",
    flags=re.DOTALL | re.IGNORECASE
)

# Regex to extract article numbers
ARTICLE_PATTERN = re.compile(
    r"(?:ART[IÍ]CULO)\s+(\d+)", re.IGNORECASE
)

# Text splitter configuration for chunking
TEXT_SPLITTER = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50
)

# OpenAI embedding model instance
EMBEDDING_MODEL = OpenAIEmbeddings()

# ----------------------------
# Helper Functions
# ----------------------------

def clean_section_text(text):
    """
    Removes the article header (e.g., 'Artículo 5') from the given text,
    preserving the actual content starting from the next uppercase letter.
    """
    cleaned_text = HEADER_PATTERN.sub("", text, count=1)
    return cleaned_text.strip()


def extract_article_sections(text):
    """
    Extracts article sections from the full text.

    Returns:
        List of tuples (cleaned_text, article_number)
    """
    article_sections = []
    matches = list(ARTICLE_PATTERN.finditer(text))
    total_matches = len(matches)

    if total_matches == 0:
        return article_sections  # No matches found

    for idx, match in enumerate(matches):
        start_pos = match.start()
        article_num = match.group(1)

        # Determine end position: either next article or end of text
        end_pos = matches[idx + 1].start() if idx + 1 < total_matches else len(text)

        section_text = text[start_pos:end_pos]
        cleaned_section = clean_section_text(section_text)

        article_sections.append((cleaned_section, article_num))

    return article_sections

# ----------------------------
# Main Processing Function
# ----------------------------

def load_and_process_document(file_path):
    """
    Loads a text document and processes it into a vector store
    by splitting into article-based chunks and generating embeddings.

    Args:
        file_path (str): Path to the input text file.

    Returns:
        Chroma vector store instance for semantic search.
    """
    # Load document content
    text = TextLoader(file_path).load()[0].page_content

    # Extract article-based sections
    article_sections = extract_article_sections(text)

    # Split sections into smaller documents with metadata
    splits = [
        doc
        for section_text, article_num in article_sections
        for doc in TEXT_SPLITTER.create_documents(
            texts=[section_text],
            metadatas=[{
                "source": file_path,
                "source_article": article_num
            }]
        )
    ]

    # Build and return vector index
    return Chroma.from_documents(splits, EMBEDDING_MODEL)
