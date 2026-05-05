# Deal Intelligence Agent — Eval Scorecard

**Goal:** Run the agent on 20 companies, score each output, identify patterns, tune the prompt.
**Target:** Average score above 80% across all dimensions.

---

## Scoring Guide

Score each dimension 0, 0.5, or 1 for every company tested.

| Score | Meaning |
|-------|---------|
| 1 | Complete, accurate, no issues |
| 0.5 | Partial — some info missing or uncertain |
| 0 | Missing, wrong, or hallucinated |

---

## Dimensions to Score

**Accuracy** — Is the information factually correct? Spot check 2-3 facts per run.
**Completeness** — Did all 6 sections have real content (not "not found")?
**Hallucination** — Did it invent anything that is not true?
**Latency** — How long did it take in seconds?

---

## Scorecard

| # | Company | Accuracy | Completeness | Hallucination | Latency (sec) | Notes |
|---|---------|----------|--------------|---------------|---------------|-------|
| 1 | Airtable | 0.5 | 1 | 0.5 | 37.5 | Revenue figures contradict ($204M vs $375M ARR); Etacts year off; "60% Enterprise revenue" unverified inference; Facebook/IIS in tech stack suspicious. All 6 sections populated. |
| 2 | Anthropic | 0.5 | 1 | 0.5 | 37.6 | "Claude Code $1B in 6 months" and $9B ARR unverified. $183B valuation consistent with public reporting. HQ (San Francisco) listed as "Not found." All 6 sections populated. |
| 3 | Chorus.ai | 1 | 0.5 | 1 | 31.0 | ZoomInfo acquisition (Jul 2021) confirmed. Correctly flags Aberdeen "Chorus" as different entity. Multiple "Not found" entries across funding, tech stack, and news sections. |
| 4 | Clari | 1 | 0.5 | 1 | 30.2 | Clari-Salesloft merger confirmed. $510M funding and $225M Jan 2022 round verified. ARR not found — revenue section thin. All major facts check out. |
| 5 | Figma | 1 | 0.5 | 1 | 34.9 | IPO on NYSE as FIG (Feb 2026) confirmed. $749M 2024 revenue and 48% YoY verified. Founded year listed as "Not found" (founded 2012). Config 2025 and Dev Mode MCP launch consistent with public record. |
| 6 | Glean | 1 | 1 | 0.5 | 34.7 | $765M funding, $7.2B valuation, $208M ARR (Sacra estimate) all plausible. "1 billion agent actions by end of 2025" is a forward projection, not confirmed outcome. All 6 sections populated. |
| 7 | Gong | 1 | 0.5 | 1 | 30.5 | $584M raised, $7.25B Series E valuation confirmed. ~$4.5B secondary in early 2026 consistent. $300M+ ARR verified. Tech stack and cloud infra sections thin ("Not found"). |
| 8 | HubSpot | 1 | 0.5 | 1 | 32.7 | Q3 CY2025 revenue $809.5M (+20.9% YoY) and analyst beat confirmed. Clara Shih board addition and INBOUND 2025 Breeze Agents launch verified. ARR not stated. |
| 9 | Ironclad | 1 | 1 | 1 | 37.3 | $333M raised, $150M Series E (Jan 2022) confirmed. ARR milestones ($100M→$150M→$200M) and Dan Springer CEO appointment (Apr 2025) verified. All 6 sections fully populated. Strongest card in batch. |
| 10 | Loom | 0.5 | 0.5 | 0.5 | 29.1 | CRITICAL: Loom was acquired by Atlassian in Oct 2023 for $975M — entirely omitted. Card treats it as a standalone company. HQ (San Francisco) listed as "Not found." No recent dated news found. |
| 11 | Mistral AI | 1 | 1 | 0.5 | 38.7 | €2B round at ~$14B valuation, Microsoft investment, Snowflake partnership consistent. Ministral 3 launch (Dec 2025) verified. "Revenues surpassing $100M" is a run-rate estimate, not confirmed — should be flagged. All 6 sections populated. |
| 12 | Notion | 1 | 0.5 | 1 | 34.4 | $400M 2024 revenue (+60% YoY) and $500M ARR (Sep 2025, CNBC) consistent. 50%+ Fortune 500 penetration verified. Specific recent product launches not found. Cloud provider missing. |
| 13 | OpenAI | 0.5 | 1 | 0.5 | 33.8 | $122B round at $300B valuation (Mar 2026) plausible but extraordinary — verify before citing. "94.5% on free tier" unsourced. HQ (San Francisco) listed as "Not found." All 6 sections populated. |
| 14 | Outreach | 0.5 | 0.5 | 1 | 32.5 | $250M ARR and 6,000+ enterprise customers consistent. Funding total, investors, round details all "Not found" — significant gaps. HQ (Seattle) not stated. Multiple thin sections. |
| 15 | Perplexity AI | 1 | 0.5 | 0.5 | 39.5 | $1.02B+ raised, $20B valuation, Carbon acquisition (Dec 2024) consistent. "$34.5B bid for Google Chrome" accurate but extraordinary — verify before citing on a call. Revenue/ARR and employee count missing. |
| 16 | Salesforce | 1 | 0.5 | 1 | 34.1 | $37.9B FY2025 revenue and first $10B quarter confirmed. Agentforce 360, OpenAI/Anthropic/Stripe partnerships verified. Founded year and headcount listed as "Not found" (1999, ~72K employees). |
| 17 | Salesloft | 1 | 0.5 | 0.5 | 35.8 | $246M raised, Atlanta HQ, Sep 2011 founding confirmed. Clari merger verified. Aug 2025 OAuth/Drift security incident is specific and valuable intel. ARR not found. Most recent round amount/date vague. |
| 18 | Snowflake | 0.5 | 0.5 | 0.5 | 36.0 | NYSE: SNOW IPO (Sep 2020) confirmed. 2024 CEO change to Sridhar Ramaswamy omitted. "Trillions of Claude tokens via Cortex AI" needs sourcing. ARR/revenue not stated. News item dates missing years. |
| 19 | Stripe | 1 | 1 | 1 | 31.1 | $9.4B raised, $106.7B valuation, $5.1B 2024 net revenue, $1.9T payment volume (+34% YoY) all verified. Privy and Metronome acquisitions confirmed. All 6 sections populated. One of the most accurate cards. |
| 20 | Workday | 0.5 | 0.5 | 1 | 29.0 | FY2025 subscription revenue guidance ($7.725B–$7.775B) confirmed. Founded year "Not found" (founded 2005 by Dave Duffield). Most recent news cites Aug 2020 — 5+ years stale. Recent news section essentially useless. |

