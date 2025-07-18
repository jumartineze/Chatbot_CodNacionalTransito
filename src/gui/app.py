import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image

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

# Asumiendo que estos módulos existen y funcionan como se espera
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
# Streamlit UI Enhancements
# -----------------------

# Configuración de la página para una mejor apariencia general
st.set_page_config(
    page_title="Chatbot Código Nacional de Tránsito",
    page_icon="🚗",
    layout="centered", # o "wide" para más espacio
    initial_sidebar_state="expanded" # La barra lateral expandida al inicio
)


# --- CSS personalizado para una experiencia "Woow" ---
st.markdown("""
<style>
body {
    background: linear-gradient(120deg, #0a2342 0%, #181c24 100%) !important;
    color: #fff !important;
}
.sidebar .sidebar-content {
    background: #142850 !important;
    color: #fff !important;
}
.banner {
    width: 100%;
    background: #142850;
    color: #fff;
    padding: 1.5rem 0.5rem 1rem 0.5rem;
    border-radius: 0 0 20px 20px;
    margin-bottom: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.18);
}
.stChatMessage {
    border-radius: 12px;
    padding: 10px 15px;
    margin-bottom: 10px;
    max-width: 80%;
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
}
.user-avatar {
    background: #1e90ff;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: inline-block;
    margin-right: 10px;
    vertical-align: middle;
    border: 2px solid #00bcd4;
}
.assistant-avatar {
    background: #23272f;
    border-radius: 50%;
    width: 38px;
    height: 38px;
    display: inline-block;
    margin-right: 10px;
    vertical-align: middle;
    border: 2px solid #3ec6e0;
}
.tool-message {
    background: #23272f;
    border-left: 4px solid #1e90ff;
    padding: 10px;
    margin-top: 8px;
    border-radius: 8px;
    font-size: 0.95em;
    color: #fff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.10);
}
.article-card {
    background: #181c24;
    border: 1px solid #1e90ff;
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 10px;
    color: #fff;
    box-shadow: 0 1px 4px rgba(0,0,0,0.10);
}
.footer {
    text-align: center;
    color: #b0c4de;
    font-size: 0.95em;
    margin-top: 2rem;
    margin-bottom: 0.5rem;
}
.stExpanderHeader {
    color: #1e90ff !important;
}
</style>
""", unsafe_allow_html=True)



# --- Banner superior con emojis y estilo llamativo ---
st.markdown('<div class="banner">', unsafe_allow_html=True)
st.markdown('''
<h1 style="margin-bottom:0.2em; font-size:2.3em;">🚦 Asistente del Código Nacional de Tránsito de Colombia 🇨🇴</h1>
<span style="font-size:1.25em; color:#005bea; font-weight:bold;">Despeja tus dudas de tránsito con IA 🤖</span><br>
<span style="font-size:1.1em; color:#3ec6e0;">Powered by LangChain & OpenAI ⚡</span>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)



st.markdown("---") # Un separador sutil

# Barra lateral para información adicional y descargos de responsabilidad
with st.sidebar:
    st.header("Acerca de este asistente ℹ️")
    st.write(
        "Este chatbot interactúa con la **Ley 769 de 2002: Código Nacional de Tránsito Terrestre** "
        "de Colombia para proporcionarte información relevante y precisa."
    )
    st.markdown("---")
    st.warning(
        "**Descargo de responsabilidad:** La información ofrecida por este asistente "
        "es de carácter **informativo** y no debe considerarse como asesoramiento legal oficial. "
        "Para asuntos legales específicos, siempre consulta a un profesional del derecho."
    )
    st.markdown("---")
    st.markdown("""
**Desarrollado por:**
<ul style='margin-top:0;margin-bottom:0;'>
  <li>Valentina Tamayo</li>
  <li>Juan Pablo Martinez</li>
  <li>Juan Manuel Sánchez</li>
</ul>
""", unsafe_allow_html=True)
    st.markdown("---")



# Inicializar el historial de chat en el estado de sesión de Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Añadir un mensaje de bienvenida inicial del asistente
    st.session_state.messages.append({"role": "assistant", "content": "¡Hola! Soy tu asistente sobre el Código Nacional de Tránsito de Colombia. ¿Tienes alguna pregunta sobre normas, multas o procedimientos de tránsito? 🛣️"})


# --- Mostrar todos los mensajes del historial de chat con avatares ---
avatar_urls = {
    # Usuario: avatar PNG neutro y moderno
    "user": "https://cdn-icons-png.flaticon.com/512/456/456212.png",
    # Asistente: mantiene el estilo actual
    "assistant": "https://cdn-icons-png.flaticon.com/512/4712/4712035.png"
}
for message in st.session_state.messages:
    avatar = avatar_urls.get(message["role"], "")
    with st.chat_message(message["role"]):
        st.markdown(f'<img src="{avatar}" class="{message["role"]}-avatar" style="display:inline;vertical-align:middle;">', unsafe_allow_html=True)
        st.markdown(message["content"])

# Aceptar la entrada del usuario
user_query = st.chat_input("Escribe tu pregunta aquí...")


if user_query:
    # Añadir el mensaje del usuario al historial de chat y mostrarlo
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(f'<img src="{avatar_urls["user"]}" class="user-avatar" style="display:inline;vertical-align:middle;">', unsafe_allow_html=True)
        st.markdown(user_query)

    # Procesar la respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("Buscando en el Código de Tránsito... 🧠"):
            full_ai_response = ""
            tool_messages_content = []
            # Animación de "escribiendo..."
            writing_placeholder = st.empty()
            for step in graph.stream(
                {"messages": [{"role": "user", "content": user_query}]},
                stream_mode="values"
            ):
                last_msg = step["messages"][-1]
                if last_msg.type == "ai":
                    full_ai_response += last_msg.content
                    writing_placeholder.markdown(f'<img src="{avatar_urls["assistant"]}" class="assistant-avatar" style="display:inline;vertical-align:middle;"> <span style="font-size:1.1em;">{full_ai_response} <span style="color:#bbb;font-size:0.9em;">⏳</span></span>', unsafe_allow_html=True)
                elif last_msg.type == "tool":
                    tool_messages_content.append(last_msg.content)
            writing_placeholder.empty()
            st.markdown(f'<img src="{avatar_urls["assistant"]}" class="assistant-avatar" style="display:inline;vertical-align:middle;">', unsafe_allow_html=True)
            st.markdown(full_ai_response)
            st.session_state.messages.append({"role": "assistant", "content": full_ai_response})
            # Mostrar los mensajes de herramientas en tarjetas dentro de un expansor
            if tool_messages_content:
                with st.expander("Ver fuentes y artículos consultados 📚"):
                    for i, tool_msg in enumerate(tool_messages_content):
                        st.markdown(f'<div class="article-card"><b>Artículo {i+1}:</b><br>{tool_msg}</div>', unsafe_allow_html=True)
                        if i < len(tool_messages_content) - 1:
                            st.markdown("---")

# --- Footer con redes sociales/contacto ---
st.markdown('''<div class="footer">
    ¿Te gustó el asistente? <a href="mailto:soporte_chat_cnt@gmail.com" target="_blank">Contáctanos</a> ·
    <a href="https://twitter.com/MinTransporteCo" target="_blank">Twitter</a> ·
    <a href="https://www.facebook.com/MinTransporteCo/" target="_blank">Facebook</a>
</div>''', unsafe_allow_html=True)
