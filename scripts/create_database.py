import pandas as pd
import sqlite3
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
import os

try:
    print("Reading the CSV file...")
    df = pd.read_csv('./data/diabetes_012_health_indicators_BRFSS2015.csv')
    print("CSV file has been read successfully.")

    print("Absolute path to CSV file:", os.path.abspath('./data/diabetes_012_health_indicators_BRFSS2015.csv'))
    print("Absolute path to SQLite DB file:", os.path.abspath('./data/diabetes_data.db'))


    print("Establishing a connection to the SQLite database...")
    conn = sqlite3.connect('./data/diabetes_data.db')
    print("Connection established.")

    print("Creating the 'diabetes_raw' table and inserting data...")
    df.to_sql('diabetes_raw', conn, if_exists='replace', index=False)
    print("'diabetes_raw' table created and data inserted.")

    # Preprocessing for SMOTE
    # ... Your preprocessing code here ...
    
    print("Applying SMOTE...")
    

    X_train, X_test, y_train, y_test = train_test_split(
            df.drop('Outcome', axis=1), df['Outcome'], test_size=0.2, random_state=42)

    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_train, y_train)
    print("SMOTE applied successfully.")

    print("Creating a new DataFrame from the resampled data...")
    df_resampled = pd.DataFrame(X_res, columns=df.columns[:-1])
    df_resampled['Outcome'] = y_res
    print("New DataFrame created.")

    
    
    print("Creating the 'diabetes_balanced' table and inserting balanced data...")
    df_resampled.to_sql('diabetes_balanced', conn, if_exists='replace', index=False)
    print("'diabetes_balanced' table created and data inserted.")

    

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the connection if it's open
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")

# testing to see if tables were successfully created
try:
    print("Re-establishing connection to database to verify tables...")
    conn = sqlite3.connect('./data/diabetes_data.db')
    print("Connection re-established.")

    print("Retrieving data from 'diabetes_raw' table...")
    print(pd.read_sql_query("SELECT * FROM diabetes_raw LIMIT 5", conn))
    print("Data retrieved successfully.")

    print("Retrieving data from 'diabetes_balanced' table...")
    print(pd.read_sql_query("SELECT * FROM diabetes_balanced LIMIT 5", conn))
    print("Data retrieved successfully.")

except Exception as e:
    print(f"An error occurred while retrieving data: {e}")

finally:
    # Close the connection if it's open
    if 'conn' in locals():
        conn.close()
        print("Database connection closed.")