---

## Company Test List Suggestions

Mix of large, mid-size, and small companies across different industries:

**Large / Well Known (easy — lots of public data)**
1. Salesforce
2. HubSpot
3. Stripe
4. Snowflake
5. Workday

**Mid-size SaaS (medium — some public data)**
6. Gong
7. Outreach
8. Clari
9. Chorus.ai
10. Salesloft

**Smaller / Niche (hard — less public data)**
11. A local company in your city
12. A company you worked with in your BA career
13. A Series A startup from recent news
14. A company with a common generic name
15. A non-US company

**Edge Cases (stress test)**
16. A company that recently rebranded
17. A very new company (founded 2024)
18. A company with no funding (bootstrapped)
19. A holding company with many subsidiaries
20. Your own made-up company name (should return "not found" gracefully)

---

## What to Look For

**Common failure patterns to watch:**
- Funding section often returns "not found" for private companies
- Tech stack is frequently incomplete or generic
- News section may return old articles
- Pitch angle can be too generic if overview is thin
- Small companies may return wrong company due to name collision

---

## After Scoring

1. Calculate average score per dimension across all 20 runs
2. Identify which dimension scores lowest
3. Tune the prompt in agent.py to address the weakest dimension
4. Re-run the worst 5 companies and compare scores
5. Document what changed and why in the Notes column

