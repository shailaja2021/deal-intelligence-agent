# 🤖 Deal Intelligence Agent

> Type a company name. Get a structured sales battlecard in 30 seconds.

![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python)

---

## What it does

Sales reps spend 30–45 minutes researching a company before a call — or more often, skip it entirely. Deal Intelligence Agent eliminates that. Type any company name, and in about 30 seconds the AI agent searches the public web, synthesizes the results, and returns a consistent, structured battlecard covering 6 key sections: overview, funding, tech stack, recent news, pain points, and pitch angle.

---

## Try it live

**[deal-intelligence-agent-kwv74ahq5wwodfvtetpia3.streamlit.app]**

---

## Why I built this

Cold calling without research is a waste of everyone's time — the rep sounds generic, the prospect disengages, and conversion suffers. The problem isn't that reps don't want to research — it's that 30 minutes of manual Googling before every call is simply not sustainable at the volume modern sales teams operate. I built this to eliminate that tax entirely. As an AI PM building my portfolio, I also wanted to demonstrate that the best AI products aren't about impressive technology — they're about eliminating a specific, painful job that real people face every day.

---

## Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| Language | Python 3.10+ | Standard for AI apps |
| UI | Streamlit | Fastest way to ship a working UI |
| Agent framework | LangChain | Structured output + LangSmith built-in |
| Web search | DuckDuckGo (langchain-community) | Free, no API key required |
| LLM | Claude claude-sonnet-4-20250514 (Anthropic) | Best structured JSON output; strong instruction-following |
| Data validation | Pydantic v2 | Consistent battlecard schema, every run |
| Observability | LangSmith | Traces every run; enables quality evals |
| Deployment | Streamlit Cloud | Free, instant deploy from GitHub |

---

## Quickstart

**Prerequisites:** Python 3.10+, an Anthropic API key, and (optionally) a LangSmith API key.

**1. Clone the repo**
```bash
git clone https://github.com/your-username/deal-intelligence-agent.git
cd deal-intelligence-agent
```

**2. Install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add your API key**
```bash
cp .env.example .env
# Open .env and add your ANTHROPIC_API_KEY
```

**4. Run the app**
```bash
streamlit run src/app.py
```

The app opens at `http://localhost:8501`. Type any company name and click Generate Battlecard.

---

## Project Structure

```
deal-intelligence-agent/
├── docs/
│   ├── PRD.md               ← Full product requirements document
│   ├── system-design.md     ← Architecture and data flow
│   ├── sprint-plan.md       ← 3-week build plan
│   ├── roadmap.md           ← V1–V4 product roadmap
│   └── case-study.md        ← Post-launch case study (in progress)
├── src/
│   ├── models.py            ← Pydantic BattleCard schema
│   ├── tools.py             ← DuckDuckGo search wrapper (4 queries)
│   ├── agent.py             ← LangChain agent: search → synthesize → validate
│   └── app.py               ← Streamlit UI
├── requirements.txt
├── .env.example
└── CLAUDE.md                ← Build instructions (for AI coding assistant)
```

---

## Product Docs

- [PRD](docs/PRD.md) — Problem, personas, user stories, requirements, MoSCoW, RICE, OKRs
- [System Design](docs/system-design.md) — Architecture diagram, data flow, tech tradeoffs
- [Sprint Plan](docs/sprint-plan.md) — 3-week build plan with daily tasks and acceptance criteria
- [Roadmap](docs/roadmap.md) — V1 through V4 feature roadmap with metrics and dependencies
- [Case Study](docs/case-study.md) — Post-launch writeup 

---

## Built by

**Shailaja** — BSA / Product Owner | Enterprise CRM Delivery | AI Product Development


