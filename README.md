# 🔐 UPI Fraud Detection System

A Machine Learning–based system designed to detect fraudulent UPI (Unified Payments Interface) transactions in real time.

#📘 Project Overview
UPI transactions have become widely used in financial systems, increasing the risk of fraud.
This project aims to identify suspicious transactions by training ML models on a structured dataset and deploying an easy-to-use prediction website.


## The system:

- Trains models on historical transaction data

- Uses preprocessing techniques like StandardScaler & OneHotEncoder

- Compares multiple ML algorithms

- Deploys a fully functional fraud prediction website using Streamlit

- Alerts the user whether a transaction is Fraudulent or Legitimate

# 📁 Dataset & Training Process
- We trained the model using a dataset with features such as:

-Transaction type

- Transaction amount

- Account balances (old & new)

- Balance differences

- Origin & destination account details

- Fraud labels


## Training Steps

## 1.Data Cleaning & Preprocessing

- Handling missing values

- Converting data types

- Splitting categorical & numerical columns

## 2.Feature Engineering

- balanceDiffOrig = newBalanceOrig - oldBalanceOrig

- balanceDiffDest = newBalanceDest - oldBalanceDest

## 3. Encoding & Scaling

- OneHotEncoder for categorical features

- StandardScaler for numerical features

## 4. Model Training
- We trained and compared two models:

- Logistic Regression

- Random Forest Classifier

## 5.Model Saving
- The best-performing model was saved using:

- joblib

- cloudpickle (fallback to avoid version mismatch errors)

# 🤖 Machine Learning Algorithms Used
🔹 StandardScaler

- Used to normalize numerical values for better model performance.

🔹 OneHotEncoder

- Converts categorical features (like transaction type) into numerical format.

🔹 Logistic Regression

- Lightweight, interpretable, and effective for binary fraud detection.

🔹 Random Forest

A more powerful ensemble model that handles non-linear patterns, often giving higher accuracy and recall.


# 🛠️ Technologies Used

- Python

- Pandas

- NumPy

- Scikit-learn

- Streamlit

- Joblib

- Cloudpickle

# 🖥️ UPI Fraud Detection Web App (Streamlit)

A clean and interactive Streamlit application was developed to allow real-time predictions.

## Features of the Website

✔ User inputs the transaction details
✔ ML model processes the data
✔ Predicts whether the transaction is:

Fraudulent

Not Fraudulent
✔ A fraud alert message is shown instantly
✔ Professional UI with gradient background theme
✔ Quick, real-time performance

## To run the app:

```
git clone https://github.com/Priyadav17/UPI-Fraud-Detection-system.git
streamlit run fraud_detection.py
```

# 🧪 Model Evaluation

## The models were tested using the following metrics:

- Accuracy

- Precision

- Recall

- F1-score

- Confusion Matrix

- Random Forest generally achieved higher recall, which is very important for catching fraudulent transactions.

