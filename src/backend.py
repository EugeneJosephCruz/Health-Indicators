import sqlite3
import joblib
import pandas as pd
from datetime import datetime

# Load the model and scaler
model = joblib.load("models/xgboost_diabetes_model.joblib")
scaler = joblib.load('models/fitted_scaler.joblib')

db_file = "diabetes_risk_assessments.db"

def create_connection():
    """Create and return a database connection."""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def create_table():
    """Create the database table if it doesn't exist."""
    conn = create_connection()
    with conn:
        sql = '''CREATE TABLE IF NOT EXISTS assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    HighBP INTEGER,
                    HighChol INTEGER,
                    BMI INTEGER,
                    Smoker INTEGER,
                    Stroke INTEGER,
                    HeartDiseaseorAttack INTEGER,
                    PhysActivity INTEGER,
                    DiffWalk INTEGER,
                    Sex INTEGER,
                    Age INTEGER,
                    risk_level INTEGER)'''
        conn.execute(sql)
        print("Table created")

def insert_assessment(user_responses):
    """Insert a new row into the assessments table."""
    conn = create_connection()
    with conn:
        sql = ''' INSERT INTO assessments(timestamp, HighBP, HighChol, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, DiffWalk, Sex, Age, risk_level)
                  VALUES(:timestamp, :HighBP, :HighChol, :BMI, :Smoker, :Stroke, :HeartDiseaseorAttack, :PhysActivity, :DiffWalk, :Sex, :Age, :risk_level) '''
        cur = conn.cursor()
        cur.execute(sql, user_responses)
        return cur.lastrowid

def make_prediction(user_responses):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Specify the column order explicitly for prediction
    columns_order = ['HighBP', 'HighChol', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'DiffWalk', 'Sex', 'Age']
    df = pd.DataFrame([user_responses], columns=columns_order)
    print(f'df unscaled: {df}')
    df_scaled = scaler.transform(df)
    print(f'df_scaled: {df_scaled}')
    prediction = model.predict(df_scaled)[0]

    # Convert numpy.int64 to native Python int for JSON serialization
    prediction = int(prediction)

    # Add 'timestamp' and 'risk_level' for database insertion
    user_responses_for_db = user_responses.copy()
    user_responses_for_db['timestamp'] = timestamp
    user_responses_for_db['risk_level'] = prediction

    user_id = insert_assessment(user_responses_for_db)
    return prediction, user_id

# Ensure the table is created on import
create_table()


# from flask import Flask, request, jsonify
# import sqlite3
# from flask_cors import CORS
# from joblib import load
# import joblib
# import pandas as pd
# import datetime
# import json
# from sklearn.preprocessing import StandardScaler

# # Load the model from the saved file
# model = load("models/xgboost_diabetes_model.joblib")

# # Load the fitted StandardScaler
# scaler = joblib.load('models/fitted_scaler.joblib')

# app = Flask(__name__)
# CORS(app)
# db_file = "diabetes_risk_assessments.db"

# def create_connection():
#     """Create and return a database connection."""
#     try:
#         conn = sqlite3.connect(db_file)
#         return conn
#     except sqlite3.Error as e:
#         print(e)
#     return None

# def create_table():
#     """Create the database table if it doesn't exist."""
#     conn = create_connection()
#     with conn:
#         sql = '''CREATE TABLE IF NOT EXISTS assessments (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     timestamp TEXT,
#                     HighBP INTEGER,
#                     HighChol INTEGER,
#                     BMI INTEGER,
#                     Smoker INTEGER,
#                     Stroke INTEGER,
#                     HeartDiseaseorAttack INTEGER,
#                     PhysActivity INTEGER,
#                     DiffWalk INTEGER,
#                     Sex INTEGER,
#                     Age INTEGER,
#                     risk_level INTEGER)'''
#         conn.execute(sql)
#         print("Table created")

# def insert_assessment(user_responses):
#     """Insert a new row into the assessments table."""
#     conn = create_connection()
#     with conn:
#         sql = ''' INSERT INTO assessments(timestamp, HighBP, HighChol, BMI, Smoker, Stroke, HeartDiseaseorAttack, PhysActivity, DiffWalk, Sex, Age, risk_level)
#                   VALUES(:timestamp, :HighBP, :HighChol, :BMI, :Smoker, :Stroke, :HeartDiseaseorAttack, :PhysActivity, :DiffWalk, :Sex, :Age, :risk_level) '''
#         cur = conn.cursor()
#         cur.execute(sql, user_responses)
#         return cur.lastrowid
    
# @app.route('/submit', methods=['POST'])
# def submit_responses():
#     user_responses = request.get_json()
#     user_responses = json.loads(user_responses)
#     print(f"user_responses is: {user_responses}")
#     if not isinstance(user_responses, dict):
#         print("Error: Received data is not a dictionary")
#         return jsonify({"error": "Invalid input format"}), 400

#     print("Received user responses:", user_responses)

#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#     # Specify the column order explicitly for prediction
#     columns_order = ['HighBP', 'HighChol', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack', 'PhysActivity', 'DiffWalk', 'Sex', 'Age']
#     df = pd.DataFrame([user_responses], columns=columns_order)
#     print(f'Original df: {df}')
#     df_scaled = scaler.transform(df)
#     print(f'Transformed df: {df_scaled}')
#     #print("DataFrame created from user responses:\n", df)

#     try:
#         prediction = model.predict(df_scaled)[0]
#         print("Prediction made:", prediction)

#         # Convert numpy.int64 to native Python int for JSON serialization
#         prediction = int(prediction)

#         # Add 'timestamp' and 'risk_level' for database insertion
#         user_responses_for_db = user_responses.copy()
#         user_responses_for_db['timestamp'] = timestamp
#         user_responses_for_db['risk_level'] = prediction

#         user_id = insert_assessment(user_responses_for_db)
#         print(f"Assessment inserted with ID {user_id}")

#         return jsonify({
#             "message": "Responses submitted and prediction made successfully",
#             "user_id": user_id,
#             "model_response": prediction
#         }), 200
#     except Exception as e:
#         print("Error during prediction or database insertion:", str(e))
#         return jsonify({"error": str(e)}), 500
