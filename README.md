# 🛣️ Chatbot_CodNacionalTransito

**Conversational AI assistant for answering legal questions based on the _Código Nacional de Tránsito_ (Colombian National Traffic Code).**
This project combines semantic search, large language models (LLMs), and article-level retrieval to deliver reliable, cited legal responses.

---

## 🚀 Features

- 🔎 **Semantic Search** — Retrieves relevant legal articles using vector embeddings.
- 🤖 **LLM-Powered Responses** — Generates detailed, context-aware answers using OpenAI models.
- 📚 **Article Citation** — Cites specific articles used to build each answer.
- 🖥️ **Web Interface (Streamlit)** — Easy-to-use app for real-time interaction.
- ⚙️ **Modular Pipeline** — Components are easily adaptable for other legal domains or documents.

---

## 📁 Project Structure

```

Chatbot\_CodNacionalTransito/
├── data/                     # Raw and processed legal texts
├── src/
│   ├── document\_loader.py   # Loads and vectorizes documents
│   ├── graph\_wrapper.py     # Core chatbot pipeline logic
│   ├── retriever\_utils.py   # Retrieval & formatting utilities
│   ├── preprocess\_text.py   # Text cleaning and prep scripts
│   └── gui/
│       ├── app.py           # Streamlit-based web app
│       └── components.py    # Optional UI components
├── main.py                  # Entry point to launch the chatbot
├── setup.py                 # Project setup (Python dependencies)
├── setup.bat                # Windows setup script
├── setup.sh                 # Mac/Linux setup script
├── README.md                # Project documentation

````

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Chatbot_CodNacionalTransito.git
cd Chatbot_CodNacionalTransito
````

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

**On Windows:**

```bash
./setup.bat
```

**On Mac/Linux:**

```bash
bash setup.sh
```

### 4. Configure environment variables

Create a `.env` file.

Fill in your API keys inside `.env`:

```dotenv
OPENAI_API_KEY=your-openai-key
LANGCHAIN_API_KEY=your-langsmith-key
LANGCHAIN_PROJECT=MiProyectoLLM
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

---

## 💬 Usage

To launch the chatbot web app:

```bash
python main.py
```

---

## 🧪 Example Questions

You can try asking the assistant:

* *"¿Puede una moto circular por la línea discontinua amarilla entre los carros?"*
* *"¿Qué puedo hacer si un agente de tránsito me multa injustamente?"*
* *"¿Quién regula las normas de tránsito en Colombia?"*

---

## 📌 Notes

* This chatbot is focused **exclusively** on the Colombian National Traffic Code.
* All responses are grounded in the actual legal text and **cite specific articles** used.
* Ensure your `.env` file is properly configured and that the legal documents have been preprocessed for optimal results.

---

## 👤 Authors

**Valentina Tamayo Guarín**
[vatamayog@unal.edu.co](mailto:vatamayog@unal.edu.co)

**Juan Manuel Sánchez Restrepo**
[jsanchezre@unal.edu.co](mailto:jsanchezre@unal.edu.co)

**Juan Pablo Martínez Echavarría**
[jumartineze@unal.edu.co](mailto:jumartineze@unal.edu.co)