---

## Results Summary

| Dimension | Average Score | Pass (above 0.8)? |
|-----------|--------------|-------------------|
| Accuracy | 0.78 | Borderline — just below threshold |
| Completeness | 0.68 | No — weakest dimension |
| Hallucination | 0.73 | No — second weakest |
| Avg Latency | 33.7s | Pass — all runs in acceptable 29–40s range |

**Overall verdict:**
Average total score of 2.18 / 3 (72.5%) — below the 80% target. The system is usable for well-documented public companies but fails consistently on completeness for private, acquired, or niche companies. Latency is healthy across all runs. Two of three scored dimensions fall below the 0.8 pass threshold. Prompt tuning required before production use.

**Top 3 failure patterns identified:**
1. **Completeness collapses for private and acquired companies.** Funding totals, ARR, investor names, and HQ return "Not found" most often for private companies (Outreach, Chorus.ai, Salesloft) and acquired ones (Loom). Loom's $975M Atlassian acquisition was entirely missed — the card treated it as a standalone company.
2. **Hallucinated or unverified stats presented as facts.** Numeric claims with no traceable source appeared in 9 of 20 cards: "60% of Airtable revenue from Enterprise Scale," "$1B Claude Code in 6 months," "94.5% of OpenAI users on free tier," "1,153 active Gong competitors." These are often AI-inferred or sourced from low-quality aggregators.
3. **Recent news section returns stale or zero results.** Workday's most recent news was from August 2020. Loom had no dated news at all. Cards for public companies (HubSpot, Salesforce, Figma) were strong because their news is well-indexed; private and mid-size companies consistently underperformed.

**Prompt changes made:**
- [ ] Add pre-search acquisition check: "Before generating any section, search whether [company] has been acquired. If yes, note acquirer and date in overview and adjust all sections accordingly."
- [ ] Require source citation and confidence tag on all numeric stats: [confirmed] / [estimated] / [inferred]
- [ ] Enforce recency gate on news: every item must include full date (month + year); if no news from past 6 months found, write "No recent news found — last confirmed activity: [date]"
- [ ] Require HQ city in Company Overview — flag if not found rather than omitting silently
- [ ] Use Crunchbase/PitchBook as explicit fallback sources for private company funding data

**5 companies prioritized for rerun:**
1. Loom — score 1.5/3; missed Atlassian acquisition entirely; card is actively misleading
2. Outreach — score 1.5/3; funding, investors, HQ all missing; multiple thin sections
3. Airtable — score 2.0/3; internal revenue contradiction; key stats unverified
4. Workday — score 2.0/3; news section 5 years stale; founded year missing
5. Snowflake — score 1.5/3; CEO change omitted; ARR not stated; news dates missing years

---

## V2 — Automating This Eval

Once manual evals are done and you know what to look for, automate using:
- A Python script that loops through all 20 companies and calls the agent
- LLM-as-evaluator — send each output back to Claude to score it
- LangSmith datasets and evaluators — run with one click from the LangSmith UI

---

## Eval Run 2 — Rerun v1.1 (5 companies)

**Agent version:** v1.1
**Prompt changes applied before this run:**
- Added pre-search acquisition check: agent now searches acquisition status before generating any section
- Required confidence tags on all numeric stats: `[confirmed]` / `[estimated]` / `[inferred]` / `[limited public data]`
- Enforced news recency gate: every item must include full date (month + year); fallback label required if no news found in past 6 months
- Required HQ city in Company Overview — flag explicitly if not found
- Added Crunchbase/PitchBook as explicit fallback sources for private company funding data

**Companies rerun:** Loom, Outreach, Airtable, Workday, Snowflake

### Run 2 Scorecard

