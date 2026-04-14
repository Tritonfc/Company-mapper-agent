"""Test fixtures for job descriptions."""

ICEYE_SENIOR_DATA_ENGINEER = """
Role highlights:

Senior Data Engineer, Geospatial
Location: Espoo, Finland
Department:  Solutions
Reports to: Director of Product Engineering
Employment type: Permanent
Workplace model: Hybrid
Employment is subject to applicable security screening (incl. SUPO, where required)
Why this role matters:

Our ICEYE Solutions analytical products are powered by a geospatial data platform that joins satellite-derived observations with terrain, weather, and other third-party datasets. We are scaling this platform significantly in geographic coverage, breadth of data sources, and the demands placed on it by our data science teams.

We are looking for a Senior Data Engineer to transform our geospatial engine into an analytics platform capable of continent-wide analytics. Your success in this role will be measured by the reliability and performance of the data structures you build, enabling us to process diverse datasets across millions of locations. We operate with a high-velocity, incremental delivery mindset, leveraging AI-assisted development to move fast without compromising on engineering integrity.

We want an environment where testing new geospatial hypotheses is fast and reliable. Your job is to build that foundation, a platform where we can iterate at a high tempo and then systematically turn successful experiments into a continent-wide, production-grade analytical core.

Who We Are

ICEYE delivers space-based intelligence, surveillance, and reconnaissance (ISR) capabilities to governments and allied nations. This includes sovereign and turnkey ISR missions leveraging ICEYE's world-leading synthetic aperture radar (SAR) satellite technology, as well as access to data from the world's largest SAR satellite constellation. These capabilities enable partners to detect and respond to critical changes anywhere on Earth with unprecedented speed and accuracy – day or night and in any weather, supported by ultra high-resolution imagery and high-frequency revisits.

As a trusted partner for defense, intelligence, security, and maritime domain awareness, ICEYE's near real-time data creates a tactical advantage for mission-critical operations. Designed for dual use, the platform also serves civil protection and commercial users for natural-catastrophe intelligence, insurance, maritime monitoring (including oil-spill detection), and finance, contributing to global security and community resilience.

ICEYE is headquartered in Finland and operates globally across Europe, North America, the Middle East, and Asia-Pacific. We have more than 900 employees, united by a shared vision: improving life on Earth by becoming the global source of truth in Earth Observation.


Your day-to day responsibilities

Pipeline Scaling: Extend the existing geospatial data pipeline to cover millions of US properties across several states, using established ingest patterns and adding new data sources
Data Integration: Integrate terrain, hydrographic, land cover, weather, and third-party risk datasets; build and maintain spatial joins at the property scale with quality and lineage tracking
Performance Tuning: Configure and tune databases for large-scale spatial workloads,  indexes, parallelism, memory, and connection management
Frictionless Data Delivery: Automate versioned, analysis-ready data flows that allow data scientists to move from experimental hypothesis to production with zero friction
Data Quality: Maintain coverage monitoring and consistency checks across geographies and data sources
Workflow Reliability: Improve the scheduling, orchestration, and observability of ingest and export pipelines to support repeatable production operations across geographies and data sources
Requirements
What we're looking for

Must haves:

Analytical Architecture & Dataset Design: Proven experience designing and building analysis-ready data structures. You know how to transform raw, noisy geospatial sources into clean, versioned, and performant datasets (e.g., Star Schemas, Feature Tables, or Partitioned Parquet) that allow researchers to iterate without friction
Geospatial & Performance Engineering: 5+ years of professional experience with PostgreSQL / PostGIS in production. You possess deep knowledge of spatial indexing, complex joins, and the performance trade-offs between database-centric and distributed execution patterns for large-scale raster and vector processing
Software Craftsmanship & Code Ownership: Confidence in reading and extending complex Python codebases. You value incremental delivery and have the engineering discipline to ship production-grade code that is testable and maintainable from day one
Data Modeling & Integrity Mastery: Hands-on expertise with common geospatial models and cloud-native formats (Cloud Optimized GeoTIFFs, Geoparquet, STAC). You understand the "physicality" of the data reprojections, tiling, and transformations and how to structure it to ensure long-term data integrity and lineage
Modern Tooling & Velocity: A pragmatic and expert-level approach to using AI-assisted tools (e.g., Cursor, Claude, Copilot). You use these to accelerate routine engineering (boilerplate, unit tests, refactoring), allowing you to focus on high-level architectural decisions
Infrastructure & AWS: Proficiency with AWS (S3, RDS/Aurora, EC2) and scaling database workloads. You have experience managing high-volume data flows where operational stability is as important as the speed of the initial delivery.
Education: Master's degree in Computer Science, Geoinformatics, or a related quantitative field or equivalent depth earned through building real-world systems at scale
Nice to haves:

Experience with flood, climate, or natural hazard data (FEMA, NOAA, USGS)
Deep familiarity with classic and modern geospatial stack - from GDAL/OGR to rioxarray
Experience with distributed data platforms such as Databricks, Delta Lake, PySpark, or Unity Catalog
Parquet / Arrow for analytical data export
Docker and Makefile-based development workflows
Tech stack: PostgreSQL / PostGIS, Python, rasterio / GDAL, AWS, Docker
"""

BACKEND_ENGINEER_PYTHON = """
We are looking for a Senior Backend Engineer to join our team.

Requirements:
- 5+ years of experience with Python
- Strong experience with Django or FastAPI
- Experience with PostgreSQL and Redis
- Familiarity with Docker and Kubernetes
- Experience with AWS services
- Good understanding of REST APIs and microservices
- Excellent communication skills

Nice to have:
- Experience with GraphQL
- Knowledge of Kafka or RabbitMQ
"""
