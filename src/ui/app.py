import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

from src.common.enums import ProgressStage
from src.workflows.company_mapper import CompanyMapper
from src.sumble.models import JobSearchCriteria
from src.sumble.client import search_companies
from src.agent.job_description_parser import parse_job_description


st.set_page_config(page_title="Company Mapper", layout="wide")
st.title("Company Mapper")

input_method = st.radio("Input Method", ["Manual Entry", "Upload CSV"], horizontal=True)

if input_method == "Manual Entry":
    st.subheader("Job Description Parser")

    col1, col2, col3 = st.columns(3)

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

    with col3:
        country = st.text_input(
            "Country",
            placeholder="e.g., Germany",
        )

    job_description = st.text_area(
        "Job Description",
        placeholder="Paste the full job description here...",
        height=250,
    )

    # Check if required fields are filled
    form_ready = bool(company_name and job_role and country and job_description)

else:
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    form_ready = False

    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        companies = df.to_dict("records")
        form_ready = bool(companies)
    else:
        companies = []

if form_ready:
    if input_method == "Manual Entry":
        st.success(f"Ready to process: **{company_name}** - {job_role} ({country})")
    else:
        st.write(f"**{len(companies)} companies** ready to process")

if st.button("Run", type="primary", disabled=not form_ready):
    if input_method == "Manual Entry":
        # Step 1: Parse job description to extract skills
        with st.spinner("Parsing job description..."):
            parse_result = parse_job_description(job_description)

        if parse_result.status == "insufficient_info":
            st.error(f"Could not extract skills: {parse_result.reason}")
        else:
            # Step 2: Build JobSearchCriteria with extracted skills
            criteria = JobSearchCriteria(
                company=company_name,
                job_role=job_role,
                country=country,
                tech=parse_result.skills,
            )

            st.info(f"Extracted skills: **{', '.join(criteria.tech)}**")

            # Debug: show the filter being sent
            st.write("Sumble filter:", criteria.to_sumble_filter())

            # Step 3: Search Sumble for companies
            with st.spinner("Searching for companies on Sumble..."):
                companies = search_companies(criteria, limit=5)

            if not companies:
                st.warning("No companies found matching the criteria.")
            else:
                st.success(f"Found **{len(companies)} companies** from Sumble")

                # Step 4: Run CompanyMapper workflow
                progress_container = st.empty()

                def update_progress(stage: ProgressStage, company: str|None, result):
                    if stage == ProgressStage.VERIFYING:
                        progress_container.info(f"Verifying: {company}...")
                    elif stage == ProgressStage.VERIFIED:
                        status = result.status if result else "unknown"
                        progress_container.info(f"Verified {company}: {status}")
                    elif stage == ProgressStage.FINDING_PEOPLE:
                        progress_container.info(f"Finding people at: {company}...")
                    elif stage == ProgressStage.FOUND_PEOPLE:
                        progress_container.info(f"Found {result} people at {company}")

                mapper = CompanyMapper(job_role=job_role, location=country, on_progress=update_progress)

                with st.spinner("Running verification workflow..."):
                    result = mapper.run(companies)

                progress_container.empty()

                # Step 5: Display results
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

    else:
        # CSV flow - existing workflow
        progress_container = st.empty()

        def update_progress(stage: ProgressStage, company: str|None, result):
            if stage == ProgressStage.VERIFYING:
                progress_container.info(f"Verifying: {company}...")
            elif stage == ProgressStage.VERIFIED:
                status = result.status if result else "unknown"
                progress_container.info(f"Verified {company}: {status}")
            elif stage == ProgressStage.FINDING_PEOPLE:
                progress_container.info(f"Finding people at: {company}...")
            elif stage == ProgressStage.FOUND_PEOPLE:
                progress_container.info(f"Found {result} people at {company}")

        mapper = CompanyMapper(job_role="", location="", on_progress=update_progress)

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
