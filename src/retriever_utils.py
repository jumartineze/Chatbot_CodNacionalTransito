from langchain.load import dumps, loads

# ----------------------------
# Helper Functions
# ----------------------------

def get_unique_union(documents: list[list]):
    """
    Returns a list of unique documents from a nested list structure,
    using the combination of page content and article number as the uniqueness key.
    """
    # Flatten the nested list and serialize each document using content + article number
    flattened_docs = [
        dumps(doc.page_content + doc.metadata.get("source_article", ""))
        for sublist in documents
        for doc in sublist
    ]

    # Remove duplicates by converting to a set
    unique_docs = list(set(flattened_docs))

    loaded_unique_docs = []
    for doc_str in unique_docs:
        doc = loads(doc_str)
        # Find original document to preserve metadata
        original_doc = next(
            (
                d for sublist in documents
                for d in sublist
                if d.page_content + d.metadata.get("source_article", "") == doc
            ),
            None
        )
        if original_doc:
            loaded_unique_docs.append(original_doc)

    return loaded_unique_docs


def format_context_with_articles(docs):
    """
    Formats a list of documents by prepending the article number
    to each document’s content for clearer display.

    Returns:
        A single formatted string combining all documents.
    """
    formatted_contexts = []
    for doc in docs:
        article_num = doc.metadata.get("source_article", "N/A")
        formatted_contexts.append(f"[Artículo {article_num}] {doc.page_content}")

    return "\n\n".join(formatted_contexts)
