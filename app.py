
import streamlit as st
import requests
from exporters import make_txt, make_docx, make_pdf

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️"
)

st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.caption(
    "Generate and edit an AI-assisted legal document draft."
)

backend_url = st.text_input(
    "Backend API URL",
    "http://127.0.0.1:8000"
).rstrip("/")

with st.form("legal_form"):
    document_type = st.selectbox(
        "Document Type",
        [
            "Employment Contract",
            "Non-Disclosure Agreement",
            "Residential Lease Agreement",
            "Freelance Work Contract",
            "General Agreement"
        ]
    )

    party_a = st.text_input("Party A")
    party_b = st.text_input("Party B")
    effective_date = st.text_input("Effective Date")
    jurisdiction = st.text_input(
        "Jurisdiction",
        "Tamil Nadu, India"
    )
    terms = st.text_area(
        "Terms and Conditions",
        placeholder="Enter terms separated by semicolons."
    )

    submitted = st.form_submit_button(
        "Generate Document"
    )

if submitted:
    if not all([
        party_a.strip(),
        party_b.strip(),
        effective_date.strip(),
        terms.strip()
    ]):
        st.error("Please fill in all required fields.")
    else:
        payload = {
            "document_type": document_type,
            "party_a": party_a,
            "party_b": party_b,
            "effective_date": effective_date,
            "terms": terms,
            "jurisdiction": jurisdiction
        }

        try:
            with st.spinner("Generating document..."):
                response = requests.post(
                    f"{backend_url}/generate",
                    json=payload,
                    timeout=120
                )

            if response.ok:
                st.session_state["draft"] = (
                    response.json()["document"]
                )
            else:
                st.error(response.text)

        except requests.RequestException:
            st.error(
                "Backend unavailable. Start FastAPI first."
            )

if "draft" in st.session_state:
    st.markdown("---")
    st.subheader("Document Preview and Editor")

    edited_text = st.text_area(
        "Edit your document",
        value=st.session_state["draft"],
        height=400
    )

    st.session_state["draft"] = edited_text

    st.download_button(
        "Download TXT",
        data=make_txt(edited_text),
        file_name="LegalEase_Draft.txt",
        mime="text/plain"
    )

    st.download_button(
        "Download DOCX",
        data=make_docx(edited_text),
        file_name="LegalEase_Draft.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    try:
        pdf_data = make_pdf(edited_text)

        st.download_button(
            "Download PDF",
            data=pdf_data,
            file_name="LegalEase_Draft.pdf",
            mime="application/pdf"
        )
    except Exception:
        st.warning("PDF export failed. Try DOCX or TXT.")

    st.info(
        "AI output is a draft, not legal advice. "
        "Get qualified legal review before real use."
    )
