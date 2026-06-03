"""Streamlit UI for AskPeer MVP."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import streamlit as st
from askpeer.models import Expert, Question
from askpeer.matcher import classify_question, match_question_to_experts
from askpeer.seed_data import EXPERTS

st.set_page_config(page_title="AskPeer", page_icon="🧠", layout="wide")

st.title("🧠 AskPeer")
st.caption("On-demand academic expert matching — not peer review, consultation.")

# Sidebar: expert count
with st.sidebar:
    st.metric("Experts available", len(EXPERTS))
    st.divider()
    st.markdown("### Delivery modes")
    st.markdown("- 🎥 30-min call\n- ✍️ Async feedback\n- 🤝 Collaboration")
    st.divider()
    st.markdown("*MVP — no payment, no login. Just matching.*")

# Main: question input
st.subheader("What's your research problem?")

question_text = st.text_area(
    "Describe your question in detail — what are you working on, what's blocking you?",
    placeholder="E.g., I'm trying to solve a cryo-EM structure of a ~50kDa membrane protein but getting severe preferred orientation. Tried grid screening and detergent exchange — no luck. What am I missing?",
    height=120,
)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    use_llm = st.checkbox("LLM re-rank", value=False, help="Use AI to re-rank matches (slower but better)")

with col2:
    top_k = st.selectbox("Results", [1, 3, 5], index=1)

if st.button("🔍 Find Experts", type="primary", disabled=not question_text.strip()):
    with st.spinner("Analyzing your question..."):
        # Step 1: Classify question
        classification = classify_question(question_text)

        question = Question(
            id="live",
            text=question_text,
            domain=classification.get("domain", ""),
            method=classification.get("method", ""),
            technique=classification.get("technique", ""),
            depth=classification.get("depth", "troubleshooting"),
            classified_text=classification.get("classified_text", question_text),
        )

        # Show classification
        with st.expander("🔍 AI Analysis", expanded=False):
            st.json({
                "domain": question.domain,
                "method": question.method,
                "technique": question.technique,
                "depth": question.depth,
                "classified_text": question.classified_text,
            })

        # Step 2: Match
        matches = match_question_to_experts(
            question, EXPERTS, top_k=top_k, use_llm_rerank=use_llm
        )

        # Step 3: Show results
        st.subheader(f"Top {len(matches)} Matches")

        for i, m in enumerate(matches):
            score_pct = min(int(m.score * 100), 99)
            with st.container():
                cols = st.columns([3, 1])
                with cols[0]:
                    st.markdown(f"### {i+1}. {m.expert.name}")
                    st.caption(f"🏛️ {m.expert.affiliation}")
                with cols[1]:
                    st.metric("Match", f"{score_pct}%")

                st.markdown(f"**Domains**: {', '.join(m.expert.domains)}")
                st.markdown(f"**Methods**: {', '.join(m.expert.methods)}")
                st.markdown(f"**Techniques**: {', '.join(m.expert.techniques)}")
                st.markdown(f"> {m.expert.bio}")

                # Email template
                with st.expander("✉️ Intro Email Template", expanded=False):
                    st.code(f"""Subject: AskPeer: Quick question about {question.domain}

Hi Dr. {m.expert.name.split()[-1]},

I'm a researcher working on {question.domain}. I came across your work on {', '.join(m.expert.domains[:2])} and was hoping you might help with a quick question:

{question_text}

Would you be available for a 30-min call or async feedback?

Best,
[Your name]""", language="text")

                st.divider()

# Footer
st.divider()
st.caption("AskPeer MVP · MIT License")
