# 4Geeks Data Science and Machine Learning Capstone-Project

**_Healthcast_ - Diabetes Risk Calculator Team Project**

This project involves the creation of a risk calculator for diabetes. It involves creating a Classification model in Python.

The **tech stack** includes Pandas, Scikit Learn, SQLite, Joblib, Streamlit, GitHub, and Render.

The app can be viewed on Render.com [here](https://healthcastdiabetesrisk.streamlit.app/)

**Introduction:**

The _Healthcast_ application aims to assess diabetes risk for patients and healthcare providers (HCPs) through an interactive questionnaire. By leveraging various machine learning techniques, we have developed a robust risk calculator to aid in proactive health management.

**Background:**

In the development process, we established benchmarking criteria to ensure the reliability and accuracy of our risk calculator model. We leveraged the Diabetes Risk Score.

The data set is from the Centers for Disease Control (CDC) and uses survey data. It has 253680 rows and 22 columns.

Addressing the challenge of imbalanced data in our dataset, we explored techniques such as class weights and synthetic data generation, specifically utilizing SMOTE (Synthetic Minority Over-sampling Technique).

To determine the most effective algorithm for our task, we evaluated several machine learning models, including Decision Trees, Gradient Boosting, Support Vector Machines, and Deep Neural Networks. Through comprehensive analysis, we sought to identify the algorithm that best balances predictive accuracy with computational efficiency for real-world application.

Enjoy!


Directory structure
/my_streamlit_project
    /data
    /models
    /notebooks
    /scripts
        preprocess_data.py
        train_model.py
    /components
    /static
        /images
        style.css
    /templates
    app.py
    requirements.txt
    README.md
    .gitignore
    Dockerfile (optional)
    Procfile (optional)
