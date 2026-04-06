import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

from src.common.enums import ProgressStage
from src.workflows.company_mapper import CompanyMapper


st.set_page_config(page_title="Company Mapper", layout="wide")
st.title("Company Mapper")

input_method = st.radio("Input Method", ["Manual Entry", "Upload CSV"], horizontal=True)

if input_method == "Manual Entry":
    st.subheader("Enter Companies")

    company_input = st.text_area(
        "Companies (one per line: company name, tech stack, company url)",
        placeholder="Virta, kotlin, https://www.virta.global\nWolt, react native, https://wolt.com",
        height=150,
    )

    def parse_input(text: str) -> list[dict]:
        companies = []
        for line in text.strip().split("\n"):
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) >= 3:
                companies.append({
                    "name": parts[0],
                    "tech": [t.strip() for t in parts[1:-1]] if len(parts) > 3 else [parts[1]],
                    "company_url": parts[-1],
                })
        return companies

    companies = parse_input(company_input) if company_input else []

else:
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        companies = df.to_dict("records")
    else:
        companies = []

if companies:
    st.write(f"**{len(companies)} companies** ready to process")

if st.button("Run", type="primary", disabled=not companies):
    progress_container = st.empty()

    def update_progress(stage: ProgressStage, company: str, result):
        if stage == ProgressStage.VERIFYING:
            progress_container.info(f"Verifying: {company}...")
        elif stage == ProgressStage.VERIFIED:
            status = result.status if result else "unknown"
            progress_container.info(f"Verified {company}: {status}")
        elif stage == ProgressStage.FINDING_PEOPLE:
            progress_container.info(f"Finding people at: {company}...")
        elif stage == ProgressStage.FOUND_PEOPLE:
            progress_container.info(f"Found {result} people at {company}")

    mapper = CompanyMapper(on_progress=update_progress)

    with st.spinner("Running workflow..."):
        result = mapper.run(companies)

    progress_container.empty()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Verified Companies ({len(result.verified)})")
        if result.verified:
            st.dataframe(result.verified_df(), use_container_width=True)
        else:
            st.info("No companies verified via GitHub")

    with col2:
        st.subheader(f"People Found ({len(result.people)})")
        if result.people:
            st.dataframe(result.people_df(), use_container_width=True)
        else:
            st.info("No people found")
