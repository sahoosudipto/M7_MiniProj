import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import gradio
from fastapi import FastAPI, Request, Response

import random
import numpy as np
import pandas as pd
import os
import pickle
# import xgboost as xgb


# Define model path
# MODEL_PATH = os.path.join('models', 'xgboost-model.pkl')
# MODEL_PATH = root / 'models' / 'xgboost-model.pkl'
MODEL_PATH = os.path.join(root, 'models', 'xgboost-model.pkl')


# Load the model
def load_model():
    try:
        print(f'parent:{parent} root:{root}')
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        raise Exception(f"Model file not found at {MODEL_PATH}")
    except Exception as e:
        raise Exception(f"Error loading model: {str(e)}")

# Load model at startup
try:
    xgb_trained = load_model()
except Exception as e:
    print(f"Error: {str(e)}")
    exit(1)

def predict_death_event(age, anaemia, high_blood_pressure, creatinine_phosphokinase, 
                       diabetes, ejection_fraction, platelets, sex, 
                       serum_creatinine, serum_sodium, smoking, time):
    """Function to predict survival of patients with heart failure"""
    try:
        # Convert inputs
        input_data = preprocess_inputs(
            age, anaemia, high_blood_pressure, creatinine_phosphokinase,
            diabetes, ejection_fraction, platelets, sex,
            serum_creatinine, serum_sodium, smoking, time
        )
        
        # Make prediction
        prediction = xgb_trained.predict(input_data)[0]
        result = "High Risk" if prediction == 1 else "Low Risk"
        return result
    except Exception as e:
        return f"Error making prediction: {str(e)}"

def preprocess_inputs(*args):
    """Preprocess input values"""
    def convert_binary(value):
        if value in ["Yes", "Male"]:
            return 1
        elif value in ["No", "Female"]:
            return 0
        return float(value)
    
    # Convert all inputs
    processed = [convert_binary(arg) for arg in args]
    
    # Convert to numpy array with correct shape and type
    return np.array(processed, dtype=np.float32).reshape(1, -1)




# FastAPI object
app = FastAPI()


# UI - Input components

in_Age =  gradio.Slider(minimum=0, maximum=100, label="Age")
in_Anaemia = gradio.Radio(["Yes", "No"], label="Anaemia")
in_CP = gradio.Slider(minimum=0, maximum=1000, label="Creatinine Phosphokinase")
in_Diabetes = gradio.Radio(["Yes", "No"], label="Diabetes")
in_Ejection = gradio.Slider(minimum=0, maximum=100, label="Ejection Fraction")
in_HBP = gradio.Radio(["Yes", "No"], label="High Blood Pressure")
in_Platelets = gradio.Slider(minimum=0, maximum=1000000, label="Platelets")
in_SC = gradio.Slider(minimum=0, maximum=100,  label="Serum Creatinine")
in_SS = gradio.Slider(minimum=0, maximum=100, label="Serum Sodium")
in_Sex = gradio.Radio(["Male", "Female"], label="Sex")
in_Smoking = gradio.Radio(["Yes", "No"], label="Smoking")
in_Time = gradio.Slider(minimum=0, maximum=100,label="Time")


# UI - Output component
out_label = gradio.Textbox(type="text", label='Prediction', elem_id="out_textbox")
# outputs = gradio.Textbox(label="Prediction")


# # Label prediction function
# def predict_death_event(in_Age, in_Anaemia, in_CP, in_Diabetes, in_Ejection, in_HBP, in_Platelets, in_SC, in_SS, in_Sex, in_Smoking, in_Time):
#     pass


# def convert_binary(value):
#     """Convert Yes/No and Male/Female to binary"""
#     if value in ["Yes", "Male"]:
#         return 1
#     elif value in ["No", "Female"]:
#         return 0
#     return value

# def predict_death_event(age, anaemia, creatinine_phosphokinase, diabetes, ejection_fraction, high_blood_pressure, platelets, serum_creatinine, serum_sodium, sex, smoking, time):
#     """Function to predict survival of patients with heart failure"""
    
#     # Convert categorical inputs to numeric
#     anaemia = convert_binary(anaemia)
#     diabetes = convert_binary(diabetes)
#     high_blood_pressure = convert_binary(high_blood_pressure)
#     sex = convert_binary(sex)
#     smoking = convert_binary(smoking)
    
#     # Create input array with explicit dtype
#     input_data = np.array([
#         age, anaemia, high_blood_pressure, creatinine_phosphokinase,
#         diabetes, ejection_fraction, platelets, sex, serum_creatinine,
#         serum_sodium, smoking, time
#     ], dtype=np.float32).reshape(1, -1)
    
#     # Make prediction
#     prediction = xg.predict(input_data)[0]
#     result = "High Risk" if prediction == 1 else "Low Risk"
#     return result



# Create Gradio interface object
iface = gradio.Interface(fn = predict_death_event,
                         inputs = [in_Age, in_Anaemia, in_CP, in_Diabetes, in_Ejection, in_HBP, in_Platelets, in_SC, in_SS, in_Sex, in_Smoking, in_Time],
                         outputs = [out_label],
                         title="Patient Survival Prediction",
                         description="Predict survival of patient with heart failure, given their clinical record",
                         allow_flagging='never'
                         )

# Mount gradio interface object on FastAPI app at endpoint = '/'
app = gradio.mount_gradio_app(app, iface, path="/")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 