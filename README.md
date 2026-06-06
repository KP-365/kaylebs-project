# kaylebs-project

Two AI systems: a multi-agent biomedical research tool and a Retrieval-Augmented Generation system for clinical A&E data.

---

## 1. Biomedical Research Agent

A multi-agent pipeline that takes a biomedical research topic, searches for relevant scientific papers, and produces a structured analysis report.

### How it works

1. User inputs a research topic
2. Apify actor scrapes up to 10 papers (title, URL, abstract)
3. CrewAI research agent analyses the collected abstracts
4. Agent outputs a structured report covering: key findings, study methodologies, clinical significance, research trends, quality assessment, and recommendations

### Stack

`CrewAI` `Apify` `OpenAI API` `Python`

### Run

```bash
pip install crewai apify-client openai
python Biomain.py
```

Set your API keys in environment variables before running:
```bash
export OPENAI_API_KEY=your_key
export APIFY_API_TOKEN=your_token
```

---

## 2. RAG A&E System

A Retrieval-Augmented Generation system built for Accident and Emergency clinical data, with separate backend and frontend services managed through Docker Compose.

### Stack

`Python` `Docker` `RAG pipeline` `REST API`

### Run

```bash
docker-compose up
```

API can be tested with the included shell script:
```bash
bash test_api.sh
```

See `RAG - A&E/README.md` for full setup and configuration details.
