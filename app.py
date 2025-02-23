import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))



def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,pdf_content[0],prompt])

    return response.text                



def input_pdf_setup(uploaded_file):
   if uploaded_file is not None:
        ##convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

       ##convert to bytes
        ##PDF Page → JPEG Image →  Special Code (Base64)
        img_byte_arr = io.BytesIO()

        first_page.save(img_byte_arr , format='JPEG')

        img_byte_arr = img_byte_arr.getvalue()


        pdf_parts = [
           {
               "mime_type":"image/jpeg",
               "data":base64.b64encode(img_byte_arr).decode()
           }
        ]
        return pdf_parts
   else:

        raise FileNotFoundError("no uploaded files") 
   



####streamlit 

st.set_page.config(page_title="ATS Resume")
st.header("ATS Tracking System")

input_text = st.text_area("job description:" ,key="input")  ##key for tracking purpose

uploaded_files = st.file_uploader("upload your resume(PDF)" , type=["pdf"])   

if uploaded_files is not None:
    st.write("PDF Uploaded successfully")


submit1 = st.button("Tell me about the resume")

submit2 = st.button("How can I improve my skills")

#submit3 = st.button("what are the keywords are missing")

submit3 = st.button("percentage match")


input_prompt1 = "you are an experienced HR in the field of machine learning,deep learining,generative ai,data science,data analyst, your task is to review the provided resume against the job description for this profiles"

input_prompt2 = "you are an experienced HR in the field of machine learning,deep learining,generative ai,data science,data analyst,your task is share how to improve the skills  "


input_prompt3 ="you are an skilled ATS(APPlicant tracking system), scanner with in the field of machine learning,deep learining,generative ai,data science,data analyst and deep ATS functionality,your task is to evalute the resume against the provided job description give me the percentage of match if the resume matches "

if submit1:
    if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt1,pdf_content,input)
        st.subheader("the response is...")
        st.write(response)
    
   
    else:
        st.write("please uploaded the resume")


elif submit3:
   if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt3,pdf_content,input)
        st.subheader("the response is...")
        st.write(response)
    
   
   else:
        st.write("please uploaded the resume")


    
    

