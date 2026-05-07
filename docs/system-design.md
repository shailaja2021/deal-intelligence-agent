# System Design Document
# Deal Intelligence Agent
**Author:** Shailaja
**Version:** 1.0
**Status:** In Progress
**Last Updated:** 2026-04-29

---

## Architecture Overview

The Deal Intelligence Agent is a single-user, request-response web application. There is no database, no authentication layer, and no persistent state between sessions. Each request is fully self-contained: input in, battlecard out.

### ASCII Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│                    (Streamlit Cloud URL)                         │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTP  (company name as string)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     src/app.py                                  │
│                   (Streamlit UI Layer)                           │
│                                                                 │
│  - Renders text input, button, spinner, expandable sections     │
│  - Calls generate_battlecard() from agent.py                    │
│  - Renders BattleCard object as 6 expandable sections           │
│  - Offers Download as Markdown button                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │ function call (company_name: str)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     src/agent.py                                │
│                 (LangChain Agent / Orchestrator)                 │
│                                                                 │
│  1. Calls search_company() from tools.py                        │
│  2. Builds structured synthesis prompt                          │
│  3. Calls claude-sonnet-4-6 with structured output│
│  4. Validates response with Pydantic BattleCard model           │
│  5. Returns BattleCard object to app.py                         │
└─────────────┬─────────────────────────────┬─────────────────────┘
              │                             │
              ▼                             ▼
┌─────────────────────────┐   ┌─────────────────────────────────┐
│      src/tools.py        │   │    Anthropic API                │
│  (DuckDuckGo Wrapper)    │   │  (claude-sonnet-4-6)     │
│                         │   │                                 │
│  Runs 4 searches:        │   │  - Receives raw search results  │
│  1. Overview/model       │   │  - Receives structured prompt   │
│  2. Funding/investors    │   │  - Returns JSON matching        │
│  3. Tech stack           │   │    BattleCard Pydantic schema   │
│  4. News/partnerships    │   │                                 │
│                         │   │  Provider: Anthropic            │
│  Returns: combined str   │   │  Swap option: OpenAI GPT-4o     │
└─────────────┬───────────┘   └─────────────────────────────────┘
              │
              ▼
┌─────────────────────────┐   ┌─────────────────────────────────┐
│  DuckDuckGo Search API   │   │     LangSmith                   │
│  (Free, no API key)      │   │  (Eval & Observability)         │
│                         │   │                                 │
│  4 HTTP requests         │   │  - Logs every agent run         │
│  ~1 sec each             │   │  - Captures input, output,      │
│  Public web results      │   │    latency, token counts        │
│                         │   │  - Used for manual eval scoring  │
└─────────────────────────┘   └─────────────────────────────────┘

                            ┌─────────────────────────────────────┐
                            │        src/models.py                │
                            │     (Pydantic BattleCard)           │
                            │                                     │
                            │  - Defines BattleCard schema        │
                            │  - Validates Claude JSON output     │
                            │  - Provides to_markdown() method    │
                            └─────────────────────────────────────┘
