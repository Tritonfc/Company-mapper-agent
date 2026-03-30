---
name: find-company-github
description: Find a company's GitHub account(s) given the company name. Use this skill whenever someone asks to find, locate, or identify a company's GitHub organization or user account. Also trigger when users mention "GitHub profile", "GitHub org", "company repository", or want to know what name a company uses on GitHub. Works for companies with unusual naming, old/legacy names, or acquired companies.
---

# Find Company GitHub

Your task is to find the primary GitHub account (organization or user) for a given company. Return ONLY the GitHub username/organization name — nothing else.

## Output Format

Return a single line with just the GitHub username(s):

```
<github-username>
```

If the company has multiple verified GitHub accounts, return them comma-separated:

```
<primary-username>, <secondary-username>
```

If no GitHub account can be found after exhaustive searching, return:

```
NOT_FOUND: <brief reason>
```

If the company name is ambiguous (multiple companies share the name), return:

```
AMBIGUOUS: <list the options with their GitHub usernames>
```

## Search Strategy: Adaptive Approach

Start with standard checks. If confidence is high, return immediately. If confidence is low, escalate to exhaustive searching.

### Phase 1: Standard Search (always run)

1. **Direct GitHub search**
   - Search `https://github.com/search?q=<company-name>&type=users`
   - This returns a mix of: employees listing the company in their bio, organizations with similar names, and the actual company account
   - **Don't stop at the first result** — scroll through and identify accounts that look like organization/company accounts (not personal profiles)
   - For each candidate organization, click through and verify:
     - Does it have a verified domain matching the company?
     - Does the email use the company's domain?
     - Does it have repositories (not an empty placeholder)?
   - The actual company account may use an unexpected name (e.g., Oura uses `jouzen`, not `oura` or `ouraring`)

2. **Web search for official presence**
   - Search: `<company-name> GitHub official`
   - Search: `<company-name> open source`
   - Look for the company's official website and check for GitHub links (often in footer, "About", "Careers", or "Developers" sections)

3. **Cross-reference verification**
   - Visit the candidate GitHub profile
   - Check if the profile's website URL matches the company's domain
   - Check the **verified domain** on the GitHub profile (organizations can verify domain ownership)
   - Check if the profile description/bio mentions the company
   - Check the contact email — does it use the company's domain?
   - Look at pinned/popular repositories — do they relate to the company's known products?

**Confidence assessment after Phase 1:**
- HIGH confidence: Exact/close name match + verified via company website link + active repositories matching company products → Return result
- LOW confidence: No clear match, multiple candidates, common company name, or verification links don't match → Proceed to Phase 2

### Phase 2: Exhaustive Search (only if confidence is low)

4. **Google X-ray search for GitHub profiles**
   ```
   site:github.com "<company-name>" -intitle:repos -inurl:tab
   ```
   This finds GitHub pages mentioning the company while filtering out noise.

5. **Search for alternative names**
   - Company's previous/old names (check Wikipedia, Crunchbase for acquisition history)
   - Common abbreviations or variations
   - Parent company or subsidiary names
   - Product names that might be used instead of company name

   Example: Oura (the ring company) might use "ouraring" on GitHub, or a pre-acquisition name.

6. **Developer/engineering blog search**
   - Search: `<company-name> engineering blog GitHub`
   - Search: `<company-name> "our GitHub" OR "on GitHub" OR "GitHub organization"`
   - Tech blogs often link to official GitHub accounts

7. **LinkedIn and job postings**
   - Search: `<company-name> GitHub site:linkedin.com`
   - Engineering job posts often mention "contribute to our open source" with GitHub links

8. **npm/PyPI/package registry search**
   - If the company has known packages, check who published them
   - The publisher organization often matches the GitHub org

9. **Press releases and announcements**
   - Search: `<company-name> "open source" announcement`
   - Companies often announce open source initiatives with GitHub links

10. **Community references**
    - Search: `<company-name> GitHub site:medium.com`
    - Search: `<company-name> GitHub site:dev.to`
    - Search: `<company-name> GitHub site:reddit.com`
    - Developers writing about the company often link to official repos

11. **Search for verified domain**
    - Search: `site:github.com "<company-domain>" verified`
    - GitHub organizations can verify domain ownership — this is a strong signal of authenticity
    - Example: Oura's GitHub is `jouzen` (not `oura` or `ouraring`) but it has `ouraring.com` as a verified domain

