# Startup Intelligence Agent

> Autonomous market researcher + pitch writer + living knowledge base for startups. Built on LangGraph, RAG, and production-grade data pipelines.

---

## ✨ What it does (at a glance)

* **Scan a domain** and ingest credible sources (news, blogs, APIs, filings, GitHub, job boards) for any startup market or company.
* **Map the landscape**: trends, competitors, differentiators, growth signals, and risks — all with sources & timestamps.
* **Generate investor-ready artifacts**: concise one-pager, 3–5 slide deck draft, elevator pitch, and tailored investor outreach.
* **Persist verified knowledge** in a searchable store (vector DB + graph) with provenance, confidence scores, and refresh schedules.
* **(Optional) Always-on monitoring**: alerts when funding rounds, layoffs, notable hires, or regulatory shifts occur.

> **Users get**: a clean Market Report, Competitor Map, Investor-Ready Pitch, a reusable Knowledge Base, and Real‑Time Alerts.

---

## 🏗️ Architecture Overview

```
           +------------------+          +-----------------------+
Sources -->| Ingestion Layer  |--docs--> | Preprocess & Parse    |--->
 (APIs,    | (crawler, APIs)  |          | (clean, dedupe, OCR)  |
  RSS,     +------------------+          +-----------------------+
 filings)                                                  |
                                                 +--------v---------+
                                                 | NER & Relation   |
                                                 | Extraction       |
                                                 +--------+---------+
                                                          |
                                       +------------------v------------------+
                                       | Knowledge Layer                     |
                                       |  • Vector DB (semantic search)      |
                                       |  • Knowledge Graph (entities/edges) |
                                       +------------------+------------------+
                                                          |
                               +--------------------------v-------------------+
                               | LangGraph Orchestration (flows & guards)     |
                               |  • summarize • verify • score • persist      |
                               +--------------------------+-------------------+
                                                          |
                           +------------------------------v------------------+
                           | Outputs & Interfaces                              |
                           |  • Reports • Pitch Deck • Alerts • REST/CLI/UI   |
                           +--------------------------------------------------+
```


---

## 🔑 Features

* **Domain Scan**: targeted crawl + API pulls; dedupe & normalize.
* **Competitor Mapping**: similarity, feature overlap, funding, traction proxies.
* **Trend Detection**: time‑series signals from news/jobs/code activity/regulatory notes.
* **Pitch Generation**: one‑pager, elevator pitch, and slide outline (with speaker notes).
* **Financial Sketch**: quick TAM/SAM/SOM, unit economics scaffold, pricing hypotheses.
* **Investor Matching** (optional): align by stage, thesis, geography; draft personalized outreach.
* **Knowledge Persistence**: vector search + graph queries; snapshots with versioning.
* **Provenance & Confidence**: per‑fact source list, extraction time, and reliability score.
* **Continuous Monitoring** (optional): webhook/RSS jobs for funding, patents, layoffs, leadership moves.

---

## 🚀 Quickstart

### Prerequisites

* Python **3.11+**
* API keys for your chosen model & search/news providers (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `TAVILY_API_KEY` or similar)
* A vector DB (local **Chroma** by default; Pinecone/Weaviate/Milvus supported via env)

### Installation

```bash
# clone
git clone https://github.com/<you>/startup-intelligence-agent.git
cd startup-intelligence-agent

# create env
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)

# install
pip install -U pip
pip install -r requirements.txt
```

### Configure environment

Create `.env` in repo root:

```dotenv
# LLMs
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...

# Search / news (pick your stack)
TAVILY_API_KEY=...
NEWS_API_KEY=...

# Storage
VECTOR_DB=chroma
VECTOR_DB_DIR=.cache/chroma
GRAPH_DB_URL=bolt://localhost:7687   # if using Neo4j (optional)

```
---

## 🔒 Grounding, QA & Governance

* **Provenance first**: every key claim links to source URL + extraction time.
* **Verification node**: re‑queries KB & external APIs; below‑threshold facts are flagged.
* **Confidence model**: combines extraction confidence and source reliability.
* **Compliance**: respect robots.txt & site ToS; prefer official/licensed APIs; store PII securely.

---

## 🤝 Contributing

PRs welcome! Please open an issue with context and expected behavior before large changes. Run tests with `pytest` and include coverage for new nodes/flows.

