# Product Requirements Document
# Deal Intelligence Agent
**Author:** Shailaja
**Version:** 1.0
**Status:** In Progress
**Last Updated:** 2026-04-29

---

## Executive Summary

Deal Intelligence Agent is an AI-powered sales research tool that transforms a company name into a structured, six-section battlecard in under 30 seconds. It eliminates the 30–45 minute manual research burden that causes most sales reps to skip pre-call preparation entirely. Built for B2B SaaS sales teams, it uses LangChain, Claude claude-sonnet-4-20250514, and public web data to deliver consistent, actionable intelligence before every call. V1 is free, public, and requires no login or setup — removing every adoption barrier.

---

## Problem Statement

### Job To Be Done (JTBD)

> "When I have a sales call in 30 minutes, I want to instantly know everything relevant about this company so I can walk in confident and have a meaningful conversation instead of wasting their time."

### The As-Is Process (Manual Research)

Sales reps today must piece together company intelligence from 5–8 different sources: the company website, LinkedIn, Crunchbase, G2, TechCrunch, Google News, and the CRM. This process takes 30–45 minutes per company when done well — which is why most reps skip it entirely.

**Current pain points:**
- **Time cost:** 30–45 mins per account, unsustainable at scale (50+ calls/day for SDRs)
- **Inconsistency:** Different reps research differently; no standard format across the team
- **Incompleteness:** Reps miss funding news, leadership changes, or competitive signals that matter
- **Skip rate:** Most reps walk into calls cold, damaging conversion rates and brand perception
- **No leverage:** Research done for one call is lost — not reused or shared across the team

### The To-Be Process (With Deal Intelligence Agent)

1. Rep types a company name
2. Agent searches the web across 4 targeted queries in parallel
3. Claude synthesizes raw results into a structured 6-section battlecard
4. Rep reads a consistent, formatted battlecard in under 30 seconds
5. Rep walks into the call confident, informed, and ready

---

## Target Users & Personas

### Alex — SDR (22–25)
**Role:** Sales Development Representative at a B2B SaaS company
**Volume:** Makes 50+ cold calls per day
**Pain:** Zero time for research. Skips it entirely. Walks in blind, which tanks conversion rates and makes calls feel generic to prospects.
**Goal:** Wants to sound informed on every call without spending any time preparing.
**Success looks like:** Can say "I saw you just raised a Series B — congrats. That's actually why I'm calling..." instead of "So, tell me about your business."
**Adoption barrier:** Tool must be zero-friction. Any login, setup, or credit card = won't use it.

### Maya — Account Executive (28–35)
**Role:** AE managing a book of 50–100 accounts at a mid-market SaaS company
**Volume:** 8–12 calls per day, more complex deals, longer sales cycles
**Pain:** Does research but inconsistently. Sometimes thorough, sometimes rushed. Quality varies by how much time she has.
**Goal:** Wants consistent research quality on every call, not just when she has time.
**Success looks like:** Every call prep takes the same 30 seconds and produces the same reliable depth of intelligence.
**Adoption barrier:** Tool must give her the pain points and pitch angle — not just raw facts she could Google herself.

### Sam — Sales Manager (35–45)
**Role:** VP of Sales or Sales Manager overseeing a team of 5–15 reps
**Volume:** Doesn't make calls himself; watches call recordings and reviews pipeline
**Pain:** Huge variance in call quality across the team. Some reps research, most don't. Can't enforce a standard.
**Goal:** Raise the floor on call quality across his whole team without adding overhead to his reps.
**Success looks like:** Every rep on his team walks into every call with the same baseline of intelligence. Call quality variance drops. Conversion rates rise.
**Adoption barrier:** Needs to see the team actually use it — adoption depends on zero friction for reps.

---

## User Stories

1. **As Alex (SDR),** I want to get a full company overview in under 30 seconds so that I can sound informed even when I have no time to research before a call.

2. **As Alex (SDR),** I want to know a company's recent news and trigger events so that I can open the call with a relevant, personalized hook instead of a generic pitch.

3. **As Maya (AE),** I want to see a suggested pitch angle and opening line so that I can tailor my positioning to this specific company's situation rather than using a generic script.

4. **As Maya (AE),** I want to see likely pain points for the company so that I can anticipate their objections and address them proactively.

5. **As Maya (AE),** I want to download the battlecard as a markdown file so that I can save it in my notes or CRM before the call.

6. **As Sam (Sales Manager),** I want all battlecards to follow the same consistent format so that I can review call prep across my team and ensure a quality floor.

7. **As Sam (Sales Manager),** I want the tool to be publicly accessible with no login so that I can share it with my team and see immediate adoption without an IT procurement process.

