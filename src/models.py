"""
models.py — Pydantic data model for the Deal Intelligence Agent battlecard.

This file defines the BattleCard schema. Every other file in the project
references this model — it is the single source of truth for what a battlecard
contains and how it is structured.
"""

from pydantic import BaseModel
from typing import List


class BattleCard(BaseModel):
    """
    Structured sales battlecard output from the Deal Intelligence Agent.

    Each field is a list of strings — bullet points for that section.
    The agent (agent.py) populates these fields by calling Claude with
    structured output. The UI (app.py) renders each field as a section.

    If information for a field could not be found, items will contain
    "Not found" — the agent is instructed never to fabricate data.
    """

    company_overview: List[str]
    """
    High-level company snapshot.
    Contains: company name, industry, size, HQ, founded year,
    business model (B2B/B2C/marketplace), key products and services.
    """

    funding_growth: List[str]
    """
    Financial and growth signals.
    Contains: total funding raised, most recent round and date,
    key investors, ARR or revenue if publicly known.
    """

    tech_stack: List[str]
    """
    Technology profile.
    Contains: known technologies the company uses, key integrations
    and platforms they run on (e.g., Salesforce, AWS, Stripe).
    """

    recent_news: List[str]
    """
    Latest signals and triggers.
    Contains: last 3 significant news items with dates, hiring trends
    (growing/shrinking/stable), recent product launches or partnerships.
    """

    pain_points: List[str]
    """
    Likely challenges this company faces.
    Contains: problems typical for their industry and growth stage,
    and how your product could address those problems specifically.
    """

    pitch_angle: List[str]
    """
    How to approach this company on a call.
    Contains: positioning recommendation for this specific company,
    a suggested opening line, and key objections to anticipate with
    suggested rebuttals.
    """

    def to_markdown(self) -> str:
        """
        Format the battlecard as clean, downloadable markdown.

        Returns a string with 6 sections, each with an emoji header
        and bullet points for each item. Used by the Streamlit download
        button so reps can save the battlecard to their notes or CRM.

        Returns:
            str: The full battlecard formatted as markdown text.
        """
        # Map each field to its display label and emoji
        sections = [
            ("🏢 Company Overview", self.company_overview),
            ("💰 Funding & Growth", self.funding_growth),
            ("🛠️ Tech Stack", self.tech_stack),
            ("📰 Recent News & Triggers", self.recent_news),
            ("😤 Pain Points", self.pain_points),
            ("🎯 Pitch Angle", self.pitch_angle),
        ]

        lines = ["# Deal Intelligence Battlecard\n"]

        for section_title, items in sections:
            lines.append(f"## {section_title}")
            for item in items:
                # Each item becomes a markdown bullet point
                lines.append(f"- {item}")
            lines.append("")  # blank line between sections

        lines.append("---")
        lines.append("*⚠️ AI-generated research. Verify key facts before your call.*")

        return "\n".join(lines)
