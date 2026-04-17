---
name: find-related-companies
description: Find companies that use specific technologies, similar to a target company.
---

# Find Related Companies

Find companies that actively use the specified technologies. Return companies that would be good places to recruit candidates from.

## Input

You will receive:
- **Technologies**: 1-3 core technical skills to search for
- **Industry/Context** (optional): Target industry or company type
- **Location** (optional): Geographic focus

## Output

Return 5-10 companies that:
1. Actively use the specified technologies
2. Have engineering teams (not just using as customers)
3. Are real, verifiable companies

## Search Strategy

### Step 1: Direct Technology Search
Search for companies known to use the technologies:
- `"<technology> engineering team"`
- `"companies using <technology>"`
- `"<technology> case study"`
- `"built with <technology>"`

### Step 2: Job Board Search
Search job postings that require these skills:
- `"<technology> engineer jobs"` - extract company names from results
- Check which companies are actively hiring for these skills

### Step 3: Tech Blog/Conference Search
- `"<technology> blog engineering"`
- Companies that speak at tech conferences about these technologies

### Step 4: GitHub/Open Source Search
- Search for companies with popular open source projects in that technology
- Check GitHub organization profiles

## Validation Rules

For each company, verify:
1. **Real company** - Has a website, LinkedIn presence
2. **Tech company or tech team** - Actually builds software (not just uses SaaS)
3. **Uses the technology** - Evidence from job posts, blog, GitHub, or case studies
4. **Active** - Company is still operating, recently posted jobs or content

## What to Include

**DO include:**
- Tech companies of all sizes (startups to enterprises)
- Companies with strong engineering cultures
- Companies known for the technology
- Companies actively hiring for these skills

**DON'T include:**
- Consulting/staffing agencies
- Companies with no web presence
- Companies that only use the tech as customers (e.g., a bakery using Shopify)
- Defunct or acquired companies (unless still operating independently)

## Examples

### Example 1: Python + Django
Technologies: `["Python", "Django"]`

**Return:**
- Instagram (Meta) - instagram.com
- Spotify - spotify.com
- Dropbox - dropbox.com
- Mozilla - mozilla.org
- Eventbrite - eventbrite.com

### Example 2: Rust + Systems Programming
Technologies: `["Rust"]`

**Return:**
- Cloudflare - cloudflare.com
- Discord - discord.com
- Figma - figma.com
- 1Password - 1password.com
- Oxide Computer - oxide.computer

### Example 3: React + TypeScript
Technologies: `["React", "TypeScript"]`

**Return:**
- Vercel - vercel.com
- Stripe - stripe.com
- Linear - linear.app
- Notion - notion.so
- Shopify - shopify.com

## Edge Cases

- **Very niche technology**: If few companies use it, return what you find with a note
- **Extremely common technology**: Focus on companies known for excellence in that tech
- **No results**: Return empty list with status explaining why
