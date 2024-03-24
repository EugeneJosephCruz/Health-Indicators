# import streamlit as st
# import pandas as pd
# import numpy as np
# import datetime
# import base64
# import requests
# #added by Eugene below
# from joblib import load
# import json



# # Load the model from the saved file
# model = load("models/xgboost_diabetes_model.joblib")

# def calculate_bmi(height, weight):
#     height_m = height / 100
#     bmi = weight / (height_m ** 2)
#     return bmi

# def categorize_bmi(bmi):
#     if bmi < 18.5:
#         return 'Underweight'
#     elif 18.5 <= bmi < 25:
#         return 'Normal weight'
#     elif 25 <= bmi < 30:
#         return 'Overweight'
#     else:
#         return 'Obesity'
    
# def display_prediction_result(prediction):
#     risk_levels = {
#         0: 'Low',
#         1: 'Moderate',
#         2: 'High'
#     }
#     risk_level = risk_levels[prediction]

#     st.write(f"Based on your responses, your risk for diabetes is {risk_level}.")

#     if prediction == 0:
#         st.markdown('**Low Risk for Diabetes:**\n'
#                     'Congratulations on maintaining habits that keep your diabetes risk low. '
#                     'Remember to:\n'
#                     '- Continue engaging in regular physical activity.\n'
#                     '- Keep eating a balanced diet, rich in fruits and vegetables.\n'
#                     '- Maintain a healthy weight range.\n'
#                     '- Avoid smoking.\n'
#                     '- Limit your intake of sugary drinks.\n'
#                     '- Maintain regular checkups with a healthcare professional.')
#     elif prediction == 1:
#         st.subheader('Based on your responses, you might be at a moderate risk for prediabetes.')
#         st.markdown('**Moderate Risk for Pre-Diabetes:**\n'
#                     'It’s important to take steps now to prevent diabetes. Consider the following:\n'
#                     '- Discuss your results with a healthcare professional for personalized advice.\n'
#                     '- Increase your physical activity to at least 150 minutes per week.\n'
#                     '- Incorporate more fruits, vegetables, and whole grains into your diet.\n'
#                     '- If you’re overweight, aim for a moderate weight loss of 5-7% of your body weight.\n'
#                     '- If you smoke, seek help to quit.\n'
#                     '- Limit alcohol consumption and avoid sugary drinks.')
#     elif prediction == 2:
#         st.subheader('Based on your responses, you are at a high risk for diabetes.')
#         st.markdown('**High Risk for Diabetes:**\n'
#                     'Your assessment indicates a high risk for diabetes. It’s important to take action now:\n'
#                     '- Schedule a visit with a healthcare provider to discuss your results and possible medical interventions.\n'
#                     '- Begin or increase physical activity levels, aiming for at least 150 minutes of moderate exercise each week.\n'
#                     '- Adopt a healthy, balanced diet with limited sugar and processed foods.\n'
#                     '- If overweight, focus on achieving a healthy weight through diet and exercise.\n'
#                     '- Avoid tobacco use and limit alcohol intake.\n'
#                     '- Monitor your health regularly and follow any medical advice provided by your healthcare professionals.')

# def main():
#     st.title('Healthcast')
#     # correcting file path (Eugene)
#     st.image('assets/images/Orca logo.png', use_column_width=True)
#     st.markdown('1 in 3 US adults has prediabetes and is at high risk for type 2 diabetes. How about you?')

#     questions = [
#         {"title": "Have you ever been diagnosed with high blood pressure?", "options": ["Yes", "No"], "variable": "HighBP"},
#         {"title": "Is your cholesterol level higher than it should be?", "options": ["Yes", "No"], "variable": "HighChol"},
#         {"title": "What is your age group?", "options": ["18-24", "60-69", "80 or older"], "variable": "Age"},
#         {"title": "How would you describe your smoking habits?", "options": ["Non-smoker", "Former smoker", "Current smoker"], "variable": "Smoker"},
#         {"title": "Have you ever had a stroke?", "options": ["Yes", "No"], "variable": "Stroke"},
#         {"title": "On average, how many days in the past month have you felt physically unwell?", "options": ["0-5 days", "6-10 days", "More than 10 days"], "variable": "PhysActivity"},
#         {"title": "Have you ever suffered from a heart attack?", "options": ["Yes", "No"], "variable": "HeartDiseaseorAttack"},
#         {"title": "What is your gender?", "options": ["Male", "Female", "Prefer not to say"], "variable": "Sex"},
#         {"title": "Do you have any difficulty walking or climbing stairs?", "options": ["Yes", "No"], "variable": "DiffWalk"},
#         # BMI question formatted as you've provided will be handled separately in collect_bmi function
#     ]

    
#     user_responses = {}
#     for question in questions:
#         user_responses[question['variable']] = st.radio(question['title'], question['options'])

#     height = st.number_input("Enter your height in centimeters:", 120, 250, key="Height")
#     weight = st.number_input("Enter your weight in kilograms:", 30, 200, key="Weight")
#     if height and weight:
#         bmi = weight / ((height / 100) ** 2)
#         user_responses['BMI'] = categorize_bmi(bmi)
    