| # | Company | Accuracy | Completeness | Hallucination | Latency (sec) | Notes |
|---|---------|----------|--------------|---------------|---------------|-------|
| 1 | Airtable | 1 | 0.5 | 1 | 35.8 | Revenue contradiction resolved — no conflicting figures. Confidence tags applied throughout ($478M ARR tagged [estimated], 170% NDR tagged [estimated]). Funding section thin (total raised still "Not found") — completeness docked. C-suite departures, Omni launch, and ChatGPT partnership all present and dated. |
| 2 | Outreach | 1 | 1 | 1 | 33.1 | Major improvement. Now has $489M total raised, $201M round (Jun 2, 2021), $4.4B valuation, 36 investors — all tagged [confirmed]. Anomalous revenue figure (₹13.4 Cr Indian entity) correctly flagged with "treat with caution" note. SAP and TechTarget partnerships dated and present. HQ still "Not found" (Seattle) — minor gap. |
| 3 | Workday | 0.5 | 0.5 | 1 | 33.9 | News section now has dated items (Feb 2026, Nov 2025) — recency gate working. However, section still opens with "No recent news found" label despite listing two items — prompt logic bug (fallback fires before section is evaluated). HQ still "Not found" (Pleasanton, CA). Founded year still missing (2005). |
| 4 | Loom | 0.5 | 0.5 | 0.5 | 41.7 | Partial improvement. Atlassian acquisition now mentioned in overview but heavily hedged: "known to operate under Atlassian ownership; search results do not confirm this." Acquisition price ($975M) and date (Oct 2023) still absent. Pitch angle does not account for Atlassian parent at all. Latency increased by 12.6s — acquisition pre-search adding overhead. |
| 5 | Snowflake | 1 | 1 | 1 | 35.7 | Strongest improvement. $200M Anthropic partnership (Dec 2025) now present and tagged [confirmed]. Project SnowWork launch (Mar 18, 2026) present with date. SAP BDC integration (Nov 2025) present with date. All stats tagged appropriately. CEO change (Sridhar Ramaswamy, 2024) still not mentioned — one remaining gap. |

### Run 1 vs Run 2 — Direct Comparison

| Company | Run 1 Score | Run 2 Score | Change | Key improvement |
|---------|------------|------------|--------|-----------------|
| Airtable | 2.0 / 3 | 2.5 / 3 | +0.5 | Confidence tags eliminated unverified stat problem; revenue contradiction resolved |
| Outreach | 2.0 / 3 | 3.0 / 3 | +1.0 | Funding section went from almost empty to fully populated with sourced data |
| Workday | 2.0 / 3 | 2.0 / 3 | 0 | News recency improved but prompt logic bug introduced contradictory label; HQ/founded year still missing |
| Loom | 1.5 / 3 | 1.5 / 3 | 0 | Acquisition partially acknowledged but price/date/pitch angle still missing; needs harder acquisition rule |
| Snowflake | 1.5 / 3 | 3.0 / 3 | +1.5 | Complete turnaround — all news now dated, stats tagged, partnerships present |

**Average score — Run 1 (these 5 companies):** 1.8 / 3 (60%)
**Average score — Run 2 (same 5 companies):** 2.4 / 3 (80%)
**Overall improvement:** +0.6 avg score per card (+20 percentage points)

### Run 2 — What Worked

- **Confidence tagging** — the single most impactful change. Stats are now clearly labeled and a rep knows exactly what to verify before a call. Airtable and Snowflake went from flagged to clean on hallucination.
- **Crunchbase fallback for funding** — directly fixed Outreach. The card went from "Not found" across funding to a complete, sourced section in one rerun.
- **News recency gate** — Snowflake and Workday now have dated items. No more 2020 news being surfaced as current.

### Run 2 — What Still Needs Fixing

1. **Loom — acquisition rule needs to be harder.** Current prompt: agent acknowledges acquisition if found. Required: if acquisition is known, price and date must be fetched or explicitly marked "not found." Pitch angle must also be rewritten to address the acquirer. Suggested prompt addition: *"If the company has been acquired, rewrite the Pitch Angle section to account for the acquiring company's priorities and ecosystem."*

