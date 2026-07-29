# RAG-to-SQL

A small Streamlit application that demonstrates using a retrieval-augmented generation (RAG) style approach to convert natural-language questions into SQL, execute those queries against a local SQLite database, and return human-readable explanations of results using Google Gemini (Generative AI).

> Warning: This repository contains a sample `patient.db` SQLite database. Do NOT use real patient data or other sensitive personal data in this repository. The included database is intended for demonstration only.

## Repository structure

- app.py — Streamlit app that accepts a natural-language question, uses Google Gemini to generate SQL, runs the SQL against `patient.db`, and asks Gemini to generate a friendly explanation.
- sql.py — Small scripts that demonstrate reading from SQLite databases into pandas (unused by the Streamlit app, example/utility).
- patient.db — Sample SQLite database used by the app (committed for demo purposes).
- requirements.txt — Python dependencies.
- RAG .pptx — A presentation file (slides) related to the project.
- .env — Environment file (not tracked with any secrets here in the repo snapshot).
- venv/ — A committed virtual environment directory (should be removed from the repo; see Security & Cleanup below).

## What this does

- Accepts an English question via a Streamlit UI.
- Uses the Google Generative AI (Gemini) API to translate the question into an SQL statement that matches the expected schema.
- Executes the generated SQL against `patient.db`.
- Uses Gemini again to create a human-friendly summary/explanation of the query result.

## Expected database schema

The app is written to work with a table shaped like the following (named in prompts as `Sample_Healthcare_Data`):

- NAME — TEXT
- AGE — INTEGER
- MEDICALCONDITION — TEXT
- MEDICATION — TEXT
- DATE — TEXT (YYYY-MM-DD)

Note: The real `patient.db` bundled in the repo may use different table names; the app's prompt and SQL generation assume the schema above. Inspect `patient.db` with the sqlite3 CLI or a GUI tool if you need to adapt the prompt or table names.

## Requirements

- Python 3.8+
- An API key for Google Generative AI (Gemini) with access to the `gemini-pro` model.

Install dependencies:

pip install -r requirements.txt

## Environment

Create a `.env` file in the repo root (or set the environment variable directly) with:

GOOGLE_API_KEY=your_google_generative_ai_api_key

Do NOT commit secrets to the repository.

## Run the demo

1. Install requirements: `pip install -r requirements.txt`
2. Ensure `patient.db` is present in the repo root (it is included here for demo purposes).
3. Add your Google API key to `.env` as shown above.
4. Start the Streamlit app:

streamlit run app.py

5. In the browser UI, type a natural-language question about the sample healthcare data (for example: "Find records for Patient X" or "Add a visit for Patient Y on 2024-12-27 with mild fever and paracetamol 500 mg") and click "Ask the question".

If Gemini generates an UPDATE/INSERT/DELETE statement, the app will run it against the SQLite database — be cautious when experimenting.

## Notes, limitations and suggestions

- The current implementation relies on the model to produce valid SQL and does not fully validate or sanitize generated SQL. This is risky for production use. For real applications, implement strict validation, parameterization, and allow-listing of permitted SQL commands.
- The app expects the schema described above. If your database differs, update the `prompt` in `app.py` and/or inspect and modify the SQL execution logic.
- Committed virtual environments (`venv/`) and databases are discouraged in version control. Consider removing `venv/` and adding it to `.gitignore`.
- The app uses Gemini Pro (`gemini-pro`) model in the code. Ensure your API key has appropriate access, or change the model name as needed.

## Security

- Do NOT put real PHI (Protected Health Information) or secrets in this repository.
- Do validation and escaping of any generated SQL before executing it in production.

## How to improve

- Add SQL parsing and validation to accept only safe SELECT statements in read-only mode, or require explicit user confirmation for DML/DDL operations.
- Replace the direct execution of generated SQL with a parameterized query builder or mapping layer.
- Add unit tests and CI to verify the prompt-to-SQL behavior and database safety.

## License

This repository has no license file. Add a LICENSE if you want to specify usage terms.

