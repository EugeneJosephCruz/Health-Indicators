import streamlit as st
import requests
from joblib import load
import json

# Load the model from the saved file
model = load("models/xgboost_daiabetes_model.joblib")

def calculate_bmi(height_ft, height_in, weight_lbs):
    print("Calculating BMI...")
    total_height_in = height_ft * 12 + height_in  # Convert feet and inches to inches
    height_cm = total_height_in * 2.54  # Convert inches to centimeters
    weight_kg = weight_lbs * 0.453592  # Convert pounds to kilograms
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    print(f"Calculated BMI: {bmi}")
    return bmi

def clear_session():
    print("Clearing session...")
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()


def display_prediction_result(prediction):
    """Display the prediction result in a user-friendly format."""

    risk_levels = {
        0: 'Low',
        1: 'Moderate',
        2: 'High'
    }
    risk_level = risk_levels[prediction]

    st.write(f"Based on your responses, your risk for diabetes is {risk_level}.")

    if prediction == 0:
        st.markdown('**Low Risk for Diabetes:**\n'
                    'Congratulations on maintaining habits that keep your diabetes risk low. '
                    'Remember to:\n'
                    '- Continue engaging in regular physical activity.\n'
                    '- Keep eating a balanced diet, rich in fruits and vegetables.\n'
                    '- Maintain a healthy weight range.\n'
                    '- Avoid smoking.\n'
                    '- Limit your intake of sugary drinks.\n'
                    '- Maintain regular checkups with a healthcare professional.')
    elif prediction == 1:
        st.subheader('Based on your responses, you might be at a moderate risk for prediabetes.')
        st.markdown('**Moderate Risk for Pre-Diabetes:**\n'
                    'It’s important to take steps now to prevent diabetes. Consider the following:\n'
                    '- Discuss your results with a healthcare professional for personalized advice.\n'
                    '- Increase your physical activity to at least 150 minutes per week.\n'
                    '- Incorporate more fruits, vegetables, and whole grains into your diet.\n'
                    '- If you’re overweight, aim for a moderate weight loss of 5-7% of your body weight.\n'
                    '- If you smoke, seek help to quit.\n'
                    '- Limit alcohol consumption and avoid sugary drinks.')
    elif prediction == 2:
        st.subheader('Based on your responses, you are at a high risk for diabetes.')
        st.markdown('**High Risk for Diabetes:**\n'
                    'Your assessment indicates a high risk for diabetes. It’s important to take action now:\n'
                    '- Schedule a visit with a healthcare provider to discuss your results and possible medical interventions.\n'
                    '- Begin or increase physical activity levels, aiming for at least 150 minutes of moderate exercise each week.\n'
                    '- Adopt a healthy, balanced diet with limited sugar and processed foods.\n'
                    '- If overweight, focus on achieving a healthy weight through diet and exercise.\n'
                    '- Avoid tobacco use and limit alcohol intake.\n'
                    '- Monitor your health regularly and follow any medical advice provided by your healthcare professionals.')

def main():

    st.title('Healthcast Diabetes Risk Assessment')
    st.image('static/images/Orca logo.png', use_column_width=True)
    st.markdown('1 in 3 US adults has prediabetes and is at high risk for type 2 diabetes. How about you?')

    # Questions and form to collect user input
    questions = [
        {"title": "Have you ever been diagnosed with high blood pressure?", "options": ["Yes", "No"], "variable": "HighBP"},
        {"title": "Is your cholesterol level higher than it should be?", "options": ["Yes", "No"], "variable": "HighChol"},
        {"title": "What is your age group?", "options": ["18-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80 or older"], "variable": "Age"},
        {"title": "Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]", "options": ["Yes", "No"], "variable": "Smoker"},
        {"title": "Have you ever had a stroke?", "options": ["Yes", "No"], "variable": "Stroke"},
        {"title": "In the past 30 days, excluding your job, did you participate in any physical activities or exercises such as running, calisthenics, golf, gardening, or walking for exercise?", "options": ["Yes", "No"], "variable": "PhysActivity"},
        {"title": "Have you ever had a heart attack or have coronary heart disease?", "options": ["Yes", "No"], "variable": "HeartDiseaseorAttack"},
        {"title": "What is your Sex?", "options": ["Male", "Female"], "variable": "Sex"},
        {"title": "Do you have any difficulty walking or climbing stairs?", "options": ["Yes", "No"], "variable": "DiffWalk"},
    ]

    age_mapping = {
        "18-24": 1,
        "25-29": 2,
        "30-34": 3,
        "35-39": 4,
        "40-44": 5,
        "45-49": 6,
        "50-54": 7,
        "55-59": 8,
        "60-64": 9,
        "65-69": 10,
        "70-74": 11,
        "75-79": 12,
        "80 or older": 13
    }

    

    # 'Male' is mapped to 1 and 'Female' to 0 based on model training
    sex_mapping = {
        "Male": 1,
        "Female": 0
    }

    binary_questions = ["HighBP", "HighChol", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "DiffWalk", "Sex"]

    user_responses = {}
    for question in questions:
        response = st.radio(question['title'], question['options'], key=question['variable'])
        if question['variable'] in binary_questions:
            if question['variable'] == 'Sex':
                user_responses[question['variable']] = sex_mapping[response]
            else:
                user_responses[question['variable']] = 1 if response == 'Yes' else 0
        elif question['variable'] == 'Age':
            user_responses[question['variable']] = age_mapping[response]
        else:
            user_responses[question['variable']] = response

    col1, col2 = st.columns(2)
    with col1:
        height_ft = st.number_input("Enter your height (feet):", min_value=4, max_value=7, key="Height_ft")
    with col2:
        height_in = st.number_input("Enter your height (inches):", min_value=0, max_value=11, key="Height_in")
    weight_lbs = st.number_input("Enter your weight (pounds):", min_value=50, max_value=400, key="Weight_lbs")

    # Check if height and weight inputs are provided before calculating BMI
    if height_ft and weight_lbs:
        bmi_value = calculate_bmi(height_ft, height_in, weight_lbs)
        user_responses['BMI'] = int(bmi_value)

    if st.button('Submit'):
        print("Submitting responses...")
        try:
            # Convert responses to JSON string for the POST request
            json_data = json.dumps(user_responses)
            print(f"Sending JSON data to backend: {json_data}")
            response = requests.post("http://localhost:5000/submit", json=json_data)
            if response.status_code == 200:
                response_data = response.json()
                prediction = response_data['model_response']
                display_prediction_result(prediction)
                st.success(f"Responses submitted successfully! User ID: {response_data.get('user_id')}")
            else:
                st.error(f"Failed to submit responses. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

    if st.button('Clear & Restart'):
        clear_session()

if __name__ == "__main__":
    main()
