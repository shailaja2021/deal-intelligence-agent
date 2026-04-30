"""
app.py — Streamlit UI for the Deal Intelligence Agent.

This file is the only thing the user interacts with. It handles:
- Rendering the page layout (header, sidebar, input, output)
- Calling generate_battlecard() from agent.py when the button is clicked
- Displaying the returned BattleCard in 6 expandable sections
- Offering a download button for the markdown version of the battlecard
- Showing friendly error messages if anything goes wrong

This file contains NO business logic — it just calls agent.py and renders results.
"""

import streamlit as st
from agent import generate_battlecard

# --- Page Configuration ---
# Must be the first Streamlit command in the file.
# Sets the browser tab title, layout, and favicon emoji.
st.set_page_config(
    page_title="Deal Intelligence Agent",
    page_icon="🤖",
    layout="wide",
)

# --- Sidebar ---
# Brief explanation of what the tool does + link to the GitHub repo.
# Keeps the main area clean — no clutter, no instructions crowding the input.
with st.sidebar:
    st.title("About")
    st.markdown(
        """
        **Deal Intelligence Agent** turns any company name into a structured
        sales battlecard in about 30 seconds.

        It searches the public web, then uses Claude AI to extract and
        organize the intelligence into 6 sections every sales rep needs
        before a call.

        **How to use:**
        1. Type a company name
        2. Click Generate Battlecard
        3. Read the battlecard — or download it as Markdown

        ---
        Built by [Shailaja](https://linkedin.com/in/) · [GitHub](https://github.com/)
        """
    )

# --- Main Header ---
st.title("🤖 Deal Intelligence Agent")
st.subheader("Type a company name. Get a battlecard in 30 seconds.")
st.markdown("---")

# --- Company Name Input ---
# Single text input — the only thing the user needs to provide.
company_name = st.text_input(
    label="Enter company name",
    placeholder="e.g. Salesforce, HubSpot, Stripe",
    help="Type the name of any company you want to research before a call.",
)

# --- Generate Button ---
# Primary button style makes it obvious this is the main action.
generate_button = st.button("🔍 Generate Battlecard", type="primary")

# --- Main Logic: Handle Button Click ---
# Only runs when the button is clicked — Streamlit re-renders the whole page
# on each interaction, so we check button state to know when to act.
if generate_button:

    # Validate that the user entered something before searching
    if not company_name.strip():
        st.warning("⚠️ Please enter a company name before generating a battlecard.")

    else:
        # Show a spinner while the agent is running.
        # The message includes the company name so the user knows what's happening.
        # This is important UX — a 30-second wait with no feedback feels broken.
        with st.spinner(f"Researching {company_name}... this takes about 30 seconds"):
            try:
                # Call the agent — this is where all the work happens.
                # generate_battlecard() calls DuckDuckGo (4 searches) then Claude.
                battlecard = generate_battlecard(company_name)

            except Exception as e:
                # If generate_battlecard() itself raises (not just returns an error card),
                # show a friendly error and stop — don't try to render a None battlecard.
                st.error(
                    f"❌ Something went wrong while researching **{company_name}**.\n\n"
                    f"**Error:** {str(e)}\n\n"
                    "Please try again. If the problem persists, check that your "
                    "ANTHROPIC_API_KEY is set correctly in your .env file."
                )
                st.stop()

        # --- Check if the battlecard is an error card ---
        # agent.py returns a BattleCard with error messages in each field if the
        # LLM call fails. We detect this by checking the first item in company_overview.
        is_error_card = (
            battlecard.company_overview
            and "Error generating" in battlecard.company_overview[0]
        )

        if is_error_card:
            st.error(
                f"❌ The AI was unable to generate a battlecard for **{company_name}**.\n\n"
                f"{battlecard.company_overview[0]}\n\n"
                "Please try again in a few seconds."
            )

        else:
            # --- Check if most fields came back empty or "Not found" ---
            # This can happen for very obscure companies with minimal web presence.
            all_fields = (
                battlecard.company_overview
                + battlecard.funding_growth
                + battlecard.tech_stack
                + battlecard.recent_news
                + battlecard.pain_points
                + battlecard.pitch_angle
            )
            not_found_count = sum(
                1 for item in all_fields if "not found" in item.lower()
            )
            # If more than half the bullet points are "Not found", warn the user
            if not_found_count > len(all_fields) / 2:
                st.warning(
                    f"⚠️ Limited public information was found for **{company_name}**. "
                    "The battlecard may be incomplete. Try a slightly different company name "
                    "or check that the company has a public web presence."
                )

            # --- Render the Battlecard ---
            # Display each of the 6 sections as an expandable panel.
            # All start expanded so the user sees the full battlecard immediately.
            st.success(f"✅ Battlecard generated for **{company_name}**")
            st.markdown("---")

            # Define the sections: (emoji + title, field from BattleCard)
            sections = [
                ("🏢 Company Overview", battlecard.company_overview),
                ("💰 Funding & Growth", battlecard.funding_growth),
                ("🛠️ Tech Stack", battlecard.tech_stack),
                ("📰 Recent News & Triggers", battlecard.recent_news),
                ("😤 Pain Points", battlecard.pain_points),
                ("🎯 Pitch Angle", battlecard.pitch_angle),
            ]

            for section_title, items in sections:
                with st.expander(section_title, expanded=True):
                    if items:
                        for item in items:
                            st.markdown(f"• {item}")
                    else:
                        st.markdown("• Not found")

            st.markdown("---")

            # --- Download Button ---
            # Renders after the battlecard so the rep can save the full output.
            # File name is slugified from the company name for clean filenames.
            file_name = f"{company_name.strip().lower().replace(' ', '-')}-battlecard.md"

            st.download_button(
                label="⬇️ Download as Markdown",
                data=battlecard.to_markdown(),
                file_name=file_name,
                mime="text/markdown",
            )

# --- Footer ---
# Always visible, regardless of button state.
# The disclaimer is important: reps should verify AI-generated facts before citing them.
st.markdown("---")
st.caption("⚠️ AI-generated research. Verify key facts before your call.")
