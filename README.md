# 🌐 Learn GenAI Tools & Agents

A hands-on repository exploring **Generative AI**, **LangChain (LCEL)**, **Custom Tool Calling**, and **Interactive AI Agents with Human-in-the-Loop** using Google Gemini, OpenWeatherMap, and Tavily Search.

---

## 📌 Project Overview

This repository demonstrates practical patterns in modern LLM application development, transitioning from core LangChain Expression Language (LCEL) primitives to interactive multi-tool agents and Streamlit web applications:

1. **LCEL Fundamentals**: Sequential chains, parallel execution, and state pass-throughs.
2. **Tool Calling & Integration**: Binding custom Python tools and 3rd-party APIs (OpenWeatherMap, Tavily) to Gemini models.
3. **Interactive Agents & HITL**: Multi-step AI agents with human-in-the-loop approval before executing real-world actions.
4. **Streamlit User Interfaces**: Interactive dashboards for AI News Summarization and City Intelligence.

---

## 🗂️ Project Structure

```text
learn-genai-tool/
├── Agent/
│   ├── app.py               # Streamlit UI: Full City Intelligence System (Weather & News)
│   ├── agents.py            # CLI Agent: Human-in-the-Loop tool confirmation loop
│   ├── newsupdate.py        # Custom LangChain tool for Tavily News API
│   ├── weatherTool.py       # Custom LangChain tool for OpenWeatherMap Geo & Weather API
│   └── create_agent.py      # Agent helper / initialization script
├── custometool.py           # Introduction to LangChain @tool decorator
├── toolcalling.py           # Single-tool calling workflow with Gemini & manual dispatch
├── sequence.py              # LangChain LCEL sequential chain (prompt | model | parser)
├── parallelrunable.py       # RunnableParallel & RunnableLambda execution
├── runnablepassthrough.py   # RunnablePassthrough pipeline with code generation & explanation
├── news-summarizer.py       # CLI-based Tavily news search & Gemini summarizer
├── new-ui.py                # Streamlit UI for the AI News Summarizer
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🚀 Key Modules & Features

### 1. 🤖 City Intelligence System (`Agent/`)
- **[app.py](file:///d:/python/tool/Agent/app.py)**: A dark-themed Streamlit dashboard integrating weather updates and real-time news with tool-call inspection.
- **[agents.py](file:///d:/python/tool/Agent/agents.py)**: CLI-based conversational agent with **Human-in-the-Loop (HITL)** approval. The assistant requests permission (`Approve (yes/no)?`) before triggering tool invocations.
- **[weatherTool.py](file:///d:/python/tool/Agent/weatherTool.py)**: Resolves coordinates via OpenWeatherMap Direct Geocoding API and retrieves temperatures, humidity, wind speed, conditions, and local timestamps.
- **[newsupdate.py](file:///d:/python/tool/Agent/newsupdate.py)**: Uses Tavily Client to retrieve top weekly news articles for any given city.

### 2. 📰 AI News Summarizer (`new-ui.py` & `news-summarizer.py`)
- Takes user query topics, retrieves real-time articles via Tavily Search, and produces structured bullet-point summaries via Google Gemini.
- Features configurable search depth via a slider in the Streamlit interface.

### 3. ⛓️ LangChain LCEL Concepts
- **[sequence.py](file:///d:/python/tool/sequence.py)**: Simple pipeline composition using the pipe `|` operator (`ChatPromptTemplate | ChatGoogleGenerativeAI | StrOutputParser`).
- **[parallelrunable.py](file:///d:/python/tool/parallelrunable.py)**: Executes short and detailed explanations concurrently via `RunnableParallel`.
- **[runnablepassthrough.py](file:///d:/python/tool/runnablepassthrough.py)**: Demonstrates piping generated code into an explanation prompt while preserving the original output with `RunnablePassthrough`.
- **[toolcalling.py](file:///d:/python/tool/toolcalling.py) & [custometool.py](file:///d:/python/tool/custometool.py)**: Custom `@tool` creation, schema generation, argument binding, and response parsing.

---

## 🛠️ Tech Stack & Dependencies

- **Language**: Python 3.10+
- **LLM**: Google Gemini (`gemini-3.5-flash-lite` via `langchain-google-genai`)
- **Orchestration**: `langchain`, `langchain-core`, `langchain-community`
- **Search & Weather APIs**: `tavily-python`, `requests` (OpenWeatherMap)
- **Web UI**: `streamlit`
- **Terminal UI**: `rich`
- **Config & Env**: `python-dotenv`

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Masood-Abbas/learn-genai-tool.git
cd learn-genai-tool
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install streamlit tavily-python rich
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_google_gemini_api_key
OPENWEATHER_API_KEY=your_openweathermap_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## 💻 Running the Applications

### Run the City Intelligence Streamlit App
```bash
streamlit run Agent/app.py
```

### Run the City Intelligence CLI Agent (with Human Approval)
```bash
python Agent/agents.py
```

### Run the News Summarizer UI
```bash
streamlit run new-ui.py
```

### Run LCEL Examples
```bash
python sequence.py
python parallelrunable.py
python runnablepassthrough.py
python toolcalling.py
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