```

---

## Component Breakdown

### 1. `src/app.py` — Streamlit UI Layer

**Responsibility:** All user interaction. Input collection, state management, output rendering.

**What it does:**
- Renders the page: title, subtitle, sidebar, input field, button
- On button click: calls `generate_battlecard(company_name)` from `agent.py`
- Shows a spinner with "Researching [company]... this takes about 30 seconds"
- On success: renders the returned `BattleCard` object as 6 `st.expander` sections
- Renders a `st.download_button` with the markdown output from `battlecard.to_markdown()`
- On error: renders a friendly error message with retry suggestion

**What it does NOT do:**
- No business logic
- No search calls
- No LLM calls
- No data persistence

---

### 2. `src/agent.py` — LangChain Agent / Orchestrator

**Responsibility:** The brain. Coordinates search → synthesis → validation.

**What it does:**
- Imports `search_company` from `tools.py`
- Imports `BattleCard` from `models.py`
- Initializes `ChatAnthropic` with `claude-sonnet-4-6`
- Exposes one public function: `generate_battlecard(company_name: str) -> BattleCard`
- Inside that function:
  1. Calls `search_company(company_name)` → gets raw search string
  2. Constructs a detailed synthesis prompt that includes the raw results and instructs Claude to fill each BattleCard field
  3. Uses LangChain's `with_structured_output(BattleCard)` to get a Pydantic-validated response
  4. Returns the `BattleCard` object
- Catches exceptions and returns a safe `BattleCard` with error messages rather than crashing

**LangSmith integration:**
- LangSmith tracing is enabled via environment variables (`LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_API_KEY`)
- Every call to `generate_battlecard` is automatically logged as a trace in LangSmith
- No extra code needed beyond setting the env vars — LangChain handles the rest

---

### 3. `src/tools.py` — DuckDuckGo Search Wrapper

**Responsibility:** Web research. Runs 4 targeted searches and returns combined results.

**What it does:**
- Imports `DuckDuckGoSearchRun` from `langchain_community.tools`
- Exposes one public function: `search_company(company_name: str) -> str`
- Runs 4 searches with specific query templates:
  1. `"{company_name} company overview business model"`
  2. `"{company_name} funding investors revenue 2024 2025"`
  3. `"{company_name} tech stack technology integrations"`
  4. `"{company_name} news product launch partnership 2025"`
- Sleeps 1 second between searches to reduce rate-limiting risk
- Wraps each search in try/except — failed search returns a labeled placeholder
- Returns one combined string with clear section labels between each result block

**Why 4 queries instead of 1:**
DuckDuckGo returns top-10 results for a query. A single generic query ("tell me about Salesforce") returns mixed results. Four targeted queries each optimize for a specific content type, giving Claude richer, more structured raw material to work with.

---

### 4. Anthropic claude-sonnet-4-6 — LLM Synthesis Engine

**Responsibility:** Read raw search results. Extract and structure the battlecard.

**What it does:**
- Receives a prompt containing: raw search results + battlecard schema + synthesis instructions
- Returns JSON that maps exactly to the `BattleCard` Pydantic schema
- Instructed to only use facts present in the search results
- Instructed to write "Not found" when information is absent, not to fabricate

**Why claude-sonnet-4-6:**
- Reliable structured JSON output via LangChain's `with_structured_output`
- Strong instruction-following for "do not hallucinate" constraints
- Reasonable cost per run (~$0.02–0.05 per battlecard at claude-sonnet-4-6 pricing)
- Already available to the builder; no new vendor procurement

**Vendor risk note:**
Anthropic is the LLM provider for V1. OpenAI GPT-4o is the primary swap option if Anthropic pricing, reliability, or availability becomes a constraint. The model is referenced as a single constant in `agent.py`, making a swap a one-line change.

---

### 5. `src/models.py` — Pydantic BattleCard Schema

**Responsibility:** Define and enforce the battlecard data structure.

**What it does:**
- Defines the `BattleCard` Pydantic `BaseModel` with 6 `List[str]` fields
- LangChain's `with_structured_output(BattleCard)` uses this schema to coerce Claude's response
- Provides a `to_markdown()` method that formats the battlecard as clean, downloadable markdown
- Acts as the single source of truth for battlecard structure — the schema the prompt, the LLM, and the UI all agree on

**Fields:**
| Field | What it contains |
|-------|----------------|
| `company_overview` | Company name, industry, size, HQ, business model, key products |
| `funding_growth` | Total funding, last round, investors, ARR/revenue |
| `tech_stack` | Known technologies, integrations, platforms |
| `recent_news` | Last 3 significant news items with dates, hiring trends |
| `pain_points` | Likely challenges based on stage/industry, problems your product solves |
| `pitch_angle` | How to position, suggested opening line, key objections and rebuttals |

---

### 6. LangSmith — Observability & Evals

**Responsibility:** Log every run, enable quality scoring.

**What it does:**
- Automatically captures: input (company name), output (battlecard JSON), latency, token counts, model used
- Provides a web dashboard to review individual runs
- Enables manual eval scoring: accuracy, completeness, hallucination rate per section
- In V2+: enables automated LLM-as-judge evals

**Setup:** Set `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY` in `.env` — LangChain handles the rest.

---

## Data Flow (Step by Step)

```
Step 1:  User enters "Stripe" in the Streamlit text input and clicks "Generate Battlecard"

Step 2:  app.py receives "Stripe" as a string
         → Shows spinner: "Researching Stripe... this takes about 30 seconds"
         → Calls generate_battlecard("Stripe") from agent.py

Step 3:  agent.py calls search_company("Stripe") from tools.py
         → tools.py runs 4 DuckDuckGo searches:
             Query 1: "Stripe company overview business model"
             [1 sec sleep]
             Query 2: "Stripe funding investors revenue 2024 2025"
             [1 sec sleep]
             Query 3: "Stripe tech stack technology integrations"
             [1 sec sleep]
             Query 4: "Stripe news product launch partnership 2025"
         → tools.py combines all 4 results into one labeled string
         → Returns combined string to agent.py

Step 4:  agent.py receives raw search results (~2,000–4,000 tokens)

Step 5:  agent.py builds a structured prompt:
         - Includes the raw search results
         - Includes the BattleCard JSON schema
         - Instructs: "Extract and structure the battlecard. Only use facts from results.
                       Write 'Not found' if information is absent. Do not hallucinate."

