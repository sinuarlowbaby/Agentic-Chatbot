# 🤖 Agentic Chatbot

A **production-grade, multi-step agentic AI chatbot** built with **FastAPI**, **LangGraph**, and **LangChain**. The system uses a **Plan → Execute → Evaluate** loop, where an LLM autonomously breaks down user goals into steps, executes them using real-world tools (web search, data analysis, summarization), and self-evaluates results before responding.

---

## 📐 Architecture Overview

```
User Request (HTTP POST)
        │
        ▼
   FastAPI API Layer  (/api/v1/chat)
        │
        ▼
 ┌──────────────────────────────┐
 │       LangGraph Agent        │
 │                              │
 │  ┌─────────┐                 │
 │  │ Planner │ ◄── LLM (Groq) │
 │  └────┬────┘                 │
 │       │ plan_steps[]         │
 │  ┌────▼────┐                 │
 │  │Executor │ ◄── Tools       │
 │  └────┬────┘                 │
 │       │ output               │
 │  ┌────▼─────┐                │
 │  │Evaluator │ ──► loop back  │
 │  └──────────┘    or END      │
 └──────────────────────────────┘
        │
        ▼
 PostgreSQL  (Conversations, Messages,
              AgentRuns, ToolCalls)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **API Framework** | FastAPI 0.135 + Uvicorn |
| **Agent Orchestration** | LangGraph (StateGraph) |
| **LLM** | Groq — `llama-3.3-70b-versatile` |
| **LLM Framework** | LangChain + LangChain-Groq |
| **Web Search Tool** | Tavily Search API |
| **Database** | PostgreSQL via SQLAlchemy (ORM) |
| **Data Validation** | Pydantic v2 |
| **Session Management** | Cookie-based (HTTP-only, SameSite=Lax) |
| **Environment Config** | python-dotenv |

---

## 📁 Project Structure

```
Agentic-Chatbot/
├── app/
│   ├── main.py                  # FastAPI app entry point + lifespan handler
│   ├── agents/
│   │   ├── graph.py             # LangGraph StateGraph definition
│   │   ├── state.py             # AgentState TypedDict schema
│   │   └── nodes/
│   │       ├── planner.py       # Planner node — LLM decomposes goal into plan steps
│   │       ├── executor.py      # Executor node — dispatches tools per plan step
│   │       └── evaluator.py     # Evaluator node — decides to continue or stop
│   ├── api/
│   │   └── routes.py            # /api/v1/chat POST endpoint
│   ├── core/
│   │   ├── llm_client.py        # Groq LLM configuration
│   │   └── session.py           # Cookie-based session/user ID management
│   ├── db/
│   │   ├── database.py          # SQLAlchemy engine, session factory, Base
│   │   └── models.py            # ORM models: Conversation, Message, AgentRun, ToolCall
│   └── tools/
│       └── tools.py             # LangChain tools: web_search, analyze_data, summarize_data
├── memory/                      # (Reserved) Persistent memory / vector store integration
├── requirements.txt
├── .env                         # Environment variables (not committed)
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL (running locally or via Docker)
- API keys for: **Groq**, **Tavily**, **OpenAI** (optional)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Agentic-Chatbot.git
cd Agentic-Chatbot
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# LLM API Keys
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here   # optional, for future use

# Web Search
TAVILY_API_KEY=your_tavily_api_key_here

