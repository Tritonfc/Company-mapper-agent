import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st

from src.common.enums import ProgressStage
from src.workflows.company_mapper import CompanyMapper
from src.agent.job_description_parser import parse_job_description
from src.agent.related_companies_finder import find_related_companies
from src.agent.models import CompanyResult


st.set_page_config(page_title="Company Mapper", layout="wide")
st.title("Company Mapper")

# --- Session state initialization ---
if "result" not in st.session_state:
    st.session_state.result = None
if "companies" not in st.session_state:
    st.session_state.companies = []
if "parse_result" not in st.session_state:
    st.session_state.parse_result = None
if "extracted_skills" not in st.session_state:
    st.session_state.extracted_skills = None

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

    form_ready = bool(company_name and job_role and country and job_description)

else:
    st.subheader("Upload CSV")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    form_ready = False
    company_name = ""
    job_role = ""
    country = ""

    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        st.session_state.companies = [
            CompanyResult(
                name=row.get("name", ""),
                tech=row.get("tech", "").split(",") if isinstance(row.get("tech"), str) else row.get("tech", []),
                company_url=row.get("company_url", ""),
            )
            for row in df.to_dict("records")
        ]
        form_ready = bool(st.session_state.companies)

if form_ready:
    if input_method == "Manual Entry":
        st.success(f"Ready to process: **{company_name}** - {job_role} ({country})")
    else:
        st.write(f"**{len(st.session_state.companies)} companies** ready to process")

if st.button("Run", type="primary", disabled=not form_ready):
    # Reset previous results on new run
    st.session_state.result = None
    st.session_state.extracted_skills = None

    if input_method == "Manual Entry":
        # Step 1: Parse job description
        with st.spinner("Parsing job description..."):
            parse_result = parse_job_description(job_description)
            st.session_state.parse_result = parse_result

        if parse_result.status == "insufficient_info":
            st.error(f"Could not extract skills: {parse_result.reason}")
        else:
            st.session_state.extracted_skills = parse_result.skills
            st.info(f"Extracted skills: **{', '.join(parse_result.skills)}**")

            # Step 2: Find related companies
            with st.spinner("Finding related companies..."):
                companies = find_related_companies(
                    companyHire=company_name,
                    tech=parse_result.skills,
                    location=country,
                    limit=10
                )
                st.session_state.companies = companies

            if not companies:
                st.warning("No companies found matching the criteria.")
            else:
                st.success(f"Found **{len(companies)} related companies**")

                # Step 3: Run CompanyMapper workflow
                progress_container = st.empty()

                def update_progress(stage: ProgressStage, company: str | None, result):
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
                    st.session_state.result = mapper.run(companies)

                progress_container.empty()

    else:
        # CSV flow
        progress_container = st.empty()

        def update_progress(stage: ProgressStage, company: str | None, result):
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
            st.session_state.result = mapper.run(st.session_state.companies)

        progress_container.empty()

# --- Display results (outside button block, persists across re-runs) ---
if st.session_state.extracted_skills:
    st.info(f"Extracted skills: **{', '.join(st.session_state.extracted_skills)}**")

if st.session_state.result:
    result = st.session_state.result

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