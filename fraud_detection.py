import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

# -------------------------
# Page Setup
# -------------------------
st.set_page_config(page_title="Fraud Detection", layout="wide", page_icon="💳")

# -------------------------
# Ensure session_state for alerts persists across interactions
# -------------------------
if "alerts" not in st.session_state:
    st.session_state["alerts"] = []

# -------------------------
# Custom CSS (Light Blue Background + Attractive Small Header)
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
       background: linear-gradient(180deg, #ffffff 0%, #e3ecff 50%, #c8d8ff 100%) !important;
    color: #1c1c1c !important;
        font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }

    /* Modern small header */
    .header-small {
        padding: 14px 22px;
        border-radius: 10px;
        background: linear-gradient(90deg, #4fa3ff 0%, #7db7ff 100%);
        color: white !important;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.1);
    }

    .header-small h3 {
        margin: 0;
        padding: 0;
        font-size: 1.3rem !important; /* Smaller heading size */
        font-weight: 700;
    }

    .header-small p {
        margin: 4px 0 0;
        font-size: 0.85rem !important;
        font-weight: 400;
        color: #f0f7ff !important;
    }

    /* Cards stay same */
    .card {
        background: white;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 6px 20px rgba(16,24,40,0.06);
        margin-bottom: 18px;
        color: black !important;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #2563eb, #60a5fa) !important;
        color: white !important;
        font-weight: 600;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(59,130,246,0.20);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
    }

    label {
        color: black !important;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# New Small Header
# -------------------------
st.markdown(
    """
    <div class="header-small">
        <h3>💳 Fraud Detection Dashboard</h3>
        <p>Secure • Fast • Intelligent anomaly identification</p>
    </div>
    """,
    unsafe_allow_html=True,
)

     
     
 


# -------------------------
# Load Model
# -------------------------
try:
    model = joblib.load("fraud_detection_model.pkl")
except Exception as e:
    st.error("⚠️ Could not load the model file 'fraud_detection_model.pkl'.")
    st.exception(e)
    st.stop()

# -------------------------
# Determine expected columns (keeps your earlier logic)
# -------------------------
def get_expected_columns(model):
    if hasattr(model, "feature_names_in_"):
        return list(model.feature_names_in_)
    # fallback default
    return [
        "type",
        "amount",
        "location_of_device",
        "device_name",
        "step",
        "isFlaggedFraud",
        "customer_id",
        "merchant_id",
    ]

EXPECTED_COLUMNS = get_expected_columns(model)

# -------------------------
# Input Card
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<div class='section-title'>Transaction Inputs</div>", unsafe_allow_html=True)

# Two-column layout
col1, col2 = st.columns(2, gap="large")

# Device & location options
device_options = [
    "Android Phone", "iPhone", "iPad / Tablet", "Windows Laptop",
    "MacBook Laptop", "Desktop PC", "Smartwatch", "POS Machine",
    "Unknown Device"
]

location_options = [
    "Mumbai, India", "Delhi, India", "Bangalore, India", "Chennai, India",
    "Hyderabad, India", "Kolkata, India",
    "New York, USA", "Los Angeles, USA", "Chicago, USA",
    "San Francisco, USA", "London, UK", "Toronto, Canada",
    "Dubai, UAE", "Sydney, Australia", "Tokyo, Japan", "Other"
]

# Collect inputs mapping to EXPECTED_COLUMNS where possible
user_inputs = {}
for i, col in enumerate(EXPECTED_COLUMNS):
    lc = col.lower()
    target = col1 if i % 2 == 0 else col2

    with target:
        if lc == "type":
            user_inputs[col] = st.selectbox(col, ["PAYMENT", "TRANSFER", "CASH_OUT", "DEBIT", "CASH_IN"])
        elif lc in {"location_of_device", "location"}:
            user_inputs[col] = st.selectbox(col, location_options)
        elif lc in {"device_name", "device"}:
            user_inputs[col] = st.selectbox(col, device_options)
        elif lc in {"isflaggedfraud"}:
            user_inputs[col] = 1 if st.checkbox(col) else 0
        elif lc in {"amount", "step", "customer_id", "merchant_id"}:
            # For identifiers like customer_id/merchant_id use int default
            default_val = 1000 if lc in {"customer_id", "merchant_id"} else 1000.0
            if lc in {"customer_id", "merchant_id"}:
                user_inputs[col] = st.number_input(col, min_value=0, value=int(default_val))
            else:
                user_inputs[col] = st.number_input(col, min_value=0.0, value=float(default_val))
        else:
            # generic text fallback
            user_inputs[col] = st.text_input(col, value="")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Preview + Actions Card
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
left, right = st.columns([2, 1], gap="large")

with left:
    st.markdown("<div class='section-title'>Preview Input</div>", unsafe_allow_html=True)
    preview_df = pd.DataFrame([[user_inputs.get(c, None) for c in EXPECTED_COLUMNS]], columns=EXPECTED_COLUMNS)
    # try numeric conversion for neater display
    for c in preview_df.columns:
        preview_df[c] = pd.to_numeric(preview_df[c], errors="ignore")
    st.dataframe(preview_df, use_container_width=True)

with right:
    st.markdown("<div class='section-title'>Actions</div>", unsafe_allow_html=True)
    predict_button = st.button("Predict")
    st.markdown(" ")
    st.markdown("**Alerts:**")
    # show count of stored alerts
    st.write(f"Stored alerts: {len(st.session_state['alerts'])}")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Prediction & Alert logic
# -------------------------
if predict_button:
    input_df = pd.DataFrame([[user_inputs.get(c, np.nan) for c in EXPECTED_COLUMNS]], columns=EXPECTED_COLUMNS)
    for c in input_df.columns:
        input_df[c] = pd.to_numeric(input_df[c], errors="ignore")

    st.write("Sending input to model:")
    st.dataframe(input_df)

    try:
        pred = model.predict(input_df)[0]
    except Exception as e:
        st.error("Error during prediction. Check model schema and feature names.")
        st.exception(e)
        pred = None

    if pred is not None:
        if int(pred) == 1:
            # Fraudulent path: show strong alert + allow generating a persistent alert
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("<h3 style='color:#b00020; margin:0'>🚨 FRAUD PREDICTED</h3>", unsafe_allow_html=True)
            st.warning("There are some abnormal anomalies in the transaction.")
            st.markdown("")

            # Show Generate Alert button (styled via CSS class)
            generate = st.button("Generate Alert", key="generate_alert")

            if generate:
                # Create alert record
                alert = {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "prediction": int(pred),
                    "input": input_df.to_dict(orient="records")[0]
                }
                st.session_state["alerts"].append(alert)

                # Show confirmation and details
                st.error("🚨 Alert generated: abnormal/anomalous transaction recorded.")
                st.write("Alert details:")
                st.json(alert)

            else:
                st.info("Click 'Generate Alert' to register this anomaly.")
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            # Not fraudulent
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.success("✔️ Transaction is NOT FRAUDULENT.")
            st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Alerts panel (bottom)
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<div class='section-title'>Alerts Log</div>", unsafe_allow_html=True)

if len(st.session_state["alerts"]) == 0:
    st.markdown("No alerts generated yet.")
else:
    # show table of alerts with timestamp + short description
    alerts_df = pd.DataFrame([
        {
            "timestamp": a["timestamp"],
            "prediction": a["prediction"],
            "type": a["input"].get("type", ""),
            "amount": a["input"].get("amount", ""),
            "device": a["input"].get("device_name", a["input"].get("device", "")),
            "location": a["input"].get("location_of_device", a["input"].get("location", ""))
        }
        for a in st.session_state["alerts"]
    ])
    st.dataframe(alerts_df, use_container_width=True)
    # show expanders for full details
    for i, a in enumerate(reversed(st.session_state["alerts"]), start=1):
        with st.expander(f"Alert #{len(st.session_state['alerts']) - i + 1} — {a['timestamp']}"):
            st.json(a)

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# Small footer
# -------------------------
st.markdown(
    """
    <div style="text-align:center; color:#0b1220; margin-top:12px;">
        You are Safe to use this.
    </div>
    """,
    unsafe_allow_html=True,
)
