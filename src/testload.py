import joblib

# Define the path to the model file
model_file_path = "models/xgboost_diabetes_model.joblib"

# Load the model from the file
try:
    model = joblib.load(model_file_path)
    print("Model loaded successfully!")
    # Now you can use the model object for predictions or whatever you need
except FileNotFoundError:
    print(f"Error: The file {model_file_path} does not exist.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
