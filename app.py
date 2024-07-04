import streamlit as st
import joblib
import numpy as np

# Load the pre-trained model
model = joblib.load('churnclassifier.sav')
st.title("Customer Churn Predictor")
st.subheader("Predict whether a customer will leave the bank or not")

# Input fields
try:
    CreditScore = float(st.text_input('Enter your credit score:'))
    Age = float(st.text_input('Enter your age:'))
    Tenure = float(st.text_input('Enter how long you have been at the company (in years):'))
    Balance = float(st.text_input('Enter your account balance:'))
    NumOfProducts = int(st.text_input('Enter number of products you have bought or subscribed to:'))
    HasCrCard = st.selectbox('Do you have a credit card? (1 if yes, 0 if no)', [1, 0])
    IsActiveMember = st.selectbox('Are you an active member? (1 if yes, 0 if no)', [1, 0])
    EstimatedSalary = float(st.text_input('Enter your estimated salary:'))
except ValueError:
    st.error("Please enter valid numeric values for the above field.")
    st.stop()  # Stop execution to prevent further errors

# Calculate derived features
if EstimatedSalary != 0:
       BalanceSalaryRatio = Balance / EstimatedSalary 
else:
     BalanceSalaryRatio = 0
       
TenureByAge = Tenure / Age if Age != 0 else 0.0
MoneyInAccount = Balance > 0 

# Other feature engineering (e.g., Geography, Gender, AgeCategory)
Geography = st.selectbox('Select country (Germany, Spain, France):', ['Germany', 'Spain', 'France'])
Gender_Male = st.selectbox('Select gender (1 if male, 0 if female):', [1, 0])
Geography_Germany = Geography == 'Germany'
Geography_Spain = Geography == 'Spain'
AgeCategory_40_to_50 = 40 <= Age <= 50
AgeCategory_Above_50 = Age > 50
AgeCategory_Below_30 = Age < 30

# Create input array
inputs = np.array([CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard,
                  IsActiveMember, EstimatedSalary, BalanceSalaryRatio,
                  TenureByAge, MoneyInAccount, Geography_Germany,
                  Geography_Spain, Gender_Male, AgeCategory_40_to_50,
                  AgeCategory_Above_50, AgeCategory_Below_30]).reshape(1, -1)

# Make predictions
pred = model.predict(inputs)

# Display prediction result
if pred == 1:
    st.write("*The customer will leave the bank.*")
else:
    st.write("**The customer will not leave the bank.**")
