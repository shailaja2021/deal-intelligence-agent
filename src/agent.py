"""
agent.py — LangChain agent that orchestrates research and structured output.

This is the brain of the Deal Intelligence Agent. It:
1. Calls search_company() from tools.py to gather raw web research
2. Builds a structured prompt with those results and the battlecard schema
3. Calls Claude claude-sonnet-4-20250514 via LangChain with structured output
4. Returns a validated BattleCard Pydantic object to the caller (app.py)

LangSmith tracing is enabled automatically via environment variables.
Every call to generate_battlecard() is logged as a trace in LangSmith —
no extra code required beyond setting LANGCHAIN_TRACING_V2=true.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic

from tools import search_company
from models import BattleCard

# Load .env from the project root (one level up from this src/ file).
# Using an explicit path means this works regardless of what directory
# the script is run from — locally, in tests, and on Streamlit Cloud.
load_dotenv(Path(__file__).parent.parent / ".env")

# Initialize the Claude claude-sonnet-4-20250514 language model via LangChain.
# We use langchain_anthropic's ChatAnthropic wrapper so we can use LangChain's
# with_structured_output() feature, which coerces Claude's response directly
# into a validated Pydantic model — no manual JSON parsing required.
#
# temperature=0 means deterministic output — we want consistent, factual
# battlecards, not creative variation. This reduces hallucination risk.
llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0,
    api_key=os.getenv("ANTHROPIC_API_KEY"),
)

# Attach the BattleCard Pydantic schema to the LLM.
# with_structured_output() tells LangChain to instruct Claude to return JSON
# that matches the BattleCard schema, then automatically validates and parses
# the response into a BattleCard object. If Claude's output doesn't match the
# schema, LangChain raises a validation error — which we catch below.
structured_llm = llm.with_structured_output(BattleCard)


def generate_battlecard(company_name: str) -> BattleCard:
    """
    Generate a structured sales battlecard for a given company.

    This is the main function called by app.py. It orchestrates the full pipeline:
    search → prompt → LLM call → Pydantic validation → return.

    Args:
        company_name (str): The name of the company to research (e.g., "Stripe").

    Returns:
        BattleCard: A validated Pydantic object with 6 populated sections.
                    If the LLM call fails, returns a BattleCard with error
                    messages in each field so the app can display something
                    useful rather than crashing.
    """

    # --- Step 1: Web Research ---
    # Call tools.py to run 4 DuckDuckGo searches and get combined raw results.
    # This takes ~8–12 seconds (4 searches × ~2 seconds each + 3 × 1 sec sleeps).
    raw_search_results = search_company(company_name)

    # --- Step 2: Build the Synthesis Prompt ---
    # This prompt is what gets sent to Claude. It includes:
    # - The raw search results (the "facts" Claude must work from)
    # - Explicit instructions on what to extract for each section
    # - A strict anti-hallucination rule: only use what's in the results
    #
    # The prompt is long by design. Claude performs better with specific
    # instructions per section than with a single vague "make a battlecard" command.
    prompt = f"""You are a sales intelligence analyst. Your job is to read raw web search results
about a company and extract structured information for a sales battlecard.

COMPANY: {company_name}

RAW SEARCH RESULTS:
{raw_search_results}

---

INSTRUCTIONS:
Extract information from the search results above and populate each battlecard section.

CRITICAL RULES:
1. Only use facts explicitly stated in the search results above.
2. If information for a field is NOT in the search results, write "Not found" as the item — do NOT guess, infer, or make up plausible-sounding facts.
3. Be specific and concrete — exact numbers, names, and dates when available.
4. Each field should have 3–6 bullet points (list items).
5. Write in plain, direct language a sales rep can read in 10 seconds.
6. ACQUISITION CHECK (HARD RULE): If {company_name} has been acquired, you MUST state the acquirer name, acquisition date (month + year), and acquisition price in company_overview. If price or date is not in the search results, write "acquisition price: Not found" and "acquisition date: Not found" — do NOT omit these fields. The pitch_angle section MUST be rewritten to reflect the acquiring company's ecosystem and priorities — do not pitch as if the company is still independent.
7. CONFIDENCE TAGS: Every numeric stat (revenue, funding, valuation, user counts, growth %) must end with one of: [confirmed] if from a named source, [estimated] if from an analyst or projection, [inferred] if derived from context. Example: "$500M ARR [confirmed — CNBC, Sep 2025]"
8. RECENCY GATE: Only list news items that have a confirmed month and year. Do NOT write "No recent news found" if you have dated items — only write it if the news section is completely empty after listing all found items.
9. HQ REQUIRED: Always include "HQ: [city, country]" in company_overview. If not in the first search result, look for "[company] headquarters" in any other result before writing "HQ: Not found".
10. PRIVATE COMPANY FLAG: If funding data is thin because the company is private, add "[limited public data — figures may be incomplete]" to the funding_growth section.

WHAT TO EXTRACT:

company_overview:
- REQUIRED: HQ city and country — write "HQ: Not found" if missing
- REQUIRED: Acquisition status — state if acquired, by whom, when, and for how much
- Company name, industry, and approximate size (employees or scale)
- Year founded (if mentioned)
- Business model: B2B, B2C, marketplace, etc.
- Core products or services (1–2 sentences)

funding_growth:
- Total funding raised with confidence tag
- Most recent funding round (type + amount + date) with confidence tag
- Key investors or backers named in results
- Revenue or ARR with confidence tag
- Growth metrics (user count, customer count, YoY growth) with confidence tag
- Add [limited public data — figures may be incomplete] if company is private and data is thin

tech_stack:
- Technologies, programming languages, or frameworks mentioned
- Key platforms or infrastructure they run on (e.g., AWS, GCP, Azure)
- Major integrations or APIs they use or offer
- Notable technical differentiators mentioned

recent_news:
- Up to 3 recent news items — EACH MUST include month and year
- If no news from past 6 months found, write: "No recent news found — last confirmed activity: [date]"
- Recent product launches or major announcements
- Partnerships or acquisitions
- Hiring trend: are they actively hiring, doing layoffs, or stable?

pain_points:
- Likely operational challenges given their industry and growth stage
- Problems a B2B SaaS seller could plausibly address for this company
- Gaps or pressures implied by the news or business model
(These may be inferred from their industry/stage, but ground them in what the results reveal)

pitch_angle:
- How a B2B SaaS seller should position their product for this specific company
- A suggested opening line for the sales call (1 sentence, conversational tone)
- 2–3 likely objections and a one-line rebuttal for each

Now extract the battlecard from the search results. Remember: "Not found" over hallucination, every time.
"""

    # --- Step 3: Call Claude with Structured Output ---
    # structured_llm is the LLM bound to the BattleCard schema.
    # LangChain sends the schema to Claude as part of the tool-calling interface,
    # so Claude knows exactly what JSON shape to return.
    # The response is automatically validated against BattleCard — no manual parsing.
    try:
        battlecard = structured_llm.invoke(prompt)
        return battlecard

    except Exception as e:
        # If the LLM call fails (network error, API timeout, malformed response,
        # Pydantic validation failure), return a safe BattleCard with error messages
        # in every field. This prevents the Streamlit app from crashing and gives
        # the user a clear signal that something went wrong.
        error_message = f"Error generating this section: {str(e)}"

        return BattleCard(
            company_overview=[error_message, "Please try again or check your API key."],
            funding_growth=[error_message],
            tech_stack=[error_message],
            recent_news=[error_message],
            pain_points=[error_message],
            pitch_angle=[error_message],
        )
