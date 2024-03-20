import streamlit as st
import pandas as pd
import numpy as np
from joblib import load
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc

# Assuming you have a function to calculate BMI from height and weight
def calculate_bmi(height_in_cm, weight_in_kg):
    # Implement BMI calculation: weight (kg) / (height (m))^2
    height_in_m = height_in_cm / 100
    bmi = weight_in_kg / (height_in_m**2)
    return bmi

# Load the model from the saved file
model = load("xgboost_diabetes_model.joblib")

# Function to get user input for each feature
def user_input_features():
    st.title('Healthcast Diabetes Risk Prediction')

    # Add your logo and introduction
    st.image('C:\Users\gosmi\Pictures\Orca logo.png', use_column_width=True)
    st.write('1 in 3 US adults has prediabetes and is at high risk for type 2 diabetes. How about you?')

    # Initialize an empty dictionary for the features
    features = {}

    # For simplicity, adding features with user input
    # In your actual code, you'd split these into separate pages with st.form or similar
    features['HighBP'] = st.radio('Have you ever been diagnosed with high blood pressure?', ('Yes', 'No'))
    features['HighChol'] = st.radio('Is your cholesterol level higher than it should be?', ('Yes', 'No'))
    # Continue this for all features...
    
    # For BMI, calculate from height and weight
    height = st.number_input('Enter your height (in cm):', min_value=120, max_value=250)
    weight = st.number_input('Enter your weight (in kg):', min_value=40, max_value=200)
    features['BMI'] = calculate_bmi(height, weight)

    # Convert responses to numerical format based on your data dictionary
    # For example, if 'Yes' = 1 and 'No' = 0 in your dataset:
    for feature in features:
        if features[feature] == 'Yes':
            features[feature] = 1
        elif features[feature] == 'No':
            features[feature] = 0

    # Convert dictionary to dataframe
    features_df = pd.DataFrame.from_dict([features])
    
    # Standardize the data
    scaler = StandardScaler()
    features_df_scaled = scaler.fit_transform(features_df)

    return features_df_scaled

# Sidebar for navigation
with st.sidebar:
    st.title("Navigation")
    start_analysis = st.button('Start Risk Analysis')

# Main page
if start_analysis:
    user_data = user_input_features()
    prediction = model.predict(user_data)
    prediction_proba = model.predict_proba(user_data)


# Assuming you've already asked questions and collected user responses

# Display the prediction result
if prediction[0] == 0:
    st.subheader('Based on your responses, your risk for diabetes is low.')
    st.markdown('**Low Risk for Diabetes:**\n'
                'Congratulations on maintaining habits that keep your diabetes risk low. '
                'Remember to:\n'
                '- Continue engaging in regular physical activity.\n'
                '- Keep eating a balanced diet, rich in fruits and vegetables.\n'
                '- Maintain a healthy weight range.\n'
                '- Avoid smoking.\n'
                '- Limit your intake of sugary drinks.\n'
                '- Maintain regular checkups with a healthcare professional.')
elif prediction[0] == 1:
    st.subheader('Based on your responses, you might be at a moderate risk for prediabetes.')
    st.markdown('**Moderate Risk for Pre-Diabetes:**\n'
                'It’s important to take steps now to prevent diabetes. Consider the following:\n'
                '- Discuss your results with a healthcare professional for personalized advice.\n'
                '- Increase your physical activity to at least 150 minutes per week.\n'
                '- Incorporate more fruits, vegetables, and whole grains into your diet.\n'
                '- If you’re overweight, aim for a moderate weight loss of 5-7% of your body weight.\n'
                '- If you smoke, seek help to quit.\n'
                '- Limit alcohol consumption and avoid sugary drinks.')
elif prediction[0] == 2:
    st.subheader('Based on your responses, you are at a high risk for diabetes.')
    st.markdown('**High Risk for Diabetes:**\n'
                'Your assessment indicates a high risk for diabetes. It’s important to take action now:\n'
                '- Schedule a visit with a healthcare provider to discuss your results and possible medical interventions.\n'
                '- Begin or increase physical activity levels, aiming for at least 150 minutes of moderate exercise each week.\n'
                '- Adopt a healthy, balanced diet with limited sugar and processed foods.\n'
                '- If overweight, focus on achieving a healthy weight through diet and exercise.\n'
                '- Avoid tobacco use and limit alcohol intake.\n'
                '- Monitor your health regularly and follow any medical advice provided by your healthcare professionals.')

# Optionally, show the probabilities for each class
st.subheader('Prediction Probabilities:')
st.write(f'Low Risk: {prediction_proba[0][0] * 100:.2f}%')
st.write(f'Moderate Risk: {prediction_proba[0][1] * 100:.2f}%')
st.write(f'High Risk: {prediction_proba[0][2] * 100:.2f}%')


