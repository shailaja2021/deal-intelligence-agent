# Product Roadmap
# Deal Intelligence Agent
**Author:** Shailaja
**Version:** 1.0
**Last Updated:** 2026-04-29

---

## Roadmap Summary

| Version | Timeframe | Theme | Key Metric |
|---------|-----------|-------|------------|
| V1 — NOW | Shipping | Core battlecard, free & public | Battlecards generated per week |
| V2 — NEXT | TBD | Save, share, and connect to CRM | Battlecards saved to CRM per week |
| V3 — LATER | TBD | Automatic research, team workflow | Battlecards auto-triggered per week |
| V4 — FUTURE | TBD | Full sales intelligence platform | Revenue influenced by battlecard-assisted calls |

---

## V1 — NOW (Shipping)

**Theme:** Prove the core value. One rep, one company, one battlecard in 30 seconds. Free forever.

### Features

| Feature | Description |
|---------|-------------|
| Company name input | Plain text input — no formatting required |
| 4-query web research | DuckDuckGo searches targeting overview, funding, tech stack, recent news |
| Structured battlecard | 6 sections, consistent format, every time |
| Sub-30 second response | Agent + LLM pipeline optimized for speed |
| No login required | Zero friction — open URL, type company, get battlecard |
| Download as Markdown | Save the battlecard locally with one click |
| Streamlit Cloud deployment | Free, public URL — shareable immediately |
| LangSmith evals | Quality monitoring from day one |
| Error handling | Friendly messages for failures; "Not found" instead of hallucination |

### User Benefit

> Any sales rep can walk into any call prepared — in 30 seconds, for free, with no setup.

### Key Metric

