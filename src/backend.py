from flask import Flask, request, jsonify
import sqlite3
from flask_cors import cors
from joblib import load


# Load the model from the saved file
model = load("xgboost_diabetes_model.joblib")


app = Flask(__name__)
Healthcast_Survey = "diabetes_risk_assessments.db"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(Healthcast_Survey)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table():
    conn = create_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS assessments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        HighBP TEXT,
                        HighChol TEXT,
                        BMI REAL,
                        Smoker TEXT,
                        Stroke TEXT,
                        HeartDiseaseorAttack TEXT,
                        PhysActivity TEXT,
                        DiffWalk TEXT,
                        Sex TEXT,
                        Age TEXT,
                        risk_level TEXT)''')

def insert_assessment(user_responses):
    conn = create_connection()
    with conn:
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO assessments(timestamp,HighBP,HighChol,BMI,Smoker,Stroke,HeartDiseaseorAttack,PhysActivity,DiffWalk,Sex,Age,risk_level)
                           VALUES(:Timestamp,:HighBP,:HighChol,:BMI,:Smoker,:Stroke,:HeartDiseaseorAttack,:PhysActivity,:DiffWalk,:Sex,:Age,:risk_level)''', user_responses)
        return cursor.lastrowid

@app.route('/submit', methods=['POST'])
def submit_responses():
    user_responses = request.json
    user_id = insert_assessment(user_responses)
    return jsonify({"message": "Responses submitted successfully", "user_id": user_id}), 200

@app.route('/predict', methods=['POST'])
def submit_model_response():
    user_responses = request.json
    model_response = model.predict(user_responses)[0]

    return jsonify({"message": "Responses submitted successfully", "model_response": model_response}), 200


    
if __name__ == "__main__":
    create_table() # Ensure the table is created on startup
    app.run(debug=True, port=5000)

