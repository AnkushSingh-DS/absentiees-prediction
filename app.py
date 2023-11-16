import streamlit as st
import pandas as pd
from joblib import load
from absenteeism_module import CustomScaler  # Adjust the import based on your actual module structure

# Load the trained logistic regression model
model = load('model.joblib')

# Load the scaled input pickle file
scaled_input_scaler = load('scaler.joblib')

# Set page configuration and title
st.set_page_config(
    page_title='Absenteeism Predictor',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS for styling, including the background image
custom_css = """
    body {
        background-image: url('background_image.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        background-color: #f4f4f4; /* Fallback color if the image fails to load */
        color: #333;
    }
    .header {
        font-size: 36px;
        font-weight: bold;
        color: #00008B; /* Blue header color */
        padding-bottom: 20px;
    }
    .prediction {
        font-size: 24px;
        color: #27ae60; /* Green prediction color */
        padding-top: 20px;
    }
    .input-label {
        font-size: 24px;
        font-weight: bold;
        color: black; /* Red input label color */
        padding-top: 10px;
    }
    .input-field {
        font-size: px;
        color: #2c3e50;  /* Dark gray input field color */
    }
    .predict-button {
        background-color: #e74c3c; /* Red button color */
        color: white;
        padding: 15px 30px;
        font-size: 24px;
        border-radius: 8px;
        cursor: pointer;
        text-align: center;
    }
"""

# Apply custom CSS
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# Streamlit app
st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

# Streamlit app
with st.container():
    st.title('Absenteeism Predictor')
    st.markdown("<p class='header'>Predict Employee Absenteeism</p>", unsafe_allow_html=True)

    st.markdown('<hr style="border-top: 5px solid green; margin: -20px 0 80px 0; width: 40%;">', unsafe_allow_html=True)

    # Input fields
    st.markdown('<p class="input-label"><b>Age</b></p>', unsafe_allow_html=True)
    age = st.slider('', 18, 65, 30, format="%d", key='age', help="input-field")

    # Horizontal line for visual separation
    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)

    st.markdown('<p class="input-label"><b>Reasons for Absence</b></p>', unsafe_allow_html=True)
    reason_1 = st.checkbox('Medical Conditions', key='reason_1')
    reason_2 = st.checkbox('Reproductive and Perinatal Health', key='reason_2')
    reason_3 = st.checkbox('Clinical Findings and External Causes', key='reason_3')
    reason_4 = st.checkbox('Medical Services and Follow-up', key='reason_4')

    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)

    # Add the Month Value input field
    st.markdown('<p class="input-label"><b>Month</b></p>', unsafe_allow_html=True)
    month_value = st.slider('', 1, 12, 6)

    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)
    
    st.markdown('<p class="input-label"><b>Transportation Expense</b></p>', unsafe_allow_html=True)
    transportation_expense = st.slider('', 100, 200, 150, key='transportation_expense', help="input-field")

    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)

    st.markdown('<p class="input-label"><b>Body Mass Index</b></p>', unsafe_allow_html=True)
    body_mass_index = st.slider('', 15, 40, 25, key='body_mass_index', help="input-field")

    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)

    st.markdown('<p class="input-label"><b>Education</b></p>', unsafe_allow_html=True)
    education = st.radio('', ['High School', 'More than High School'], key='education')

    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)

    st.markdown('<p class="input-label"><b>Children</b></p>', unsafe_allow_html=True)
    children = st.slider('', 0, 3, 1, key='children', help="input-field")

    st.markdown('<hr style="border-top: 2px solid #; margin: 30px auto; margin-bottom: 45px; width: 80%;">', unsafe_allow_html=True)

    st.markdown('<p class="input-label"><b>Pet</b></p>', unsafe_allow_html=True)
    pet = st.slider('', 0, 3, 1, key='pet', help="input-field")

    st.markdown('<hr style="border-top: 2px solid green; margin: 30px auto; margin-bottom: 70px; width: 100%;">', unsafe_allow_html=True)

    # Prediction function with caching
    def predict_outcome(age, reason_1, reason_2, reason_3, reason_4, month_value, transportation_expense,
                        body_mass_index, education, children, pet):
        input_data = pd.DataFrame({
            'Age': [age],
            'Reason_1': [1 if reason_1 else 0],
            'Reason_2': [1 if reason_2 else 0],
            'Reason_3': [1 if reason_3 else 0],
            'Reason_4': [1 if reason_4 else 0],
            'Month Value': [month_value],
            'Transportation Expense': [transportation_expense],
            'Body Mass Index': [body_mass_index],
            'Education': [1 if education == 'More than High School' else 0],
            'Children': [children],
            'Pet': [pet],
        })

        scaled_input = scaled_input_scaler.transform(input_data)
        prediction_result = model.predict(scaled_input)[0]

        if prediction_result == 0:
            return "Low Absenteeism"
        else:
            return "High Absenteeism"

    # Prediction button
    button_clicked = st.button('Predict Outcome', key='predict_button')
    if button_clicked:
        prediction_result = predict_outcome(age, reason_1, reason_2, reason_3, reason_4, month_value,
                                            transportation_expense, body_mass_index, education, children, pet)
        st.markdown(f"<p class='prediction'>Predicted Absenteeism: {prediction_result}</p>", unsafe_allow_html=True)
        # Description button
    if st.button("Description"):
        st.write(
            """
            ### Absenteeism Prediction Description
            
            - **Low Absenteeism:** The model predicts that the employee is expected to have a lower likelihood of being absent from work.
            
            - **High Absenteeism:** The model predicts that the employee may have a higher likelihood of being absent from work.
            
            #### Example:
            
            - If the model predicts "Low Absenteeism," it suggests that the employee is expected to have a good attendance record.
            
            - If the model predicts "High Absenteeism," it suggests that the employee may be absent more frequently.
            """
        )    
