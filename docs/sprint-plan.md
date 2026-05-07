# Sprint Plan
# Deal Intelligence Agent — V1
**Author:** Shailaja
**Duration:** 3 weeks
**Goal:** Ship a publicly deployed, LangSmith-evaluated battlecard generator
**Last Updated:** 2026-04-29

---

## Sprint Overview

| Week | Theme | Goal |
|------|-------|------|
| Week 1 | Foundation | Agent runs end-to-end locally; returns structured data for any company |
| Week 2 | UI & Polish | Full app works locally for 10+ companies; download and error handling complete |
| Week 3 | Ship | Live URL on Streamlit Cloud; LangSmith score > 80%; README and docs complete |

---

## Week 1 — Foundation

**Theme:** Get the agent working. No UI yet. Just data.

**Acceptance Criteria:**
Running `python src/agent.py` with any company name returns a valid, structured BattleCard object printed to the console. No crashes, no placeholder data from the LLM.

---

### Day 1 — Repo Setup

**Goal:** Clean, working local development environment.

**Tasks:**
- [ ] Confirm folder structure matches CLAUDE.md spec: `docs/`, `src/`, `venv/`
- [ ] Create `.env` from `.env.example` — add real `ANTHROPIC_API_KEY`
- [ ] Add `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2=true`, `LANGCHAIN_PROJECT=deal-intelligence-agent` to `.env`
- [ ] Activate `venv` and run `pip install -r requirements.txt`
- [ ] Verify installs: `python -c "import streamlit, langchain, anthropic, pydantic; print('OK')"`
- [ ] Initialize git repo: `git init`, create `.gitignore` (exclude `.env`, `venv/`, `__pycache__/`)
- [ ] First commit: "chore: initial repo structure"

**Done when:** `pip install` succeeds with no errors; Python import check prints "OK"; git repo initialized.

---

### Day 2 — Build `src/models.py`

**Goal:** Define the BattleCard Pydantic schema. This is the contract everything else conforms to.

**Tasks:**
- [ ] Create `src/models.py`
- [ ] Define `BattleCard(BaseModel)` with 6 `List[str]` fields
- [ ] Write docstrings for the class and each field
- [ ] Implement `to_markdown()` method with emoji section headers
- [ ] Test manually: `python -c "from src.models import BattleCard; b = BattleCard(company_overview=['Test'], funding_growth=['Test'], tech_stack=['Test'], recent_news=['Test'], pain_points=['Test'], pitch_angle=['Test']); print(b.to_markdown())"`

**Done when:** BattleCard can be instantiated and `to_markdown()` produces clean markdown output.

---

### Day 3 — Build `src/tools.py`

**Goal:** Agent can search the public web and return raw results.

**Tasks:**
- [ ] Create `src/tools.py`
- [ ] Implement `search_company(company_name: str) -> str`
- [ ] Run 4 targeted DuckDuckGo queries with 1-second sleep between each
- [ ] Wrap each search in try/except with labeled placeholder fallback
- [ ] Test manually: `python -c "from src.tools import search_company; print(search_company('Stripe'))"`
- [ ] Verify: 4 labeled sections appear in output; no crashes if one search fails

**Done when:** Running the test command prints 4 labeled sections of search results for "Stripe" in under 20 seconds.

---

### Day 4 — Build `src/agent.py`

**Goal:** Agent takes a company name, searches the web, calls Claude, and returns a validated BattleCard.

**Tasks:**
- [ ] Create `src/agent.py`
- [ ] Initialize `ChatAnthropic` with `claude-sonnet-4-6`
- [ ] Implement `generate_battlecard(company_name: str) -> BattleCard`
- [ ] Write the synthesis prompt with JSON schema and anti-hallucination instructions
- [ ] Use `with_structured_output(BattleCard)` to get Pydantic-validated response
- [ ] Add try/except that returns a safe error BattleCard if parsing fails
- [ ] Load `.env` variables at module init using `python-dotenv`

**Done when:** `generate_battlecard("Stripe")` returns a BattleCard object with all 6 fields populated (not all "Not found").

---

### Day 5 — End-to-End Test & Fix

**Goal:** Agent is stable and reliable across diverse company types.

**Tasks:**
- [ ] Test with 3 companies covering different profiles:
  - Well-known US startup: "Stripe"
  - Established enterprise: "Salesforce"
  - Smaller / less-covered company: pick a real company with limited press coverage
- [ ] Document any issues found: missing sections, hallucinations, crashes, timeouts
- [ ] Fix top 3 issues found
- [ ] Measure response time for all 3 — confirm < 30 seconds each
- [ ] Review LangSmith dashboard — confirm all 3 runs are logged with input and output visible

**Done when:** All 3 companies return complete battlecards in < 30 seconds with no crashes; LangSmith shows 3 traced runs.

---