Step 6:  agent.py calls claude-sonnet-4-6 via LangChain ChatAnthropic
         with .with_structured_output(BattleCard)
         → Claude processes the prompt (~5–15 seconds)
         → Claude returns JSON matching the BattleCard schema

Step 7:  LangChain's with_structured_output() validates the JSON against BattleCard Pydantic model
         → If valid: returns BattleCard object
         → If invalid: agent.py catches the exception, returns error BattleCard

Step 8:  LangSmith automatically logs the full trace:
         input, output, latency, token counts, model

Step 9:  agent.py returns the BattleCard object to app.py

Step 10: app.py hides the spinner
          → Renders 6 st.expander sections from the BattleCard fields
          → Each expander labeled with emoji and section name
          → Each field item rendered as a bullet point

Step 11: app.py renders st.download_button
          → Clicking it downloads battlecard.to_markdown() as a .md file

Step 12: User reads the battlecard, clicks download, walks into the call prepared
```

---

## Tech Stack Decisions & Tradeoffs

| Decision | Chosen | Alternative | Why Chosen | Tradeoff |
|----------|--------|-------------|------------|----------|
| **UI framework** | Streamlit | FastAPI + React | Zero frontend code; ships in 1 day | Limited UI customization |
| **LLM** | claude-sonnet-4-6 | GPT-4o, Gemini 1.5 Pro | Best structured output; already have API access | Vendor lock-in to Anthropic |
| **Agent framework** | LangChain | Raw API calls, LlamaIndex | with_structured_output(); LangSmith integration built-in | More abstraction than needed for V1; harder to debug |
| **Web search** | DuckDuckGo (free) | SerpAPI, Bing API | Zero cost; no API key required | Rate limits; less reliable than paid APIs |
| **Structured output** | Pydantic | JSON parsing + dict | Automatic validation; clean Python objects; LangChain native | Minor learning curve |
| **Deployment** | Streamlit Cloud | Heroku, Railway, AWS | Free; 1-click deploy from GitHub; built for Streamlit | Cold starts; limited compute |
| **Evals** | LangSmith | Custom logging, Weights & Biases | Native LangChain integration; free tier sufficient | Adds external dependency |

---

## Known Limitations

### DuckDuckGo Rate Limits
DuckDuckGo does not publish rate limits, but aggressive use from a single IP (like Streamlit Cloud) may trigger temporary blocks. Mitigation: 1-second sleep between searches. If blocking becomes an issue in production, the swap to SerpAPI (paid) is a one-line change in `tools.py`.

### Public Data Only
The agent can only access publicly available information. Private company financials, internal tech stacks, and non-indexed pages are outside scope. For some small or private companies, several battlecard sections may return "Not found."

### Hallucination Risk
Claude is instructed not to fabricate, but LLMs can still confabulate plausible-sounding but wrong facts. The UI footer disclaimer and the "Not found" instruction reduce (but do not eliminate) this risk. Users should verify key facts before citing them on a call.

### Response Time Variance
Target is < 30 seconds. Actual time depends on:
- DuckDuckGo response time (variable; ~1–3 seconds per query)
- Anthropic API latency (variable; ~5–15 seconds for claude-sonnet-4-6)
- Streamlit Cloud network conditions

Under poor conditions, response could exceed 30 seconds. No hard timeout is implemented in V1.

### No Caching
Every request runs fresh searches and a fresh LLM call. Searching the same company twice costs twice the API cost. V2 should add a simple in-memory or Redis cache keyed by company name + date.

---

## Scalability Path

### V1 (Current)
- Single user, stateless
- DuckDuckGo (free, rate-limited)
- claude-sonnet-4-6
- No caching
- Streamlit Cloud (free tier)

### V2 — Scale Search
- Replace DuckDuckGo with SerpAPI for reliability at scale
- Add Redis or in-memory cache (TTL: 24 hours) to avoid duplicate searches
- Add async search calls (run 4 queries in parallel instead of sequential) to cut latency from ~12s to ~3s

### V3 — Scale Intelligence
- Add vector database (Pinecone or Chroma) to store past battlecards
- Semantic search: "companies like Stripe" returns cached intelligence
- Add streaming output to Streamlit so the battlecard appears section-by-section as Claude generates it (dramatically improves perceived performance)
- Multi-tenant: add lightweight auth (Clerk or Auth0) for team workspaces

### V4 — Platform
- Full API layer (FastAPI) behind the Streamlit UI
- Webhooks for real-time company alerts (funding round detected → push notification)
- Salesforce AppExchange listing for CRM-native access