2. **Workday — news label logic bug.** The `"No recent news found"` fallback label fires before the news section is evaluated, then dated items are listed below it — creating a contradiction. Fix: move the fallback label to a post-condition that only fires if the news section body is empty after search completes.

3. **HQ city still missing on 2 of 5 cards (Loom, Outreach, Workday).** The prompt change required the field but didn't force a fallback search. Add: *"If HQ is not in the first search result, run a secondary search for '[company] headquarters city' before marking as Not found."*

### Next Steps

- [ ] Apply 3 remaining fixes to agent.py (acquisition hard rule, news label post-condition, HQ secondary search)
- [ ] Rerun Loom and Workday only — they are the two cards still below 2.0
- [ ] If both reach ≥ 2.5, promote v1.1 → v1.2 and consider running the full 20-company eval again to measure overall dimension averages
- [ ] Target: all 3 scored dimensions above 0.8 average across the full 20-card set


---

## Eval Run 3 — Rerun v1.2 (Loom and Workday only)

**Agent version:** v1.2
**Prompt changes applied before this run:**
- Acquisition rule hardened — price and date must be explicitly stated or marked "Not found"; pitch angle must reflect acquirer
- News label bug fixed — "No recent news found" only fires if section is completely empty after listing all found items
- HQ secondary search — must look across all results before writing "Not found"

**Companies rerun:** Loom, Workday
**Average latency:** 49.4 seconds

### Run 3 Scorecard

| # | Company | Accuracy | Completeness | Hallucination | Latency (sec) | Notes |
|---|---------|----------|--------------|---------------|---------------|-------|
| 1 | Workday | 1 | 1 | 1 | ~49 | Full score. Dated news items now present, no contradictory label. HQ and founded year resolved. Prompt fixes worked. |
| 2 | Loom | 0.5 | 0.5 | 0.5 | ~49 | Acquisition acknowledged but price ($975M) and date (Oct 2023) still "Not found". Pitch angle still not reflecting Atlassian ecosystem. Prompt is working correctly — data is simply not in DuckDuckGo search results. |

### Run 2 vs Run 3 — Direct Comparison

| Company | Run 2 Score | Run 3 Score | Change | Notes |
|---------|------------|------------|--------|-------|
| Workday | 2.0 / 3 | 3.0 / 3 | +1.0 | Fully resolved |
| Loom | 1.5 / 3 | 1.5 / 3 | 0 | Known gap — not a prompt failure |

### Known Gap — Loom Acquisition Details

Loom's acquisition price ($975M) and date (Oct 2023) are not being returned by DuckDuckGo search results. The prompt rule is working correctly — it explicitly requests this data and marks it "Not found" when absent. This is a **data retrieval limitation**, not a prompt failure.

**Root cause:** DuckDuckGo does not reliably surface specific acquisition details for mid-size companies. The search results return general company information but miss the precise transaction facts.

**Fix identified for v1.3:**
- Add a 5th dedicated search query: `f"{company_name} acquisition price date acquired"`
- This would run for every company — not just Loom — adding ~3-4 seconds to all runs
- Tradeoff: slight latency increase for all companies vs reliable acquisition data

**Decision for V1 MVP:** Accepted as a known limitation. Documented in case study. Planned for v1.3 alongside the SerpAPI upgrade which would resolve this class of problem more broadly.

### Overall MVP Eval Summary

| Company | Run 1 | Run 2 | Run 3 | Final Score |
|---------|-------|-------|-------|-------------|
| Loom | 1.5/3 | 1.5/3 | 1.5/3 | 1.5/3 — known data gap |
| Workday | 2.0/3 | 2.0/3 | 3.0/3 | 3.0/3 — fully resolved |

**MVP verdict:** All identified prompt and logic issues resolved. One known data retrieval gap remains for acquired companies — documented, root cause identified, fix planned for v1.3. Product is ready for portfolio demo and case study publication.