8. **As any user,** I want the tool to clearly flag when information was not found (rather than making it up) so that I can trust the facts in the battlecard and not be misled.

9. **As any user,** I want a loading indicator that tells me the research is in progress so that I know the tool is working and don't close the tab thinking it froze.

10. **As any user,** I want a friendly error message if the company is not found or the search fails so that I know what happened and can try again without frustration.

---

## Functional Requirements

1. The app shall accept a plain text company name as the only required input.
2. The app shall trigger a web research process when the user clicks "Generate Battlecard."
3. The agent shall run exactly 4 targeted DuckDuckGo searches covering: company overview, funding/investors, tech stack, and recent news.
4. The agent shall pass all search results to Claude claude-sonnet-4-20250514 with a structured synthesis prompt.
5. Claude shall return a response that maps exactly to the 6-section BattleCard Pydantic schema.
6. The Pydantic model shall validate the response structure before rendering.
7. The UI shall display the battlecard in 6 labeled, expandable sections with section-specific emojis.
8. The sections shall be: Company Overview, Funding & Growth, Tech Stack, Recent News & Triggers, Pain Points, Pitch Angle.
9. The UI shall show a loading spinner with a message like "Researching [company]... this takes about 30 seconds" while processing.
10. The app shall offer a "Download as Markdown" button after the battlecard is rendered.
11. If a search fails, the agent shall return "Not found" for that section rather than fabricating data.
12. If the API call fails, the app shall display a user-friendly error message with a retry suggestion.
13. The app shall complete the full research-to-battlecard flow in under 30 seconds under normal conditions.
14. The app shall log every run to LangSmith for evaluation and monitoring.
15. The sidebar shall explain what the tool does and include a link to the GitHub repo.
16. The footer shall display a disclaimer: "AI-generated research. Verify key facts before your call."

---

## Non-Functional Requirements

| Category | Requirement |
|----------|-------------|
| **Performance** | Battlecard generation completes in < 30 seconds for 95% of requests under normal load |
| **Reliability** | App remains available during Streamlit Cloud uptime; graceful error handling for API failures |
| **Security** | No PII stored or logged; no user accounts; no session data persisted between requests |
| **Privacy** | Only publicly available web data used; no scraping behind authenticated pages |
| **Accessibility** | Readable contrast ratios; clean layout readable on desktop browsers |
| **Cost** | Zero cost to end user; API cost per run < $0.05 using Claude claude-sonnet-4-20250514 |
| **Maintainability** | All code commented; modular structure allows swapping LLM or search tool independently |
| **Portability** | Runs locally with `streamlit run src/app.py` after pip install; no Docker required |

---

## Out of Scope for V1

The following will NOT be built in V1:

- User accounts or authentication of any kind
- CRM integration (Salesforce, HubSpot)
- Team workspace or shared battlecard libraries
- Slack or email integration
- Mobile app or responsive mobile design
- Paid tiers or feature gating
- Real-time company alerts or monitoring
- Chrome extension
- Multi-company comparison
- Post-call AI scoring or coaching
- API access for third-party integrations

---

## MoSCoW Prioritization

| Priority | Feature |
|----------|---------|
| **Must Have** | Company name text input |
| **Must Have** | 4-query DuckDuckGo web research |
| **Must Have** | Claude claude-sonnet-4-20250514 structured synthesis |
| **Must Have** | Pydantic-validated 6-section battlecard output |
| **Must Have** | Battlecard rendered in UI with section headers |
| **Must Have** | Response in < 30 seconds |
| **Must Have** | Free, public, no login required |
| **Must Have** | Deployed on Streamlit Cloud |
| **Must Have** | "Not found" instead of hallucination when data unavailable |
| **Should Have** | Download as Markdown button |
| **Should Have** | Loading spinner with company name |
| **Should Have** | LangSmith tracing and eval logging |
| **Should Have** | Friendly error messages for API failures |
| **Should Have** | Sidebar with tool description and GitHub link |
| **Could Have** | Section-level copy buttons |
| **Could Have** | Search history (last 5 companies, session only) |
| **Could Have** | Confidence score or source citations per section |
| **Won't Have (V1)** | CRM integration |
| **Won't Have (V1)** | User accounts |
| **Won't Have (V1)** | Team workspace |
| **Won't Have (V1)** | Slack/email integration |
| **Won't Have (V1)** | Mobile app |

---

## RICE Scoring

