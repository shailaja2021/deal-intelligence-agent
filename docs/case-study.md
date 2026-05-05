# Deal Intelligence Agent — Case Study

**Author:** Shailaja — BSA / Product Owner | Enterprise CRM Delivery | AI Product Development | **Status:** Complete | **Live Demo:** [Deal Intelligence Agent](https://deal-intelligence-agent-kwv74ahq5wwodfvtetpia3.streamlit.app/)

---

## The Problem

Sales reps spend 30–45 minutes researching a company before a call — or more often, skip it entirely. The problem isn't that reps don't want to research. It's that manual Googling across LinkedIn, Crunchbase, news sites, and company pages is not sustainable at the volume modern sales teams operate.

The result: generic calls, disengaged prospects, and missed conversions.

This is a workflow problem, not a motivation problem. The solution had to eliminate the research tax entirely — not make it slightly easier.

---

## The Solution

Deal Intelligence Agent is a web app where a sales rep types any company name and receives a structured, 6-section battlecard in approximately 35 seconds — with no manual research, no prompting skill required, and no login.

The 6 sections: Company Overview, Funding & Growth, Tech Stack, Recent News, Pain Points, and Pitch Angle.

Every battlecard follows the same structure every time. A rep can read it in under 2 minutes before walking into a call.

---

## Product Strategy

**The core product bet:** Consistency and automation at zero friction beats a better tool that requires effort.

Claude.ai with web search would produce richer individual outputs. But it requires the rep to know what to ask, copy-paste results, and do this consistently before every call. That friction is the product gap we solved.

**V1 scope decisions:**
- No login — barrier to adoption
- No CRM integration — complexity without validated demand
- DuckDuckGo over paid APIs — zero setup friction for demo users
- Streamlit over custom UI — ship in days, not weeks
- 6 fixed sections over flexible output — consistency is the feature

Every out-of-scope decision was deliberate. The goal was to validate one thing: does a rep find this useful enough to use before a call?

---

## Product Thinking — Jobs To Be Done

> "When I have a sales call in 30 minutes, I want to instantly know everything relevant about this company so I can walk in confident and have a meaningful conversation instead of wasting their time."

Three personas informed every decision:
- **Alex (SDR)** — makes 50+ calls/day, skips research entirely, needs zero-friction prep
- **Maya (AE)** — does research inconsistently, needs reliable quality every call
- **Sam (Sales Manager)** — wants to raise the floor on call quality across his whole team

The product serves all three with one interaction: type a name, get a card.

---

## System Design & Technical Decisions

**Architecture:**
```
User input → Streamlit UI → LangChain Agent → DuckDuckGo (4 searches) → Claude Sonnet → Pydantic validation → Rendered battlecard → LangSmith trace
```

**Key decisions and tradeoffs:**

| Decision | Choice | Why | Tradeoff |
|----------|--------|-----|----------|
| UI | Streamlit | Ship in days, no frontend engineering | Not flexible enough for enterprise V2 |
| Orchestration | LangChain | Tool chaining + LangSmith built-in | Adds complexity vs direct API calls |
| Search | DuckDuckGo | Free, no API key, zero friction | Rate limits, less reliable than SerpAPI |
| LLM | Claude Sonnet | Best structured JSON output consistency | Cost per call |
| Validation | Pydantic | Enforces consistent schema every run | None for V1 |
| Observability | LangSmith | Traces every run, enables eval scoring | Free tier limits at scale |
| Deployment | Streamlit Cloud | Free, instant deploy from GitHub | No SLA, shared infrastructure |

**Why Pydantic was a product decision, not just a technical one:**
Without schema enforcement, Claude might return 5 sections one run and 7 another. Pydantic is the quality gate between the LLM and the UI — it guarantees the battlecard format is identical every time.

---

## Evaluation Process

Ran 3 rounds of evaluation across 20 companies to measure and improve output quality.

**Dimensions scored:** Accuracy, Completeness, Hallucination (each 0 / 0.5 / 1). Target: all dimensions above 0.8.

### Eval Run 1 — Baseline (20 companies)

| Dimension | Score | Pass? |
|-----------|-------|-------|
| Accuracy | 0.78 | Borderline |
| Completeness | 0.68 | No |
| Hallucination | 0.73 | No |
| Avg Latency | 33.7s | Pass |

**Top 3 failure patterns:**
1. Completeness collapsed for private and acquired companies — Loom's $975M Atlassian acquisition was missed entirely
2. Unverified numeric stats presented as facts — appeared in 9 of 20 cards
3. News section returned stale results — Workday's most recent news was from 2020

### Prompt Tuning — v1.1 (5 changes)

1. Acquisition hard check — must state acquirer, date, and price or explicitly mark Not found
2. Confidence tags — every number tagged [confirmed], [estimated], or [inferred] with source
3. Recency gate — news must include month and year; fallback label if nothing from past 6 months
4. HQ required — always state HQ city, write "HQ: Not found" rather than omitting
5. Private company flag — add [limited public data] when funding data is thin

### Eval Run 2 — 5 worst companies rerun

Average score on these 5 companies improved from **60% → 80%**.

Outreach went from almost empty funding section to fully populated with sourced data. Snowflake had a complete turnaround — all news dated, all stats tagged. Confidence tagging was the single most impactful change.

### Eval Run 3 — v1.2 fixes (Loom and Workday)

- **Workday:** Fully resolved — 3.0/3. News label bug fixed, dated items now present.
- **Loom (local testing):** Scored 1.5/3 locally — acquisition price and date not returned by DuckDuckGo on local machine.

### Live Deployment Verification

Tested Loom on the live Streamlit Cloud deployment — acquisition price ($975M), date (Oct 2023), and Atlassian context all returned correctly. The local gap was a network environment limitation, not a product limitation. DuckDuckGo returns richer results from Streamlit Cloud's infrastructure than from a local machine.

**Live latency: 29 seconds** — faster than local testing (49s) due to Streamlit Cloud's infrastructure.

**MVP verdict:** All prompt and logic issues fully resolved. Live deployment confirmed working correctly for acquired companies. Product is ready for portfolio demo.

---

## Prompt Engineering Techniques

| Technique | Used | Purpose |
|-----------|------|---------|
| Role prompting | ✅ | "You are a sales intelligence analyst" — improves output quality |
| Structured output / schema prompting | ✅ | Pydantic schema enforces consistent 6-section format every run |
| Explicit rules-based constraints | ✅ | 10 CRITICAL RULES override Claude's default behaviour |
| Retrieval grounding | ✅ | Claude only uses search results — reduces hallucination |
| Section-by-section instruction | ✅ | Separate instructions per section = consistent output per section |
| Confidence tagging | ✅ | [confirmed] / [estimated] / [inferred] forces fact reliability evaluation |
| Few-shot examples | ❌ | Most impactful unused technique — planned for V2 |
| Chain of Thought (CoT) | ❌ | Not needed — task is extraction, not multi-step reasoning |
| Self-consistency | ❌ | Not relevant given latency constraints |

---

## Tech Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| UI | Streamlit | Web interface — input, output, download |
| Orchestration | LangChain | Agent pipeline — search → synthesise → validate |
| Search | DuckDuckGo (langchain-community) | 4 targeted web searches per company |
| LLM | Claude Sonnet (Anthropic API) | Synthesis and structured output |
| Validation | Pydantic v2 | Enforces consistent 6-section battlecard schema |
| Observability | LangSmith | Traces every run, enables eval scoring |
| Version control | GitHub | Source of truth, triggers Streamlit redeploy |
| Deployment | Streamlit Cloud | Free public hosting, continuous deployment |

---

## Product Metrics

**North Star:** Battlecards generated per week

**Leading indicators** (early signals of success):
- Session starts per day
- Average latency per run
- Agent error rate (failed runs vs successful)
- LangSmith eval scores (output quality over time)

**Lagging indicators** (confirm success after the fact):
- Battlecards generated per week — North Star
- Repeat usage rate — did the same user return?
- Download rate — did reps save the battlecard?

**What is measurable now:**
LangSmith automatically captures total runs, latency, and error rate. Streamlit Cloud provides basic session and visitor counts.

**What requires V2 instrumentation:**
Repeat usage and download rate require user-level tracking — not possible in V1 without login. Download button clicks would need explicit event instrumentation.

V1 has intentionally minimal tracking — no login means no user-level analytics. The North Star (battlecards generated per week) is captured automatically via LangSmith. User behaviour metrics are planned for V2 alongside CRM integration.

---

## Results & Learnings

**What worked:**
- Pydantic schema enforcement — the most underrated decision. Consistent output was never a problem.
- Prompt iteration loop — structured eval → identify failure patterns → targeted fix → rerun. Scores improved measurably across 3 rounds.
- LangSmith observability — without traces, the unverified stats problem would have been invisible.
- DuckDuckGo for V1 — zero friction validated the concept without any setup barrier.

**What I learned:**
- AI products fail differently than traditional software. An app can run without errors and still produce actively misleading output (the Loom card). Observability is not optional.
- Prompt engineering is product management. Every rule added to the prompt was a product decision with a tradeoff — more accuracy, more latency, more complexity.
- The evaluation loop is the product process. Ship, measure, identify, fix, measure again. Same as any product iteration — the artifact being improved happens to be a prompt.
- Environment configuration is not a one-time setup. Local `.env` and Streamlit Secrets are completely separate. Staging caught this before production.

---

## What I'd Do Differently

1. **Add a 5th dedicated acquisition search query from the start** — the Loom gap was predictable for any acquired company. One targeted query would have caught it in Run 1.
2. **Pin exact dependency versions in requirements.txt** — using `>=` works for a demo but creates redeployment risk if a library releases a breaking update.
3. **Run the eval before sharing the live URL** — the first 20-company baseline revealed issues a user would notice. Eval first, share after.
4. **SerpAPI from V1 for a paid product** — DuckDuckGo is the right call for a free demo. For any production deployment with real users, the reliability and structured data from SerpAPI justifies the cost immediately.

---

## Enterprise Path

V1 validates the core hypothesis. Enterprise deployment would require:
- **Auth:** SSO via Okta or Azure AD
- **Search:** SerpAPI or licensed data sources (ZoomInfo, Clearbit)
- **Hosting:** AWS/Azure with containerised deployment (Docker + Kubernetes)
- **CRM integration:** Salesforce / HubSpot push — the highest-value V2 feature for sales teams
- **Eval pipeline:** Automated LLM-as-evaluator replacing manual scoring at scale

---

## Links

- Live App: [Deal Intelligence Agent](https://deal-intelligence-agent-kwv74ahq5wwodfvtetpia3.streamlit.app/)
- GitHub: [REPO LINK]
- PRD: [DOCS LINK]
