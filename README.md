# RAG-to-SQL

A small Streamlit demo that converts plain-English questions into SQL, executes the generated SQL against a local SQLite database, and returns a human-friendly explanation of the results using Google Generative AI (Gemini).

This repository is an experimental prototype intended to demonstrate prompt-to-SQL generation and how a model can help explain query results. It is not production-ready.

---

## Features

- Natural-language input via a Streamlit web UI.
- Uses Google Generative AI (Gemini) to translate English questions into SQL statements tailored to the demo schema.
- Executes the generated SQL against `patient.db` (SQLite) and returns results.
- Uses Gemini again to produce a friendly, human-readable explanation of the query results.

---

## Quickstart

1. Clone the repository:

   git clone https://github.com/mudgalma/RAG-to-SQL.git
   cd RAG-to-SQL

2. (Optional) Create and activate a virtual environment:

   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows

3. Install dependencies:

   pip install -r requirements.txt

4. Add your Google Generative AI API key to a `.env` file in the repository root:

   GOOGLE_API_KEY=your_google_api_key_here

   Do NOT commit your real API key to the repository.

5. Run the Streamlit app:

   streamlit run app.py

6. In the browser UI, type a question (examples below) and click "Ask the question".

---

## Example prompts

- "Find records for Patient John Doe"
- "Add a visit for Patient Jane Doe on 2024-12-27 with mild fever and paracetamol 500 mg"
- "Show patients prescribed Paracetamol 500 mg"

Notes: The demo will translate these to SQL and execute them. Be careful — INSERT/UPDATE/DELETE statements will modify `patient.db`.

---

## Expected database schema

The app's internal prompt expects a table like `Sample_Healthcare_Data` with columns:

- NAME — TEXT
- AGE — INTEGER
- MEDICALCONDITION — TEXT
- MEDICATION — TEXT
- DATE — TEXT (YYYY-MM-DD)

The bundled `patient.db` is a demo database. Inspect the actual schema before heavy use (for example: `sqlite3 patient.db "\.schema"`).

---

## Files in this repository

- `app.py` — Main Streamlit application (prompt-to-SQL + execution + explanation).
- `sql.py` — Small example scripts that show how to read SQLite tables into pandas (utility/example code).
- `patient.db` — Example SQLite database (committed for demo purposes).
- `requirements.txt` — Python dependencies.
- `RAG .pptx` — Presentation slides related to the project.
- `.env` — Environment file (not tracked with secrets here).

---

## Security & safety warnings

- Do NOT store or commit real patient data (PHI) or other sensitive information in this repository.
- The prototype executes model-generated SQL directly against a local database. This is dangerous for production use — the model may produce unexpected or malicious SQL.
- Add robust validation and allow-listing before executing any non-SELECT SQL in real applications. Consider executing only parameterized SELECT queries automatically and requiring manual review/confirmation for DML/DDL.

---

## Recommended improvements

- Remove the committed `venv/` directory and add it to `.gitignore` to reduce repo size and avoid accidental commits of environment artifacts.
- Replace the committed `patient.db` with a small generator script (e.g., `scripts/generate_sample_db.py`) that builds a demo DB at runtime.
- Add SQL parsing/validation to disallow dangerous statements or require user confirmation for DML/DDL.
- Pin dependency versions in `requirements.txt`.
- Add tests and a CI workflow to run linting and unit tests.
- Add a LICENSE file to clarify reuse terms.

---

## Development notes

- The app uses the `google-generativeai` Python package and the `gemini-pro` model name in code. Make sure your API key has the necessary access or change the model as required.
- If the model produces SQL that references a different table name or schema, either adapt the prompt in `app.py` or inspect/rename your DB tables to match the prompt.

---

## License

No license file is included. If you want this project to be open-source, add a `LICENSE` (for example, MIT or Apache-2.0).

---

If you'd like, I can now:

- Add a `.gitignore` entry to exclude `venv/` and other artifacts.
- Replace the committed `patient.db` with a small generator script and remove the large DB from the repo.
- Pin versions in `requirements.txt` and add a simple GitHub Actions workflow to run linting/tests.

Tell me which follow-up I should do and I will commit it.