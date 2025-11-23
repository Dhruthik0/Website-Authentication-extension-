import streamlit as st
import pandas as pd
import joblib
import torch
import requests
from src.features import features_from_url
from src.dataset import prepare_sequences
from src.cnn_model_torch import CharCNN
import plotly.graph_objects as go

# ----------------- UI CONFIG -----------------
st.set_page_config(
    page_title="🛡️ Phishing URL Detector",
    page_icon="🔍",
    layout="centered",
)

st.title("🛡️ Phishing URL Detector")
st.markdown("### Enter a website URL below to check if it's **legit or phishing** ⚠️")

# ----------------- LOAD MODELS -----------------
@st.cache_resource
def load_models():
    rf = joblib.load("models/rf_model.joblib")

    vocab_size = 94  # update this to your model vocab size
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    cnn_model = CharCNN(vocab_size=vocab_size).to(device)
    cnn_model.load_state_dict(torch.load("models/cnn_best_torch.pt", map_location=device))
    cnn_model.eval()
    return rf, cnn_model, device

rf, cnn_model, device = load_models()

# ----------------- HELPER FUNCTION -----------------
def check_url_reachability(url):
    """Check if the given URL is reachable."""
    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        if response.status_code < 400:
            return True
        else:
            return False
    except Exception:
        return False

# ----------------- USER INPUT -----------------
url = st.text_input("🌐 Enter URL", "https://example.com")

if st.button("🔍 Predict") and url:
    st.info("⏳ Checking reachability...")
    reachable = check_url_reachability(url)

    if not reachable:
        st.error("❌ The URL seems **unreachable**. Please check if it's correct or online.")
    else:
        st.success("✅ The URL is **reachable**. Proceeding with analysis...")

        # ----------------- MODEL PREDICTION -----------------
        rf_feat = pd.DataFrame([features_from_url(url)])
        rf_p = float(rf.predict_proba(rf_feat)[:, 1][0])

        X = prepare_sequences([url], max_len=200)
        X = torch.tensor(X, dtype=torch.long, device=device)
        with torch.no_grad():
            cnn_p = float(cnn_model(X).cpu().item())

        prob = (rf_p + cnn_p) / 2.0

        # ----------------- GAUGE METER -----------------
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            title={'text': "Phishing Probability (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "darkred"},
                'steps': [
                    {'range': [0, 30], 'color': "green"},
                    {'range': [30, 60], 'color': "orange"},
                    {'range': [60, 100], 'color': "red"},
                ],
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

        # ----------------- RESULT -----------------
        if prob < 0.3:
            st.success("✅ This website looks **Safe**.")
        elif prob < 0.6:
            st.warning("⚠️ This website looks **Suspicious**. Be careful!")
        else:
            st.error("🚨 This website is likely **Phishing**! Avoid it.")

        # ----------------- EXTRA DETAILS -----------------
        with st.expander("🔎 More details"):
            st.write({
                "Final Probability": round(prob, 3),
                "RF Score": round(rf_p, 3),
                "CNN Score": round(cnn_p, 3),
                "Label": int(prob >= 0.5),
                "Reachable": reachable
            })

st.markdown("---")
st.caption("Made by Dhruthik")
