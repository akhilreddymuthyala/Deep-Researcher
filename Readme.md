# 🔍 Deep Researcher Agent

An AI-powered research agent built with MCP (Model Context Protocol) that autonomously searches the web, scrapes content, and synthesizes detailed research reports.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                     main.py                         │
│              Entry Point / Runner                   │
└───────────────────┬─────────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │   orchestrator.py     │
        │   (Brain / LLM Loop)  │
        └───────────┬───────────┘
                    │ MCP Client calls
        ┌───────────▼────────────────────────┐
        │         MCP Servers                │
        │  ┌────────────┐ ┌──────────────┐  │
        │  │ search.py  │ │ scraper.py   │  │
        │  │ (Tavily)   │ │ (httpx+BS4)  │  │
        │  └────────────┘ └──────────────┘  │
        │        ┌──────────────────┐        │
        │        │ filesystem.py    │        │
        │        │ (save findings)  │        │
        │        └──────────────────┘        │
        └────────────────────────────────────┘
                    │
        ┌───────────▼───────────┐
        │   synthesizer.py      │
        │  (Compile Report)     │
        └───────────┬───────────┘
                    │
        ┌───────────▼───────────┐
        │   final_report.txt    │
        └───────────────────────┘
```

---

## 🔄 Agent Flow

```
User Query
    │
    ▼
┌─────────────────────────────────────────────┐
│              PHASE 1: Research              │
│                                             │
│  ┌──────────┐    ┌──────────┐    ┌───────┐  │
│  │  Search  │───▶│  Scrape  │───▶│ Save  │  │
│  │  (MCP)   │    │  (MCP)   │    │ (MCP) │  │
│  └──────────┘    └──────────┘    └───────┘  │
│       ▲                                     │
│       └──── LLM decides next action ────────┘
│                  (loop until done)          │
└─────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────┐
│             PHASE 2: Synthesize             │
│                                             │
│   Read all findings → LLM compiles report  │
└─────────────────────────────────────────────┘
    │
    ▼
 Final Report (printed + saved)
```

---

## 📁 Folder Structure

```
deep-researcher/
│
├── servers/
│   ├── search.py          ← web search MCP server
│   ├── scraper.py         ← URL scraper MCP server
│   └── filesystem.py      ← Save/read findings MCP server
│
├── agent/
│   ├── orchestrator.py    ← LLM brain — decides tool calls
│   └── synthesizer.py     ← Compiles findings into report
│
├── findings/              ← Auto-created at runtime
├── final_report.txt       ← Auto-created at runtime
├── config.py              ← API keys + settings
├── main.py                ← Entry point
├── requirements.txt       ← Dependencies
└── .env                   ← API keys (never commit this)
```

---

## ⚙️ MCP Concepts Used

```
┌─────────────────────────────────────────────────────┐
│                  MCP Protocol                       │
│                                                     │
│  Client (orchestrator.py)                           │
│       │                                             │
│       │  StdioServerParameters                      │
│       │  (spawns subprocess via stdin/stdout)       │
│       │                                             │
│       ├──▶ search-server   → tool: search_web()    │
│       ├──▶ scraper-server  → tool: scrape_url()    │
│       └──▶ fs-server       → tools: save/read/list │
│                                                     │
│  Each @mcp.tool() registers a callable for the LLM │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Setup

### 1. Clone & create virtual environment
```bash
git clone https://github.com/akhilreddymuthyala/Deep-Researcher
cd deep-researcher
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
python main.py
```

---

## 🛠️ Stack

| Layer | Tool |
|---|---|
| LLM | OpenRouter (Mistral / Gemma free models) |
| Protocol | MCP (Model Context Protocol) |
| Search | Tavily API |
| Scraping | httpx + BeautifulSoup4 |
| Storage | Local filesystem |
| Language | Python 3.10+ |

---

## 📦 Requirements

```
mcp
httpx
python-dotenv
openai
beautifulsoup4
lxml
tavily-python
```

---

## 🧠 How It Works

1. **You give a query** → `main.py` starts the agent
2. **Orchestrator connects** to 3 MCP servers via stdio
3. **LLM thinks** → decides to call `search_web`
4. **Search results return** → LLM reads them
5. **LLM calls** `scrape_url` on promising URLs
6. **LLM calls** `save_finding` to store notes
7. **Loop continues** until LLM has enough info
8. **Synthesizer reads** all saved findings
9. **Final LLM call** compiles clean report
10. **Report saved** to `final_report.txt`

---