**Battlecards generated per week**
- Week 1 target: 10 (early adopters, the builder's network)
- Month 1 target: 50 (LinkedIn, GitHub, sales communities)

### Dependencies

- Anthropic API key (active)
- LangSmith account (free tier)
- GitHub repo (public)
- Streamlit Cloud account (free)

---

## V2 — NEXT 

**Theme:** Reps can save, share, and sync battlecards. Research becomes a team asset, not a one-time event.

### Features

| Feature | Description | Persona Most Impacted |
|---------|-------------|----------------------|
| CRM export | Push battlecard to Salesforce or HubSpot with one click | Maya (AE) |
| Multi-company comparison | View 2–3 battlecards side-by-side | Sam (Manager) |
| Shareable battlecard link | Generate a URL for any battlecard to share via Slack/email | Maya, Sam |
| Search history | Last 10 companies searched, session-persistent | Alex (SDR) |
| Faster search (async) | Run 4 DuckDuckGo queries in parallel instead of sequential — cuts 12s to ~3s | All |
| SerpAPI upgrade (optional) | Replace DuckDuckGo with SerpAPI for more reliable results at scale | All |

### User Benefit

> Sales reps save and share research across their team. The battlecard becomes a team artifact, not a throwaway.

### Key Metric

**Battlecards saved to CRM per week**
- Month 2 target: 20 CRM exports per week
- Implies: users value the output enough to put it in their system of record

### Dependencies

- Salesforce Connected App (OAuth setup)
- HubSpot API integration
- SerpAPI account (if upgrading from DuckDuckGo)
- Redis or simple in-memory cache for search history

### Why Now (Not V1)

CRM integration requires OAuth flows and authenticated app setup — this adds weeks of complexity. V1 proves the battlecard is worth saving before we build the plumbing to save it.

---

## V3 — LATER 

**Theme:** Research becomes automatic. The battlecard appears before the rep even thinks to ask.

### Features

| Feature | Description | Persona Most Impacted |
|---------|-------------|----------------------|
| Slack integration | Auto-send battlecard to a channel or DM 30 min before a calendar event | Alex (SDR), Maya (AE) |
| Email integration | Send battlecard summary to rep's inbox pre-call | Maya (AE) |
| Custom templates per vertical | Healthcare template, FinTech template, SaaS template — different fields per industry | Sam (Manager) |
| Team workspace | Shared library of battlecards, searchable by the whole team | Sam (Manager) |
| Chrome extension | Right-click any company website or LinkedIn profile → generate battlecard | Alex (SDR) |
| Streaming output | Battlecard appears section-by-section as Claude generates it — eliminates wait anxiety | All |

### User Benefit

> Research becomes automatic, not manual. The battlecard is waiting in your inbox before you even think to check.

### Key Metric

**Battlecards auto-triggered per week (zero manual input)**
- Month 4 target: 50% of battlecards generated without a manual search (via calendar or Slack trigger)
- This is the inflection point: research is no longer a task, it's a background service

### Dependencies

- Google Calendar or Outlook API (to read upcoming events)
- Slack Bot API
- Gmail/Outlook API
- User authentication layer (Clerk or Auth0)
- Team data model (users, organizations, shared battlecards)
- LangChain streaming support in Streamlit

### Why Now (Not V2)

Calendar and Slack integrations require user auth, webhook infrastructure, and background jobs — a significant architecture lift. V2 proves reps will use and share battlecards before we invest in automation.

---

## V4 — FUTURE 
**Theme:** Full sales intelligence loop. Before the call, during the call, after the call.

### Features

| Feature | Description | Persona Most Impacted |
|---------|-------------|----------------------|
| Real-time company alerts | Monitor companies for funding rounds, leadership changes, news — push notifications when triggered | Maya (AE), Sam (Manager) |
| Salesforce AppExchange listing | Native CRM app — works inside Salesforce UI | Enterprise sales teams |
| AI post-call scoring | Upload call recording → AI scores discovery quality, objection handling, next steps | Sam (Manager) |
| Call coaching | After call score: "You missed asking about their current tech stack — here's how to handle it next time" | Alex (SDR), Maya (AE) |
| Full API access | Third-party developers can call the battlecard API programmatically | Builders, RevOps teams |
| Enterprise tier | SSO, audit logs, admin controls, SLA support | Enterprise buyers |

### User Benefit

> Full pre-call and post-call intelligence loop. Reps walk in prepared, get coached after, and continuously improve — all automatically.

### Key Metric

**Revenue influenced by battlecard-assisted calls**
- This requires CRM integration (V2) to close the loop: did calls with a battlecard close at a higher rate?
- V4 target: measurable lift in win rate for battlecard-assisted deals vs. control group

### Dependencies

- All V1–V3 features shipped and stable
- Post-call recording infrastructure (Gong API or Zoom integration)
- Alert monitoring pipeline (news/funding APIs: Crunchbase, PitchBook, Google Alerts)
- Enterprise sales motion (pricing, contracts, procurement)
- Dedicated backend infrastructure (cannot run on Streamlit Cloud at this scale)

### Why This Order

V4 requires the trust and adoption built by V1–V3. No enterprise buyer purchases a post-call coaching tool from a product they haven't already seen working. Each version builds the evidence and infrastructure that makes the next version credible and buildable.

---

## Feature Dependency Map

```
V1: Core battlecard (foundation everything else builds on)
  └── V2: CRM export + sharing (requires trust in V1 quality)
        └── V3: Auto-trigger + team workspace (requires auth + CRM pipes from V2)
              └── V4: Alerts + post-call + AppExchange (requires full platform from V3)
```

---

## Metrics Ladder

| Version | North Star Metric | Leading Indicators |
|---------|------------------|-------------------|
| V1 | Battlecards generated / week | Unique visitors, return visit rate, download rate |
| V2 | Battlecards saved to CRM / week | CRM export clicks, shareable link opens, comparison uses |
| V3 | Auto-triggered battlecards / week | Calendar connections, Slack installs, Chrome extension installs |
| V4 | Revenue influenced by battlecard-assisted calls | Win rate lift, deal velocity change, ACV per battlecard-assisted deal |

---

## Out of Scope (All Versions)

These are explicitly not on the roadmap:

- **Mobile app:** Web-first; mobile is a distraction until the desktop use case is proven
- **Building our own LLM:** We use best-in-class APIs; training a model is not our moat
- **Manual data entry:** If a rep has to input more than a company name, it won't get used
- **Pricing tiers in V1–V2:** Free is the growth strategy; monetization comes after retention is proven
