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
    st.subheader("Job Description Parser")

    col1, col2 = st.columns(2)

    with col1:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., Stripe",
        )

    with col2:
        job_role = st.text_input(
            "Job Role",
            placeholder="e.g., Senior Backend Engineer",
        )

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...",
        height=250,
    )

    # Build company dict if required fields are filled
    if company_name and job_role and job_description:
        companies = [{
            "name": company_name,
            "job_role": job_role,
            "job_description": job_description,
            "tech": [],  # Will be populated by LLM parser
        }]
    else:
        companies = []

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
    if input_method == "Manual Entry":
        st.success(f"Ready to process: **{companies[0]['name']}** - {companies[0]['job_role']}")
    else:
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
