from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from joblib import load
# Must import json to use requests.post (Eugene)
import json
import pandas as pd



# Load the model from the saved file
#corrected the file path on this next line (Eugene)
model = load("models/xgboost_diabetes_model.joblib")


app = Flask(__name__)
#added this next line (Eugene)
CORS(app)
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

# NOTE: Previous implementation involved making two separate POST requests to the backend — 
# one to the '/predict' endpoint for obtaining a prediction and another to the '/submit' 
# endpoint for storing user responses. To improve efficiency and ensure consistency between 
# prediction and data storage, these two operations have been combined into a single POST request. 
# Now, the '/submit' endpoint handles the prediction internally and saves the user responses 
# in one go, thereby reducing network overhead and simplifying error handling.

@app.route('/submit', methods=['POST'])
def submit_responses():
    user_responses = request.json
    # Convert the JSON to the appropriate format for prediction
    df = pd.DataFrame([user_responses])
    # Perform prediction
    prediction = model.predict(df)[0]
    # Insert the assessment to the database
    user_id = insert_assessment(user_responses)
    # Return both the user_id and the prediction
    return jsonify({"message": "Responses submitted and prediction made successfully", 
                    "user_id": user_id, 
                    "model_response": prediction}), 200


    
if __name__ == "__main__":
    create_table() # Ensure the table is created on startup
    app.run(debug=True, port=5000)