# Database
DATABASE_URL=postgresql://postgres:your_password@localhost/Agentic-chatbot
```

> ⚠️ **Never commit your `.env` file** — it is listed in `.gitignore`.

### 5. Set Up the Database

Make sure PostgreSQL is running, then create the database:

```sql
CREATE DATABASE "Agentic-chatbot";
```

The tables are created **automatically** on application startup via SQLAlchemy:

```python
models.Base.metadata.create_all(bind=engine)
```

Tables created:
- `conversations` — tracks conversation sessions per user
- `messages` — stores individual messages with role + content
- `agent_runs` — records each agent invocation with status and result
- `tool_calls` — logs every tool used during a run (name, input, output, step type)

---

## 🚀 Running the Application

```bash
python app/main.py
```

Or with Uvicorn directly:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at: **http://127.0.0.1:8000**

Interactive API docs: **http://127.0.0.1:8000/docs**

---

## 🔌 API Reference

### `GET /`

Health check.

**Response:**
```json
{"Hello": "World"}
```

---

### `POST /api/v1/chat/`

Send a message to the agentic chatbot.

**Request Body:**
```json
{
  "message": "What are the latest developments in AI agents in 2026?"
}
```

> `message` must be between 3 and 255 characters.

**Response:**
```json
{
  "response": "Here is a detailed summary of AI agent developments in 2026...",
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "steps_taken": 3
}
```

**Session:** A cookie (`session_id`) is automatically set on the first request. This persists the user identity across subsequent requests for 7 days.

---

## 🧠 How the Agent Works

The agent runs a deterministic **Plan → Execute → Evaluate** loop controlled by LangGraph:

### 1. 🗺️ Planner Node (`planner.py`)
- Receives the user's `goal` from state.
- Calls the **Groq LLM** with a structured prompt.
- Uses `PydanticOutputParser` to extract a list of `PlanStep` objects.
- Each step contains: `step` (index), `plan_step` (action type), `query` (the search/analysis query).
- Injects the plan into `AgentState.plan_steps`.

### 2. ⚡ Executor Node (`executor.py`)
- Picks the current plan step based on `current_step` index.
- Dispatches to one of three tools:
  - `web_search_tool` — Tavily real-time web search
  - `analyze_data_tool` — LLM-powered data analysis with structured JSON output
  - `summarize_data_tool` — LLM-powered summarization
- Appends tool output to `steps[]` and accumulates `intermediate_result`.

### 3. 🔍 Evaluator Node (`evaluator.py`)
- Inspects the latest execution output.
- Applies layered decision logic:
  1. **Error detected** → stop immediately, return error as final response
  2. **Max steps reached** → stop, return accumulated `intermediate_result`
  3. **Plan not finished** → continue to next step (loop back to Planner)
  4. **Output too short** (< 30 chars) → continue for better quality
  5. **Success** → stop, return output as `final_response`

### 4. 🔁 Conditional Edge (`graph.py`)
- After the Evaluator, a conditional edge checks `state["done"]` and `current_step >= max_steps`.
- If done → graph terminates (`END`).
- If not done → loops back to `planner` for the next iteration.

---

## 🗃️ Database Models

| Model | Table | Key Fields |
|---|---|---|
| `Conversation` | `conversations` | `id`, `user_id`, `title`, `created_at` |
| `Message` | `messages` | `id`, `conversation_id`, `role`, `content`, `metadata (JSONB)` |
| `AgentRun` | `agent_runs` | `id`, `conversation_id`, `message_id`, `status`, `result` |
| `ToolCall` | `tool_calls` | `id`, `run_id`, `tool_name`, `tool_input (JSONB)`, `tool_output`, `step_type` |

---

## 🔧 Tools Reference

| Tool | Description | Input |
|---|---|---|
| `web_search_tool` | Real-time web search via Tavily (max 3 results, raw content included) | `query: str` |
| `analyze_data_tool` | LLM-based analysis returning summary, key findings, recommendations, confidence score | `query: str`, `intermediate_result: str` |
| `summarize_data_tool` | LLM-based summarization returning structured summary output | `query: str` |

All tools are defined as **LangChain `@tool`-decorated functions** with Pydantic-validated output schemas.

---

## 🔐 Security Notes

- Session cookies are **HTTP-only** and **SameSite=Lax** to prevent XSS and CSRF attacks.
- API keys are loaded from `.env` — never hardcoded.
- `.env` is in `.gitignore`.
- `max_steps` hard ceiling prevents infinite agent loops.

---

## 🧪 Testing the API

You can test using `curl`:

```bash
curl -X POST http://127.0.0.1:8000/api/v1/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the latest news about LangGraph?"}'
```

Or use the built-in Swagger UI at: **http://127.0.0.1:8000/docs**

---

## 📦 Dependencies

```
fastapi==0.135.3
uvicorn==0.44.0
langchain==1.2.15
langchain-groq
langchain-tavily
langgraph
sqlalchemy
psycopg2-binary
pydantic
python-dotenv
groq==1.1.2
```

---

## 👤 Author

Built by **[Your Name]** as a production-grade agentic AI system demonstrating LangGraph orchestration, multi-tool execution, and structured LLM output parsing.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.
