---
name: find-company-github
description: Find a company's GitHub organization or user account given the company name and domain.
---

# Find Company GitHub

Find the primary GitHub account for a given company. Return ONLY the GitHub username.

## Hard Limits — Read First

- **Max 4 tool calls per company.** If you haven't found it by call 4, return `NOT_FOUND`.
- **Max 2 tool calls per step.** Don't repeat the same search with minor wording changes.
- **Stop early** the moment you hit HIGH confidence. Don't keep verifying.
- If Step 1 yields nothing promising, skip straight to Step 3. Don't exhaust Step 2 on a dead end.

## Output Format

\```
<github-username>
\```

Multiple accounts (comma-separated):
\```
<primary>, <secondary>
\```

Not found:
\```
NOT_FOUND: <brief reason>
\```

Ambiguous:
\```
AMBIGUOUS: <company1> (username1), <company2> (username2)
\```

## Search Strategy

### Step 1: Quick Search (max 2 tool calls)
1. Search `<company-name> GitHub` or check `github.com/<company-name>` directly
2. Check company website for GitHub links (footer, About, Careers)

→ HIGH confidence found? **Return immediately.**
→ Nothing promising? **Skip to Step 3.**

### Step 2: Verify Candidate (max 1 tool call)
Only if you have a candidate but are unsure:
- Does profile URL/email match the company domain?
- Does it have public repos related to company products?

→ Confirmed? **Return immediately.** Not confirmed? **Go to Step 3.**

### Step 3: Deep Search (max 1 tool call — last resort)
Pick ONE of:
- Search alternative name, abbreviation, or parent company
- Check npm/PyPI for packages with a GitHub link

→ Found? Return. Not found? **Return NOT_FOUND immediately.**

### Step 4: Final Check (no tool calls)
Before returning a result:
- Must have ≥1 public repo
- Must link to company domain OR have verified domain
- Reject: fan accounts, employee personal accounts, empty placeholders

## Edge Cases

- **Ambiguous names**: Use domain/context to disambiguate. If still unclear after Step 1, return AMBIGUOUS immediately — don't search further.
- **Unexpected GitHub names**: Companies may use old names or codenames (e.g., Oura → `jouzen`). Verified domain is the best signal.
- **Empty accounts**: 0 public repos = NOT_FOUND, don't investigate further.

## Examples

`Anthropic` → `anthropics`
`Oura` → `jouzen` (verified domain: ouraring.com)
`Unknown Startup` → `NOT_FOUND: No verifiable GitHub presence`
`Polar` (no context) → `AMBIGUOUS: Polar Electro (polarofficial), Polar Signals (polarsignals)`