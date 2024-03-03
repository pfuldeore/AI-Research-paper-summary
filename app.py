from dotenv import load_dotenv

load_dotenv()
import streamlit as st
import os
from PyPDF2 import PdfReader
import textwrap
import google.generativeai as genai
from IPython.display import Markdown

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def get_gemini_response(input,pdf_content):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(f"{input}: {pdf_content}")
    return response._result.candidates[0].content.parts[0].text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PdfReader(uploaded_file) 
        data = ""
        for i in range(len(reader.pages)):
            data = data + " " + reader.pages[i].extract_text() 
        return data
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="research paper summarizer 🔍")
st.header("📃 Advance Research paper summarizer 🔍")
uploaded_file=st.file_uploader("Upload the research paper(PDF)...",type=["pdf"])


if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Get the summary")

input_prompt1 = """
 You are an expert in reading and understanding the scientific research papers. you have an ability to extract the critical information 
 from the paper. please understand the paper mentioned above and write the summary in above points - problem statement, proposed solutions/ methedology and results
 in bullet points. 
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content)
        st.subheader("The Repsonse is")
        st.write(response)
    else:
        st.write("Please uplaod the research paper")