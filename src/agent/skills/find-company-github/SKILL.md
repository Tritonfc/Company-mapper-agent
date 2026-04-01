---
name: find-company-github
description: Find a company's GitHub organization or user account given the company name and domain.
---

# Find Company GitHub

Find the primary GitHub account for a given company. Return ONLY the GitHub username.

## Output Format

```
<github-username>
```

Multiple accounts (comma-separated):
```
<primary>, <secondary>
```

Not found:
```
NOT_FOUND: <brief reason>
```

Ambiguous:
```
AMBIGUOUS: <company1> (username1), <company2> (username2)
```

## Search Strategy

### Step 1: Quick Search
1. Search `<company-name> GitHub official` or `<company-name> site:github.com`
2. Check company website for GitHub links (footer, About, Careers, Developers sections)
3. If company domain provided, search `site:github.com "<company-domain>"`

### Step 2: Verify Candidate
For each candidate GitHub account:
- Does the profile URL/email match the company domain?
- Does it have public repositories? (empty accounts = NOT_FOUND)
- Do repos relate to company products?

If HIGH confidence → return result. If LOW confidence → continue searching.

### Step 3: Deep Search (if needed)
- Search alternative names: abbreviations, old names, parent company
- Search `<company-name> engineering blog GitHub`
- Check npm/PyPI for packages published by the company

### Step 4: Final Check
Before returning:
- Must have at least 1 public repo
- Must link back to company domain OR have verified domain
- Reject: fan accounts, employee personal accounts, empty placeholders

## Edge Cases

- **Ambiguous names**: Use domain/context to disambiguate. If unclear, return AMBIGUOUS.
- **Unexpected GitHub names**: Companies may use old names or codenames (e.g., Oura → `jouzen`). Verified domain is the best signal.
- **Empty accounts**: Account exists but 0 public repos = NOT_FOUND

## Examples

`Anthropic` → `anthropics`
`Oura` → `jouzen` (verified domain: ouraring.com)
`Unknown Startup` → `NOT_FOUND: No verifiable GitHub presence`
`Polar` (no context) → `AMBIGUOUS: Polar Electro (polarofficial), Polar Signals (polarsignals)`