#     #

#     # Submit button for prediction and sending data to backend
#     if st.button('Submit'):
#         try:
#             # Convert responses to JSON string
#             json_data = json.dumps(user_responses)
            
#             # POST request with JSON string
#             response = requests.post("http://localhost:5000/submit", json=json_data)

#             if response.status_code == 200:
#                 response_data = response.json()
#                 prediction = response_data['model_response']
#                 # Display the prediction result
#                 display_prediction_result(prediction)
#                 st.success('Responses submitted successfully! User ID: {}'.format(response_data['user_id']))
#             else:
#                 st.error("An error occurred while submitting responses.")
#         except requests.exceptions.RequestException as e:
#             st.error(f'Request failed: {e}')


        
#         # Sending user_responses to Flask backend
#         try:
#             # Endpoint where the Flask backend is listening
#             response = requests.post("http://localhost:5000/submit", json=user_responses)
#             #response.status_code should be response_model.status_code (Eugene)
#             if response_model.status_code == 200:
#                 st.success('Responses submitted successfully!')
#             else:
#                 st.error('An error occurred while submitting responses.')
#         except requests.exceptions.RequestException as e:
#             st.error(f'Request failed: {e}')
            
#         # Clear and reset the page
#         st.button("Close and Clear", on_click=clear_session)

# def clear_session():
#     # Function to clear the session state and rerun the app
#     for key in list(st.session_state.keys()):
#         del st.session_state[key]
#     st.experimental_rerun()

# # Standard boilerplate to call the main function
# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import requests
from joblib import load
import json

# Load the model from the saved file
model = load("models/xgboost_diabetes_model.joblib")

def calculate_bmi(height_cm, weight_kg):
    """Calculate and return the Body Mass Index."""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def categorize_bmi(bmi):
    """Categorize the BMI according to predefined categories."""
    if bmi < 18.5:
        return 'Underweight'
    elif 18.5 <= bmi < 25:
        return 'Normal weight'
    elif 25 <= bmi < 30:
        return 'Overweight'
    else:
        return 'Obesity'
    
def display_prediction_result(prediction):
    """Display the prediction result in a user-friendly format."""
    risk_levels = {
        0: 'Low',
        1: 'Moderate',
        2: 'High'
    }
    risk_level = risk_levels[prediction]
    st.write(f"Based on your responses, your risk for diabetes is {risk_level}.")
    # Display additional information based on the risk level

def main():
    """The main function of the Streamlit app."""
    st.title('Healthcast Diabetes Risk Assessment')
    st.image('assets/images/Orca logo.png', use_column_width=True)
    st.markdown('1 in 3 US adults has prediabetes and is at high risk for type 2 diabetes. How about you?')

    # Questions and form to collect user input
    questions = [
        {"title": "Have you ever been diagnosed with high blood pressure?", "options": ["Yes", "No"], "variable": "HighBP"},
        {"title": "Is your cholesterol level higher than it should be?", "options": ["Yes", "No"], "variable": "HighChol"},
        {"title": "What is your age group?", "options": ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75-84", "85 or older"], "variable": "Age"},
        {"title": "How would you describe your smoking habits?", "options": ["Non-smoker", "Former smoker", "Current smoker"], "variable": "Smoker"},
        {"title": "Have you ever had a stroke?", "options": ["Yes", "No"], "variable": "Stroke"},
        {"title": "On average, how many days in the past month have you felt physically unwell?", "options": ["0-5 days", "6-10 days", "More than 10 days"], "variable": "PhysActivity"},
        {"title": "Have you ever suffered from a heart attack?", "options": ["Yes", "No"], "variable": "HeartDiseaseorAttack"},
        {"title": "What is your gender?", "options": ["Male", "Female", "Prefer not to say"], "variable": "Sex"},
        {"title": "Do you have any difficulty walking or climbing stairs?", "options": ["Yes", "No"], "variable": "DiffWalk"},
    ]

    user_responses = {}
    for question in questions:
        user_responses[question['variable']] = st.radio(question['title'], question['options'])

    height = st.number_input("Enter your height in centimeters:", 120, 250, key="Height")
    weight = st.number_input("Enter your weight in kilograms:", 30, 200, key="Weight")

    # Check for valid height and weight inputs before calculating BMI
    if height and weight:
        bmi_value = calculate_bmi(height, weight)
        user_responses['BMI'] = categorize_bmi(bmi_value)

    # Submit button for prediction and sending data to backend
    if st.button('Submit'):
        try:
            # Convert responses to JSON string
            json_data = json.dumps(user_responses)
            
            # POST request with JSON string to the '/submit' endpoint
            response = requests.post("http://localhost:5000/submit", json=json_data)

            if response.status_code == 200:
                response_data = response.json()
                prediction = response_data['model_response']
                # Display the prediction result
                display_prediction_result(prediction)
                st.success(f"Responses submitted successfully! User ID: {response_data['user_id']}")
            else:
                st.error("Failed to submit responses.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

def clear_session():
    """Clear the Streamlit session state."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

if __name__ == "__main__":
    main()
