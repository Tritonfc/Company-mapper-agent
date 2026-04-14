# Company Mapper Agent

## Project Overview
A tool that finds companies and candidates matching job requirements by:
1. Parsing job descriptions to extract core tech skills
2. Querying Sumble API to find companies using those technologies
3. Verifying companies via GitHub tech stack analysis
4. Finding people at unverified companies via Exa AI

## Architecture

### Entry Point
- `src/ui/app.py` - Streamlit UI with two modes:
  - **Manual Entry**: Company name, job role, country, job description → parses skills → queries Sumble → runs verification
  - **Upload CSV**: Legacy flow, direct company list input

### Key Components

**Job Description Parser** (`src/agent/job_description_parser.py`)
- Uses Claude Haiku via LangChain `create_agent`
- Extracts 1-3 core technical skills from job descriptions
- Skill prompt: `src/agent/skills/parse-job-description/SKILL.md`
- Model: `JobDescriptionParseResult` in `src/agent/models.py`

**Sumble Integration** (`src/sumble/`)
- `models.py`: `JobSearchCriteria` - holds company, job_role, country, tech
  - `to_sumble_filter()` - simple filter format: `{"technologies": [...]}`
  - `to_sumble_query()` - advanced query format (not currently used)
- `client.py`: `search_companies(criteria, limit)` - queries Sumble, returns companies for CompanyMapper

**Company Mapper** (`src/workflows/company_mapper.py`)
- Orchestrates verification pipeline
- Input: `list[dict]` with keys: `name`, `tech`, `company_url`
- Runs `TechStackVerifier` for each company
- Runs `PeopleFinder` for failed verifications

**Tech Stack Verifier** (`src/workflows/tech_stack_verifier.py`)
- 5-step pipeline: Find GitHub org → Search by language → Search by keyword → Deep dive → Fail
- Uses `find_company_github()` agent to locate GitHub org

**GitHub Finder Agent** (`src/agent/github_finder.py`)
- Uses web search to find company's GitHub org
- Skill prompt: `src/agent/skills/find-company-github/SKILL.md`

**People Finder** (`src/workflows/people_finder.py`)
- Uses Exa AI to find LinkedIn profiles
- Searches by company + tech stack

### Test Fixtures
- `tests/fixtures/job_descriptions.py` - Sample job descriptions for testing

## Current Status
- Manual entry flow wired up end-to-end
- Sumble integration using simple filter format (advanced query had issues)
- `hiring_location` filter commented out - need to confirm correct field name

## Environment
- `SUMBLE_API_KEY` - Required for Sumble API
- `GITHUB_TOKEN` - Required for GitHub API
- `EXA_API_KEY` - Required for Exa AI
- `ANTHROPIC_API_KEY` - Required for Claude/LangChain

## Running
```bash
streamlit run src/ui/app.py
```
