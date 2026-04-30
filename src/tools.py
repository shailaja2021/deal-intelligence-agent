"""
tools.py — Web search tool for the Deal Intelligence Agent.

This file handles all web research. It runs 4 targeted DuckDuckGo searches
for a given company and returns the combined results as a single string.

Why 4 separate searches instead of 1?
DuckDuckGo returns the top ~10 results per query. A single broad query
("tell me about Stripe") returns mixed, general results. Four targeted queries
each optimize for a specific type of content (overview, funding, tech, news),
giving Claude much richer and more structured raw material to work with.
"""

import time
from langchain_community.tools import DuckDuckGoSearchRun


def search_company(company_name: str) -> str:
    """
    Search the public web for information about a company across 4 targeted queries.

    Runs 4 DuckDuckGo searches covering: company overview, funding/investors,
    tech stack, and recent news. Combines all results into one labeled string
    that gets passed to Claude for synthesis.

    A 1-second sleep between searches reduces the risk of DuckDuckGo rate-limiting
    requests from the same IP in rapid succession.

    If any individual search fails (network error, rate limit, etc.), that section
    returns a safe placeholder string rather than crashing the entire function.

    Args:
        company_name (str): The name of the company to research (e.g., "Stripe").

    Returns:
        str: Combined search results from all 4 queries, labeled by section.
             Each section is prefixed with a header so Claude knows what kind
             of data to expect in each block.
    """
    # Initialize the DuckDuckGo search tool from LangChain
    # DuckDuckGoSearchRun wraps the duckduckgo-search library and returns
    # a formatted string of the top search results
    search = DuckDuckGoSearchRun()

    # Define the 4 targeted search queries.
    # Each query is designed to surface a specific type of company intelligence.
    queries = [
        {
            "label": "COMPANY OVERVIEW",
            # Surfaces: what the company does, business model, industry, size
            "query": f"{company_name} company overview business model",
        },
        {
            "label": "FUNDING & INVESTORS",
            # Surfaces: funding rounds, total raised, key investors, ARR/revenue
            "query": f"{company_name} funding investors revenue 2024 2025",
        },
        {
            "label": "TECH STACK",
            # Surfaces: technologies used, key integrations, platforms, APIs
            "query": f"{company_name} tech stack technology integrations",
        },
        {
            "label": "RECENT NEWS",
            # Surfaces: product launches, partnerships, leadership changes, press
            "query": f"{company_name} news product launch partnership 2025",
        },
    ]

    # Collect results from each search into a list
    results = []

    for i, search_config in enumerate(queries):
        label = search_config["label"]
        query = search_config["query"]

        try:
            # Run the search — returns a string of top results
            raw_result = search.run(query)
            results.append(f"=== {label} ===\n{raw_result}")

        except Exception as e:
            # If this search fails, add a placeholder so the other sections
            # still reach Claude. We don't want one failed search to kill the
            # entire battlecard — Claude will write "Not found" for this section.
            results.append(
                f"=== {label} ===\n"
                f"Search failed for query: '{query}'. Error: {str(e)}. "
                f"Mark this section as 'Not found' in the battlecard."
            )

        # Sleep between searches to reduce DuckDuckGo rate-limiting risk.
        # Skip the sleep after the last query — no point waiting after we're done.
        if i < len(queries) - 1:
            time.sleep(1)

    # Join all 4 sections into one combined string with blank lines between them.
    # This is the raw material that gets sent to Claude in agent.py.
    combined_results = "\n\n".join(results)

    return combined_results
