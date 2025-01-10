from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure GenAI Key
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error("Failed to configure Gemini Pro API. Please check your API key.")
    st.stop()

# Function to load Google Gemini Model and provide queries as responses
def get_gemini_response(question, prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content([prompt[0], question])
        return response.text
    except Exception as e:
        st.error("Error in generating a response from Gemini Pro. Please try again.")
        print(f"Error: {e}")
        return None

# Function to retrieve query results from the database

#query parser check if sql is dml or ddl
#if ddl :
#read_sql_query(sql, db)
#else
#new dml read query
#update database only if no duplicates are there . If there are duplicates then send message to provide all details like precription and date visited.
#if only one record found only then update or delete.

def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.Error as e:
        st.error("Database query failed. Please check your SQL statement or database connection.")
        print(f"SQLite Error: {e}")
        return None

# Function to generate human-readable responses based on the query result and user input
# Function to generate human-readable responses based on the query result, user input, and the SQL query
def generate_human_readable_response(question, sql_query, query_result):
    
    try:
        # Use Gemini Pro to interpret the result in human-readable format
        prompt2 = [
            f"""
            You are an expert assistant. Based on the user's question: '{question}', the SQL query generated: '{sql_query}', 
            and the query result: {query_result}, provide a friendly, human-readable interpretation. 
            Your response should:
            - Clearly interpret the query result in simple and understandable language.
            - If the query was an update or modification, confirm the changes made.
            - If no records are found, politely inform the user.
            - Avoid using technical SQL language and focus on a user-friendly explanation.
            """
        ]
        response = get_gemini_response(question, prompt2)
        return response
    except Exception as e:
        st.error("Failed to generate a human-readable response. Please try again.")
        print(f"Error: {e}")
        return "An error occurred while generating the response."


# Define your prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name Sample_Healthcare_Data and has the following columns (
        "NAME" TEXT,
        "AGE" INTEGER,
        "MEDICALCONDITION" TEXT,
        "MEDICATION" TEXT,
        "DATE" TEXT
    );

    For example:

    Example 1 - Update Patient X’s record: add visit on Dec 27, 2024, with a diagnosis of mild fever and prescription of paracetamol 500 mg.,
    The SQL command will be something like this:
    INSERT INTO Sample_Healthcare_Data (
        NAME, 
        AGE, 
        MEDICALCONDITION, 
        MEDICATION, 
        DATE
    ) 
    VALUES (
        'Patient X',  -- Replace 'Patient X' with the actual patient's name
        NULL,         -- AGE if not given, use NULL
        'Mild Fever', -- MedicalCondition
        'Paracetamol 500 mg', -- Medication
        '2024-12-27'  -- Date in YYYY-MM-DD format
    );

    Example 2 - Find Patient X’s record,
    The SQL command will be something like this:
    SELECT * FROM Sample_Healthcare_Data WHERE NAME = 'Patient X';

    Example 3 - Set the age of Patient X to the same for every record if it is provided in one record,
    The SQL command will be something like this:
    UPDATE Sample_Healthcare_Data
    SET AGE = (SELECT AGE FROM Sample_Healthcare_Data WHERE NAME = 'Patient X' AND AGE IS NOT NULL)
    WHERE NAME = 'Patient X';

    Example 4 - Delete all records of Patient Y,
    The SQL command will be something like this:
    DELETE FROM Sample_Healthcare_Data WHERE NAME = 'Patient Y';

    Example 5 - Add medication details for Patient Z who is already in the database,
    The SQL command will be something like this:
    UPDATE Sample_Healthcare_Data
    SET MEDICALCONDITION = 'Hypertension',
        MEDICATION = 'Amlodipine 5 mg'
    WHERE NAME = 'Patient Z';

    Example 6 - Retrieve the names and medical conditions of all patients who have been prescribed a specific medication (e.g., 'Paracetamol 500 mg'),
    The SQL command will be something like this:
    SELECT NAME, MEDICALCONDITION 
    FROM Sample_Healthcare_Data 
    WHERE MEDICATION = 'Paracetamol 500 mg';
    also the sql code should not have ``` in beginning or end and sql word in output
    Ensure that all SQL commands generated align with the above structure and formatting, and avoid using unnecessary comments or formatting like backticks (`) or the keyword "SQL" in the output.
    """
]

# Streamlit App
st.set_page_config(page_title="I Can Retrieve Any SQL Data")
st.header("App to Retrieve SQL Data")

question = st.text_input("Enter your query:", key="input")
submit = st.button("Ask the question")

# If the submit button is clicked
if submit:
    if not question.strip():
        st.warning("Please enter a valid query.")
    else:
        # Get the SQL response from Gemini
        # Step1 - Generate query 
        response = get_gemini_response(question, prompt)
        if response:
            # Execute the SQL query
            
            data = read_sql_query(response, "patient.db")
                # Generate a human-readable response
            friendly_response = generate_human_readable_response(question,response, data)
            st.subheader("Response")
            st.write(friendly_response)
            