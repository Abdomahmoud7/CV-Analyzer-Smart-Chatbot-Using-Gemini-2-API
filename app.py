import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv
import fitz
from docx import Document


load_dotenv('.env')
genai.configure(api_key=os.environ['GENAI_API_KEY'])

generation_config = {
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 50,
  "max_output_tokens": 1024,
  "response_mime_type": "text/plain",
}

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def analyze_cv(cv_text: str) -> str:
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash',
        generation_config=generation_config
    )

    chat_session = model.start_chat(history=[])
    prompt = f"""
    You are an HR expert. Analyze the following CV text and provide a percentage score (0-100%) for job acceptance.
    Consider experience, skills, education, and industry relevance.
    Provide a detailed analysis and final percentage score.
    CV TEXT:
    {cv_text}
    """
    response = chat_session.send_message(prompt)
    return response.text


st.set_page_config(page_title='CV Analyzer')
st.header('CV Analyzer - Smart Chatbot Using Gemini 2 API')

uploaded_file = st.file_uploader("Upload your CV (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1]
    temp_path = f"temp_cv.{file_extension}"
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    
    if file_extension == "pdf":
        cv_text = extract_text_from_pdf(temp_path)
    elif file_extension == "docx":
        cv_text = extract_text_from_docx(temp_path)
    else:
        st.error("Unsupported file format.")
        st.stop()
    
    
    st.subheader("Analysis Result:")
    response = analyze_cv(cv_text)
    st.write(response)

