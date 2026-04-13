---
name: parse-job-description
description: Extract 2-3 core technical skills from a job description for candidate filtering.
---

# Parse Job Description

Extract the **2-3 most important technical skills** from a job description. These skills will be used to filter and find candidates, so focus on core technologies that define the role.

## Rules

1. **Maximum 3 skills** - Never return more than 3, even if more are mentioned
2. **Minimum 1 skill** - Always extract at least 1 core skill
3. **Prioritize by importance**:
   - Skills listed as "required" or "must have"
   - Primary programming languages or frameworks central to the role
   - Technologies mentioned multiple times or emphasized
4. **Avoid generic tools** - Skip things like Git, Docker, CI/CD, Agile, Jira unless they are genuinely central to the role
5. **Use canonical names** - Use widely recognized names (e.g., "React" not "ReactJS", "Kubernetes" not "K8s")

## What to Extract

**DO extract:**
- Primary programming languages (Python, Go, Rust, TypeScript)
- Core frameworks (React, Django, Spring Boot, Rails)
- Specialized technologies central to the role (Kafka, Spark, TensorFlow)
- Cloud platforms if role is cloud-focused (AWS, GCP, Azure)

**DON'T extract:**
- Soft skills (communication, teamwork)
- Generic tools everyone uses (Git, VS Code, Slack)
- Vague terms (microservices, REST APIs, cloud)
- Nice-to-haves unless nothing else is available

## Examples

### Example 1: Backend Engineer
Job description mentions: Python, Django, PostgreSQL, Redis, Docker, Kubernetes, AWS, Git, Agile

**Extract:** `["Python", "Django", "PostgreSQL"]`

Reasoning: Python and Django are the core stack, PostgreSQL is the primary database. Docker/K8s/AWS are infrastructure, Git/Agile are generic.

### Example 2: Mobile Developer
Job description mentions: React Native, TypeScript, iOS, Android, Redux, Jest, Firebase, GraphQL

**Extract:** `["React Native", "TypeScript", "GraphQL"]`

Reasoning: React Native is the core framework, TypeScript is the language, GraphQL indicates API architecture. Redux/Jest are supporting tools.

### Example 3: ML Engineer
Job description mentions: Python, PyTorch, TensorFlow, Kubernetes, MLflow, SQL, Spark, AWS SageMaker

**Extract:** `["Python", "PyTorch", "Spark"]`

Reasoning: Python is essential, PyTorch is the primary ML framework mentioned, Spark for data processing. The rest are infrastructure/tooling.

### Example 4: Vague Job Description
Job description only mentions: "modern tech stack", "cloud technologies", "programming experience"

**Extract:** `[]` with status `insufficient_info`

Reasoning: No specific technologies mentioned, cannot extract meaningful skills.
