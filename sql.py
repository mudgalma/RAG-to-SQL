import sqlite3
import pandas as pd

# Connect to SQLite database
conn = sqlite3.connect('patient.db')

# Query data and load into a DataFrame
query = "SELECT * FROM healthcare_dataset"
df = pd.read_sql_query(query, conn)

# Print the DataFrame
print(df)

# Close the connection
conn.close()

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('patient_data.db')
cursor = conn.cursor()

# Query data
cursor.execute("SELECT * FROM healthcare_datas")
rows = cursor.fetchall()

# Print results
for row in rows:
    print(row)

# Close the connection
conn.close()