## Week 2 — UI & Polish

**Theme:** Connect the agent to a Streamlit UI. Make it look and feel like a real product.

**Acceptance Criteria:**
Running `streamlit run src/app.py` opens a working app in the browser. Entering any company name and clicking "Generate Battlecard" returns a fully formatted battlecard in 6 expandable sections. Download button works. Error handling works.

---

### Day 1 — Build `src/app.py` (Basic Layout)

**Goal:** Streamlit page renders correctly with input and button — no agent connection yet.

**Tasks:**
- [ ] Create `src/app.py`
- [ ] Set page config: title, wide layout, robot emoji favicon
- [ ] Add header: "🤖 Deal Intelligence Agent" + subtitle
- [ ] Add sidebar: tool description + GitHub placeholder link
- [ ] Add text input and "Generate Battlecard" button
- [ ] Add placeholder output area (just a `st.write("Output will appear here")`)
- [ ] Run `streamlit run src/app.py` and confirm page renders without errors

**Done when:** Page opens in browser, sidebar and header are visible, button is clickable (no action yet).

---

### Day 2 — Connect Agent to UI

**Goal:** Button click triggers the agent and raw output appears in the browser.

**Tasks:**
- [ ] Import `generate_battlecard` from `agent.py` in `app.py`
- [ ] On button click: call `generate_battlecard(company_name)` inside `st.spinner()`
- [ ] Display the raw BattleCard object as `st.json()` or `st.write()` temporarily
- [ ] Test with "HubSpot" — confirm output appears in browser
- [ ] Confirm spinner shows and disappears correctly

**Done when:** Clicking the button shows a spinner, then displays the raw BattleCard data in the browser.

---

### Day 3 — Format Battlecard Display

**Goal:** Battlecard renders as 6 clean, labeled expandable sections — looks like a real product.

**Tasks:**
- [ ] Replace raw output with 6 `st.expander()` sections
- [ ] Section order: 🏢 Company Overview → 💰 Funding & Growth → 🛠️ Tech Stack → 📰 Recent News → 😤 Pain Points → 🎯 Pitch Angle
- [ ] Each expander renders its field's list items as bullet points using `st.markdown()`
- [ ] All 6 expanders open by default (`expanded=True`)
- [ ] Test visual layout — confirm spacing, readability, no clutter

**Done when:** Battlecard displays as 6 clean, emoji-labeled expandable sections with bullet points inside each.

---

### Day 4 — Download Button & Loading Message

**Goal:** Users can save the battlecard. Loading state communicates clearly.

**Tasks:**
- [ ] Update spinner message to include company name: `"Researching {company_name}... this takes about 30 seconds"`
- [ ] After battlecard renders, add `st.download_button()`:
  - Label: "⬇️ Download as Markdown"
  - Data: `battlecard.to_markdown()`
  - File name: `f"{company_name.lower().replace(' ', '-')}-battlecard.md"`
  - MIME: `"text/markdown"`
- [ ] Test: click download button, confirm `.md` file opens correctly with all 6 sections

**Done when:** Download button appears after battlecard renders; clicking it downloads a correctly formatted `.md` file.

---

### Day 5 — Error Handling

**Goal:** App never crashes. Every failure state shows a useful, friendly message.

**Tasks:**
- [ ] Handle: company name input is empty → show "Please enter a company name" warning
- [ ] Handle: `generate_battlecard()` raises an exception → show `st.error()` with friendly message and retry suggestion
- [ ] Handle: BattleCard fields all return "Not found" → show `st.warning()` noting limited data was found
- [ ] Handle: API timeout (simulate by temporarily using a bad API key) → confirm error message appears, app doesn't crash
- [ ] Test full flow with 10 different companies — confirm no crashes, all render correctly

**Done when:** App handles all 4 error scenarios gracefully; 10 companies tested end-to-end with no crashes.

---

## Week 3 — Ship

**Theme:** Evaluate, deploy, document. Make it real.

**Acceptance Criteria:**
A public Streamlit Cloud URL works for any visitor. LangSmith eval score on 20 companies > 80%. README is complete and accurate. LinkedIn post is drafted.

---

### Day 1 — LangSmith Setup & Verification

**Goal:** Every agent run is fully traced in LangSmith. Dashboard is readable.

**Tasks:**
- [ ] Confirm LangSmith tracing is capturing runs (check dashboard after 3 test runs)
- [ ] Review a trace end-to-end: input → search results → prompt → LLM output → parsed BattleCard
- [ ] Confirm token counts and latency are visible per run
- [ ] Label the project "deal-intelligence-agent" in LangSmith dashboard
- [ ] Set up a simple eval dataset: 20 company names as test inputs

**Done when:** LangSmith dashboard shows complete traces for every run; 20-company eval dataset created.

---

### Day 2 — Run Evals on 20 Companies

