from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, END
from langgraph.prebuilt import ToolNode, tools_condition

from .retriever_utils import get_unique_union, format_context_with_articles

import warnings
from langchain_core._api import LangChainBetaWarning

# -------------------------------------
# Suppress LangChain Beta Warnings
# -------------------------------------
warnings.filterwarnings("ignore", category=LangChainBetaWarning)

# -------------------------------------
# Main Graph Builder Function
# -------------------------------------

def build_graph(
    vector_store,
    retriever_llm=None,
    generator_llm=None
):
    """
    Builds and compiles a LangGraph-based conversational pipeline.
    Handles retrieval, tool invocation, and response generation
    for questions related to the Colombian National Traffic Code.
    """
    retriever = vector_store.as_retriever()

    # Fallback to default LLMs if not provided
    if retriever_llm is None:
        retriever_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    if generator_llm is None:
        generator_llm = ChatOpenAI(model="gpt-4", temperature=0)

    # -------------------------------------
    # Tool: Reformulate Query and Retrieve Context
    # -------------------------------------
    @tool(response_format="content_and_artifact")
    def extraer(pregunta):
        """
        Reformulates the user question into five diverse alternatives and retrieves
        unique relevant documents from a vector store.
        """
        template = (
            "Eres una IA asistente experta en el Código Nacional de Tránsito de "
            "Colombia. Tu tarea es generar cinco versiones alternativas y diversas "
            "de la pregunta dada por el usuario, con el objetivo de maximizar la "
            "recuperación de documentos relevantes de una base de datos de vectores. "
            "Cada versión debe ser semántica y sintácticamente diferente, pero "
            "mantener el sentido original de la pregunta. No inventes información ni "
            "agregues detalles que no estén en la pregunta original. No incluyas "
            "preguntas que no estén relacionadas con el Código Nacional de Tránsito "
            "de Colombia. Escribe cada pregunta alternativa en una línea diferente, "
            "sin enumerar ni listar. Pregunta original: {pregunta}"
        )
        prompt = ChatPromptTemplate.from_template(template)

        generate_queries = (
            prompt
            | retriever_llm
            | StrOutputParser()
            | (lambda x: [q for q in x.split("\n") if q.strip()])
        )

        try:
            retrieval_chain = (
                generate_queries
                | retriever.map()
                | get_unique_union
            )
            docs = retrieval_chain.invoke({"pregunta": pregunta})
            serialized = format_context_with_articles(docs)
            return serialized, docs

        except Exception as e:
            return f"Error extracting context: {e}", []

    # Register tool and bind to retriever LLM
    tools = ToolNode([extraer])
    retriever_llm_with_tools = retriever_llm.bind_tools([extraer])

    # -------------------------------------
    # Node: Tool Invocation or Response
    # -------------------------------------
    def query_or_respond(state):
        """
        Determines whether to call the retrieval tool or respond directly.
        """
        response = retriever_llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    # -------------------------------------
    # Node: Generate Final Answer
    # -------------------------------------
    def generate(state):
        """
        Generates a grounded answer based on retrieved documents and chat history.
        """
        # Collect recent tool messages (retrieved docs)
        recent_tool_messages = []
        for message in reversed(state["messages"]):
            if message.type == "tool":
                recent_tool_messages.append(message)
            else:
                break
        tool_messages = recent_tool_messages[::-1]

        docs_content = "\n\n".join(doc.content for doc in tool_messages)

        # Construct system message with context
        system_msg = (
            "Eres un asistente experto en el Código Nacional de Tránsito de Colombia. "
            "Debes responder únicamente preguntas relacionadas con el Código Nacional "
            "de Tránsito o con el contexto proporcionado. Si la pregunta no está "
            "relacionada con el Código Nacional de Tránsito, responde: "
            "\"La pregunta no está relacionada con el tema para el que fui entrenado "
            "(Código Nacional de Tránsito de Colombia) y no puedo responderla.\" "
            "Si la respuesta está en el contexto, da la respuesta más aproximada "
            "posible, citando el artículo en el que te basaste al inicio de cada "
            "parte relevante, diciendo \"Basado en el artículo X,...\". Si la respuesta "
            "no está en el contexto, responde que no sabes. Da detalles siempre que "
            "sea posible.\n\nContexto con artículos:\n\n"
            f"{docs_content}"
        )

        # Filter relevant messages for final prompt
        conversation = [
            msg for msg in state["messages"]
            if msg.type in ("human", "system")
            or (msg.type == "ai" and not msg.tool_calls)
        ]
        prompt = [SystemMessage(system_msg)] + conversation

        response = generator_llm.invoke(prompt)
        return {"messages": [response]}

    # -------------------------------------
    # Graph Construction
    # -------------------------------------
    graph = StateGraph(MessagesState)

    graph.add_node(query_or_respond)
    graph.add_node(tools)
    graph.add_node(generate)

    graph.set_entry_point("query_or_respond")
    graph.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph.add_edge("tools", "generate")
    graph.add_edge("generate", END)

    return graph.compile()
