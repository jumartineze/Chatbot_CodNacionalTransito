import re

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

HEADER_PATTERN = re.compile(
    r"^(?:ART[IÍ]CULO)\s+\d+[^\w]*?(?=[A-ZÁÉÍÓÚÑ])",
    flags=re.DOTALL | re.IGNORECASE
)

ARTICLE_PATTERN = re.compile(
    r'(?:ART[IÍ]CULO)\s+(\d+)', re.IGNORECASE
)

TEXT_SPLITTER = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300,
    chunk_overlap=50
)

EMBEDDING_MODEL = OpenAIEmbeddings()


def clean_section_text(text):
    """
    Remove the article header (e.g., 'Artículo 5') and everything until
    the next uppercase letter.
    """
    cleaned_text = HEADER_PATTERN.sub("", text, count=1)
    return cleaned_text.strip()


def extract_article_sections(text):
    """
    Extract article sections with their numbers, cleaning headers.
    Returns list of (cleaned_text, article_number).
    """
    article_sections = []
    matches = list(ARTICLE_PATTERN.finditer(text))
    total_matches = len(matches)

    if total_matches == 0:
        return article_sections  # If there are no items, returns an empty list

    for idx, match in enumerate(matches):
        start_pos = match.start()
        article_num = match.group(1)

        # Determines the end: next article or end of the text
        end_pos = matches[idx + 1].start() if idx + 1 < total_matches else len(text)

        section_text = text[start_pos:end_pos]
        cleaned_section = clean_section_text(section_text)

        article_sections.append((cleaned_section, article_num))

    return article_sections


def load_and_process_document(file_path):
    """
    Load and process a document, returning a vector store.
    """

    # Load the document
    text = TextLoader(file_path).load()[0].page_content

    # Extract sections by article
    article_sections = extract_article_sections(text)

    # Generate snippets with metadata
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

    # Creates the vector index
    return Chroma.from_documents(splits, EMBEDDING_MODEL)
