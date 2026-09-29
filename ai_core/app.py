import streamlit as st
import requests

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

document_type = st.selectbox(
    "Document Type",
    [
        "Agreement",
        "Contract",
        "NDA",
        "Lease Agreement",
        "Employment Offer Letter"
    ]
)

parties = st.text_area(
    "Parties",
    placeholder="Enter the parties involved"
)

terms = st.text_area(
    "Terms",
    placeholder="Enter terms separated by semicolons (;)"
)

dates = st.text_input(
    "Effective Date",
    placeholder="Example: 30 September 2026"
)

if st.button("Generate Document"):
    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    }

    try:
        response = requests.post(
            "http://localhost:8000/generate",
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            st.subheader("Generated Document")
            st.text_area(
                "Preview",
                value=data.get("document", data.get("message", "")),
                height=400
            )
        else:
            st.error("Document generation failed.")

    except requests.exceptions.ConnectionError:
        st.error("FastAPI backend is not running.")
