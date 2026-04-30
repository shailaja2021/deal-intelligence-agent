"""
test_all.py — Full test suite for the Deal Intelligence Agent.

Covers: models.py, tools.py, agent.py
- Model and tools tests run with no API calls (mocked)
- Agent test makes one real API call to Claude

Run with: pytest tests/test_all.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from unittest.mock import patch, MagicMock
from models import BattleCard


# =============================================================================
# MODELS TESTS — tests for BattleCard schema and to_markdown()
# No API calls. Runs instantly.
# =============================================================================

@pytest.fixture
def sample_battlecard():
    return BattleCard(
        company_overview=["Stripe — payments infrastructure, B2B SaaS, founded 2010"],
        funding_growth=["Total funding: $9.81B", "Last round: $694M in April 2024"],
        tech_stack=["Ruby, Go, JavaScript", "AWS infrastructure"],
        recent_news=["Launched stablecoin payments API, March 2025"],
        pain_points=["High payment processing costs", "Complex global compliance"],
        pitch_angle=["Lead with multi-currency support", "Opening: I saw you just expanded to APAC..."]
    )


def test_battlecard_creates_successfully(sample_battlecard):
    """BattleCard instantiates with all 6 fields."""
    assert sample_battlecard is not None


def test_battlecard_fields_are_lists(sample_battlecard):
    """All 6 fields are lists as required by schema."""
    assert isinstance(sample_battlecard.company_overview, list)
    assert isinstance(sample_battlecard.funding_growth, list)
    assert isinstance(sample_battlecard.tech_stack, list)
    assert isinstance(sample_battlecard.recent_news, list)
    assert isinstance(sample_battlecard.pain_points, list)
    assert isinstance(sample_battlecard.pitch_angle, list)


def test_battlecard_rejects_missing_field():
    """BattleCard raises ValidationError if a required field is missing."""
    with pytest.raises(Exception):
        BattleCard(
            company_overview=["Stripe"],
            # funding_growth intentionally missing
            tech_stack=["AWS"],
            recent_news=["News"],
            pain_points=["Pain"],
            pitch_angle=["Pitch"]
        )


def test_to_markdown_returns_string(sample_battlecard):
    """to_markdown() returns a string."""
    assert isinstance(sample_battlecard.to_markdown(), str)


def test_to_markdown_contains_all_section_headers(sample_battlecard):
    """to_markdown() includes all 6 emoji section headers."""
    result = sample_battlecard.to_markdown()
    assert "🏢 Company Overview" in result
    assert "💰 Funding & Growth" in result
    assert "🛠️ Tech Stack" in result
    assert "📰 Recent News & Triggers" in result
    assert "😤 Pain Points" in result
    assert "🎯 Pitch Angle" in result


def test_to_markdown_formats_items_as_bullets(sample_battlecard):
    """to_markdown() formats each item as a markdown bullet point."""
    result = sample_battlecard.to_markdown()
    assert "- Stripe — payments infrastructure" in result
    assert "- Total funding: $9.81B" in result


def test_to_markdown_contains_disclaimer(sample_battlecard):
    """to_markdown() includes the AI disclaimer footer."""
    result = sample_battlecard.to_markdown()
    assert "AI-generated research" in result
    assert "Verify key facts" in result


# =============================================================================
# TOOLS TESTS — tests for search_company()
# DuckDuckGo is mocked — no real web requests made.
# =============================================================================

def test_search_company_returns_string():
    """search_company() returns a combined string of 4 labeled sections."""
    with patch('tools.DuckDuckGoSearchRun') as mock_ddg:
        mock_instance = MagicMock()
        mock_instance.run.return_value = "Mocked search result"
        mock_ddg.return_value = mock_instance

        from tools import search_company
        result = search_company("Stripe")

        assert isinstance(result, str)


def test_search_company_contains_all_section_labels():
    """search_company() output includes all 4 section labels."""
    with patch('tools.DuckDuckGoSearchRun') as mock_ddg:
        mock_instance = MagicMock()
        mock_instance.run.return_value = "Mocked search result"
        mock_ddg.return_value = mock_instance

        from tools import search_company
        result = search_company("Stripe")

        assert "=== COMPANY OVERVIEW ===" in result
        assert "=== FUNDING & INVESTORS ===" in result
        assert "=== TECH STACK ===" in result
        assert "=== RECENT NEWS ===" in result


def test_search_company_handles_failed_search():
    """search_company() handles a search failure gracefully — no crash."""
    with patch('tools.DuckDuckGoSearchRun') as mock_ddg:
        mock_instance = MagicMock()
        # Simulate DuckDuckGo throwing an error on every call
        mock_instance.run.side_effect = Exception("Rate limit hit")
        mock_ddg.return_value = mock_instance

        from tools import search_company
        result = search_company("Stripe")

        # Should return a string with placeholders, not crash
        assert isinstance(result, str)
        assert "Search failed" in result


# =============================================================================
# AGENT TESTS — tests for generate_battlecard()
# Claude LLM is mocked — no real API calls made.
# =============================================================================

def test_generate_battlecard_returns_battlecard():
    """generate_battlecard() returns a BattleCard object on success."""
    mock_card = BattleCard(
        company_overview=["Stripe — fintech, B2B SaaS"],
        funding_growth=["$9.81B raised"],
        tech_stack=["AWS, Ruby"],
        recent_news=["Stablecoin launch 2025"],
        pain_points=["Compliance overhead"],
        pitch_angle=["Lead with multi-currency"]
    )

    with patch('agent.search_company', return_value="mocked search results"), \
         patch('agent.structured_llm') as mock_llm:
        mock_llm.invoke.return_value = mock_card

        from agent import generate_battlecard
        result = generate_battlecard("Stripe")

        assert isinstance(result, BattleCard)
        assert result.company_overview == ["Stripe — fintech, B2B SaaS"]


def test_generate_battlecard_returns_error_card_on_failure():
    """generate_battlecard() returns a safe error BattleCard if the LLM call fails."""
    with patch('agent.search_company', return_value="mocked search results"), \
         patch('agent.structured_llm') as mock_llm:
        mock_llm.invoke.side_effect = Exception("API timeout")

        from agent import generate_battlecard
        result = generate_battlecard("Stripe")

        # Should return a BattleCard, not raise an exception
        assert isinstance(result, BattleCard)
        # Error message should appear in the fields
        assert "Error generating" in result.company_overview[0]


def test_generate_battlecard_calls_search(sample_battlecard):
    """generate_battlecard() calls search_company() exactly once."""
    with patch('agent.search_company', return_value="mocked results") as mock_search, \
         patch('agent.structured_llm') as mock_llm:
        mock_llm.invoke.return_value = sample_battlecard

        from agent import generate_battlecard
        generate_battlecard("HubSpot")

        mock_search.assert_called_once_with("HubSpot")