### Phase 3: Final Verification

Before returning any result:

1. **Verify the account has PUBLIC content**
   - An account that exists but has ZERO public repositories is NOT a valid result
   - Check: Does the org/user have at least one public repository?
   - Empty placeholder accounts should be treated as NOT_FOUND
   - Example: `github.com/ouraring` exists but has no public repos — this is NOT a valid GitHub presence

2. **Confirm the account is official**
   - Does the GitHub profile link back to the company's official domain?
   - Is the account active (recent commits, maintained repos)?
   - Do the repositories match known company products/projects?

3. **Check for multiple accounts**
   - Some companies have separate orgs for different products or legacy reasons
   - If multiple legitimate accounts exist, identify the PRIMARY one (most active, most followers, linked from company website)
   - Only return secondary accounts if they're clearly official and actively maintained

4. **Reject false positives**
   - Fan accounts or unofficial mirrors
   - Personal accounts of employees (unless company is a solo operation)
   - Archived or abandoned accounts (unless no active alternative exists)
   - Empty/placeholder accounts with no public repositories

## Edge Cases to Handle

- **Ambiguous company names**: Many company names are shared (e.g., "Polar" could be Polar Electro, Polar software platform, or Polar Signals). Look for context clues in the user's query:
  - Industry hints: "Polar fitness" → Polar Electro
  - Product hints: "Polar heart rate sensor" → Polar Electro
  - Domain hints: "Polar (polar.com)" → Polar Electro
  - If no context is provided and multiple valid matches exist, list them and ask for clarification
- **Empty/placeholder accounts**: Some companies register GitHub usernames but never use them publicly. An account with zero public repositories is NOT a valid result — return NOT_FOUND with a note that the account exists but has no public content.
- **Acquired companies**: Search for both current and previous company names (e.g., company was acquired, may still use old GitHub name)
- **Rebranded companies**: Check for both old and new brand names
- **Companies with common names**: Be extra rigorous with verification — cross-reference multiple sources
- **Non-English companies**: Try both English and local language names
- **Stealth/early-stage startups**: May not have public GitHub; return NOT_FOUND if truly not present
- **Companies using personal accounts**: Some small companies operate under the founder's personal GitHub; verify this is intentional/official
- **Companies with only private repos**: Some companies keep all code private. If you find an account linked from their official website but it has no public repos, note this in the NOT_FOUND response.

## Examples

**Input:** `Anthropic`
**Process:** Direct GitHub search → find "anthropics" org → verify website links to anthropic.com → HIGH confidence
**Output:** `anthropics`

**Input:** `Oura`
**Process:** Direct search finds "ouraring" account → but has zero public repos → exhaustive search finds "jouzen" org → verified domain is ouraring.com, email is support@ouraring.com → has 8 public repos → confirmed official
**Output:** `jouzen`

**Input:** `Some Random Startup XYZ`
**Process:** All searches exhausted, no verifiable GitHub presence found
**Output:** `NOT_FOUND: No verifiable GitHub account found after exhaustive search`

**Input:** `Polar fitness watches`
**Process:** Context clue "fitness watches" → search confirms Polar Electro (polar.com) → GitHub is `polarofficial` with verified domain
**Output:** `polarofficial`

**Input:** `Polar` (no context)
**Process:** Multiple companies named Polar found → ambiguous
**Output:** `AMBIGUOUS: Multiple companies named Polar - Polar Electro (polarofficial), Polar software (polarsource), Polar Signals (polarsignals). Please specify which one.`

## Important Notes

- **GitHub search returns noise**: Searching a company name returns employees, fan projects, and similar-named accounts. You must manually sift through results and verify each candidate — don't assume the first or most obvious result is correct.
- **Company names on GitHub are often unexpected**: Companies may use old names, codenames, abbreviations, or completely unrelated names (e.g., Oura → `jouzen`). The verified domain is the most reliable indicator.
- Speed vs accuracy: Don't sacrifice accuracy for speed. A wrong answer is worse than taking longer to find the right one.
- When in doubt, escalate: If Phase 1 doesn't give HIGH confidence, always run Phase 2.
- One source is not enough: Always cross-reference with at least one other source before returning.
- Return the username only: No explanations, no URLs, no additional text — just the GitHub username(s).