**Goal:** Understand actual quality before shipping. Know the failure modes.

**Tasks:**
- [ ] Run `generate_battlecard()` on all 20 companies in eval set
- [ ] For each run, manually score 3 criteria (1–5 scale):
  - **Accuracy:** Are the facts correct vs. what a manual Google search confirms?
  - **Completeness:** Are most fields populated (not "Not found")?
  - **Hallucination:** Does any section contain made-up facts?
- [ ] Record scores in a simple spreadsheet or markdown table
- [ ] Identify the 3 most common failure patterns

**Target scores:**
- Accuracy: ≥ 4/5 average
- Completeness: ≥ 70% of fields populated
- Hallucination: 0 confirmed hallucinations (or document and flag)

**Done when:** 20 companies scored; failure patterns documented; average scores calculated.

---

### Day 3 — Prompt Tuning

**Goal:** Fix the top issues found in evals by improving the synthesis prompt.

**Tasks:**
- [ ] Based on eval findings, identify the specific prompt instructions that are causing issues
- [ ] Make targeted prompt edits in `agent.py` (one change at a time)
- [ ] Re-run the 5 worst-performing companies from eval set
- [ ] Confirm scores improve after each change
- [ ] Do not over-engineer — stop when scores meet targets

**Common fixes to try:**
- Add section-specific instructions if a section is consistently weak
- Add examples of good vs. bad output for problematic sections
- Adjust "Not found" instructions if the model is hallucinating instead of saying "Not found"

**Done when:** All 5 re-tested companies score ≥ 4/5 on accuracy and 0 hallucinations.

---

### Day 4 — Deploy to Streamlit Cloud

**Goal:** Public URL that works for any visitor, anywhere.

**Tasks:**
- [ ] Push final code to GitHub (public repo)
- [ ] Go to share.streamlit.io → connect GitHub repo → set main file to `src/app.py`
- [ ] Add secrets in Streamlit Cloud dashboard:
  - `ANTHROPIC_API_KEY`
  - `LANGCHAIN_API_KEY`
  - `LANGCHAIN_TRACING_V2 = true`
  - `LANGCHAIN_PROJECT = deal-intelligence-agent`
- [ ] Trigger deploy — wait for it to go live
- [ ] Test from a private browser window (no local environment): run 3 companies
- [ ] Confirm LangSmith captures runs from Streamlit Cloud (not just local)
- [ ] Add live URL to README.md, case-study.md

**Done when:** Public URL returns a valid battlecard for "Salesforce" in < 30 seconds from a fresh browser with no local environment.

---

### Day 5 — Document & Share

**Goal:** Anyone who finds this on GitHub or LinkedIn can understand, use, and learn from it.

**Tasks:**
- [ ] Finalize `README.md`:
  - Add live Streamlit Cloud URL
  - Replace all placeholder links
  - Add screenshot or GIF of the app in action (record with Loom or QuickTime)
- [ ] Update `docs/case-study.md` with post-launch content:
  - Fill in "The Problem", "The Solution", "How I Built It" sections
  - Add LangSmith eval results as "Results & Learnings"
- [ ] Update `docs/PRD.md` and `docs/system-design.md` if anything changed during build
- [ ] Draft LinkedIn post:
  - Hook: the problem (reps skip research, calls suffer)
  - What you built (30-second AI battlecard generator)
  - What you learned (as an AI PM, not just a developer)
  - Link to live app and GitHub
  - Screenshot of a battlecard output

**Done when:** README is complete with live URL; LinkedIn post is drafted and ready to publish.

---

## Sprint Summary

| Milestone | Target Date | Done When |
|-----------|------------|-----------|
| Agent returns BattleCard locally | End of Week 1 | `generate_battlecard("Stripe")` prints valid BattleCard |
| Full app runs locally | End of Week 2 | 10 companies tested; download and errors work |
| Live on Streamlit Cloud | Day 4, Week 3 | Public URL works from fresh browser |
| Evals > 80% | Day 3, Week 3 | 20 companies scored; avg accuracy ≥ 4/5 |
| Docs & LinkedIn | Day 5, Week 3 | README complete; LinkedIn post drafted |

---

## Risk Log

| Risk | Probability | Impact | Owner | Mitigation |
|------|-------------|--------|-------|------------|
| DuckDuckGo rate limiting on Streamlit Cloud IP | Medium | High | Shailaja | Test on Day 4 Week 3; switch to `DDGS` library if needed |
| Claude returns malformed JSON (fails Pydantic) | Low | Medium | Shailaja | Error BattleCard fallback already built into agent.py |
| requirements.txt version conflicts | Low | Low | Shailaja | Test install in fresh venv before deploy |
| Streamlit Cloud deploy fails | Low | Medium | Shailaja | Check logs; most issues are missing secrets or wrong main file path |
