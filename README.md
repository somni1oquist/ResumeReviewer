
# Resume Reviewer

Resume Reviewer is a prototype application that helps IT students and graduates improve their resumes for better chances in job applications. It leverages LangGraph for workflow orchestration and Azure OpenAI for language analysis, providing actionable feedback and suggestions.

---

## Features

- Upload your resume and a job description.
- Automated parsing and analysis of both documents.
- AI-powered review comparing your resume to the job requirements.
- Actionable feedback and suggestions for improvement.
- Simple, interactive UI with Streamlit.

---

## Tech Stack

- **Streamlit** – User interface
- **LangGraph** – Orchestration framework for multi-step LLM workflows
- **Azure OpenAI** – LLM backend (e.g., GPT-4o)

---

## Setup

### 1. Create a virtual environment

```bash
python -m venv .venv
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or, if you want to install manually:

```bash
pip install -U langgraph "langchain[openai]" dotenv streamlit pymupdf docx2txt
```

### 3. Environment variables

Create a `.env` file in the project root:

```ini
AZURE_OPENAI_API_KEY=REPLACE_WITH_REAL_KEY
AZURE_OPENAI_ENDPOINT=https://dev-multi-agents.openai.azure.com
OPENAI_API_VERSION=REPLACE_WITH_LATEST
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-dev
```

---

## Project Structure

```
resume_reviewer/
├── app.py                  # Streamlit app to run the graph & handle user inputs
├── graph_config.py         # Defines LangGraph nodes, edges, and flow
├── llm_config.py           # Sets up Azure OpenAI models (gpt-4o, embeddings, etc)
├── prompts/
│   ├── resume.txt          # Prompt template for resume parsing
│   ├── job.txt             # Prompt template for JD parsing
│   └── review.txt          # Prompt for alignment analysis & feedback report
├── utils/
│   ├── state.py            # Defines LangGraph state dataclass and related functions
│   └── parse_helper.py     # Resume/job parsing helpers (e.g., PDF/DOCX/text extraction)
└── requirements.txt        # Python dependencies
```

---

## Running the App

```bash
streamlit run app.py
```

---

## Contributing

Contributions, suggestions, and feedback are welcome! Please open an issue or submit a pull request.

---

## License

MIT License (see [LICENSE](LICENSE) file for details)