| Feature | Reach (1–10) | Impact (1–3) | Confidence (%) | Effort (weeks) | RICE Score |
|---------|-------------|--------------|----------------|----------------|------------|
| 6-section battlecard output | 10 | 3 | 95% | 1.0 | 28.5 |
| Sub-30 second response time | 10 | 3 | 85% | 0.5 | 51.0 |
| No login / free access | 10 | 3 | 100% | 0.1 | 300.0 |
| Download as Markdown | 7 | 2 | 95% | 0.2 | 66.5 |
| LangSmith tracing | 4 | 2 | 90% | 0.5 | 14.4 |
| Friendly error handling | 8 | 2 | 90% | 0.3 | 48.0 |

*RICE = (Reach × Impact × Confidence) / Effort*

---

## Success Metrics & OKRs

### North Star Metric
**Battlecards generated per week** — the single number that proves the tool is being used and delivering value.

### OKRs for V1 Launch

**Objective:** Ship a working, publicly deployed battlecard generator that real sales reps would actually use.

| Key Result | Target | How Measured |
|------------|--------|-------------|
| KR1: Battlecards generated in first 2 weeks post-launch | ≥ 50 | LangSmith run count |
| KR2: Average response time | < 30 seconds | LangSmith trace duration |
| KR3: LangSmith eval score (accuracy + completeness) | > 80% | Manual eval on 20 companies |
| KR4: Battlecard fields with "Not found" (hallucination proxy) | < 15% of fields | Manual review |
| KR5: GitHub stars in first month | ≥ 25 | GitHub |

---

## Risk Summary

| Risk | Type | Likelihood | Impact | Mitigation |
|------|------|-----------|--------|------------|
| DuckDuckGo rate limiting blocks searches | Technical | Medium | High | 1-second sleep between searches; try/except fallback |
| Claude returns malformed JSON (fails Pydantic validation) | Technical | Low | Medium | Error handling returns safe BattleCard with error messages |
| Search results contain outdated or inaccurate data | Technical | High | Medium | Disclaimer in UI; prompt instructs "only use facts from results" |
| Anthropic API downtime or latency spike | Vendor | Low | High | User-facing timeout message; retry suggestion |
| DuckDuckGo blocks Streamlit Cloud IPs | Technical | Medium | High | Fallback to DDGS library; document workaround |
| Users misuse battlecard as verified fact sheet | Ethical | Medium | Medium | Footer disclaimer; "Not found" instead of hallucination |
| Low adoption due to LinkedIn-only distribution | Market | Medium | Medium | Share in sales Slack communities, Product Hunt |
| Anthropic deprecates claude-sonnet-4-20250514 | Vendor | Low | Low | Model name is a single constant — easy to swap |

---

## Competitive Analysis

| Product | What it does | Strength | Weakness vs. Deal Intelligence Agent |
|---------|-------------|----------|--------------------------------------|
| **ZoomInfo** | B2B data platform with company/contact records | Massive database, CRM integration | $15K+/year; no AI synthesis; static data |
| **Apollo.io** | Sales intelligence + sequencing | Affordable, large contact database | No AI battlecard; requires login and subscription |
| **Clay** | Data enrichment + workflow automation | Highly customizable enrichment | Complex to set up; expensive; not a 30-second tool |
| **Gong** | Revenue intelligence and call recording | Post-call AI coaching | No pre-call research; no battlecard output |
| **ChatGPT (manual)** | General-purpose LLM | Flexible, capable | No structured output; no web search in free tier; no consistent format; requires prompt engineering |
| **Deal Intelligence Agent** | AI agent → structured battlecard in 30 sec | Free, instant, structured, no login | Early stage; public data only; no CRM integration yet |

---

## Open Questions

1. **Rate limiting:** How aggressively does DuckDuckGo rate-limit requests from Streamlit Cloud IPs? Will we need to implement exponential backoff or switch to DDGS (the underlying library) for V1?

2. **Eval methodology:** How do we score battlecard quality programmatically in LangSmith? Should we use Claude itself as an evaluator (LLM-as-judge), or rely on manual spot-checking for V1?

3. **Hallucination threshold:** What is an acceptable rate of "Not found" vs. fabricated data? Should we surface a confidence score per section to help users calibrate trust?

4. **Prompt iteration:** How many prompt versions will we need to test before the structured output is consistently accurate across diverse company types (startup vs. enterprise, US vs. international)?

5. **Distribution:** Where do sales reps actually discover new tools? Is LinkedIn sufficient, or do we need Product Hunt, specific Slack communities (RevGenius, Pavilion), or outbound seeding?

6. **V2 timing:** If adoption metrics hit KR targets in Week 1, should we accelerate V2 CRM integration, or stay focused on improving V1 quality first?

7. **Cost per run:** At Claude claude-sonnet-4-20250514 pricing, what is the actual API cost per battlecard at scale? At what usage volume does this become unsustainable without monetization?
