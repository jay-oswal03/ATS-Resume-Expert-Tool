import base64
import io
import google.generativeai as genai
import pdf2image
from PIL import Image
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from the generative AI model


def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

# Function to process uploaded PDF


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        with st.spinner('Processing PDF...'):
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            first_page = images[0]
            img_byte_arr = io.BytesIO()
            first_page.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            pdf_parts = [
                {
                    "mime_type": "image/jpeg",
                    "data": base64.b64encode(img_byte_arr).decode()
                }
            ]
        return pdf_parts, img_byte_arr
    else:
        raise FileNotFoundError("No file uploaded")


# Streamlit App
st.set_page_config(page_title="Resume Data Extractor", layout="wide")
custom_css = """
    <style>
    .main {
        background-color: #1e1e1e;
        color: white;
    }
    .stButton button {
        background-color: #007BFF;
        color: white;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        padding: 10px 20px;
        margin: 10px;
    }
    .stButton button:hover {
        background-color: #0056b3;
    }
    .stHeader h1, .stSubheader, .stMarkdown, .stFileUploader label {
        color: #ffffff;
    }
    .stTextArea, .stFileUploader {
        background-color: #2c2c2c;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
        font-size: 16px;
        color: white;
    }
    .stSpinner {
        text-align: center;
    }
    .css-1d391kg {
        text-align: center;
    }
    .css-9s5bis {
        text-align: center;
    }
    .uploaded-file-preview {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .uploaded-file-preview img {
        max-width: 100%;
        height: auto;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.header("ATS Resume Expert")

with st.container():
    st.subheader("Job Description")
    input_text = st.text_area("Enter Job Description:", key="input",
                              height=150, placeholder="Paste the job description here...")

with st.container():
    st.subheader("Choose a file...")
    uploaded_file = st.file_uploader("", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully")

    pdf_parts, first_page_bytes = input_pdf_setup(uploaded_file)

    with st.container():
        st.subheader("View Uploaded Resume")
        st.image(first_page_bytes,
                 caption="Uploaded Resume - First Page", use_column_width=True)

with st.container():
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submit1 = st.button("Tell me About the Resume")
    with col2:
        submit2 = st.button("Percentage Match")
    with col3:
        submit3 = st.button("Suggested Skills")

input_prompt1 = """
You are an experienced Human Resources professional with extensive expertise in evaluating 
resumes for various technology-related job roles, including Data Science, Full Stack Web Development, 
Big Data Engineering, DevOps, and Data Analyst positions. Your task is to thoroughly review the 
provided resume and compare it against the specified job description. Begin by examining the 
candidate's educational background, professional experience, technical skills, and any 
certifications. Assess how well these qualifications match the job requirements. Provide a 
comprehensive evaluation of the candidate's profile, focusing on the alignment between their 
qualifications and the job description. Highlight the candidate's strengths, such as relevant 
experience, key achievements, and notable skills. Additionally, identify any weaknesses or gaps 
in the resume, such as missing skills, lack of experience, or areas that need improvement. 
Offer detailed feedback on how the candidate can enhance their resume to better align with the 
job requirements, including suggestions for additional training, certifications, or skills 
development. In your evaluation, consider the latest industry trends and the specific demands 
of the job role. Provide a balanced and thorough analysis, ensuring that the candidate receives 
actionable insights to improve their chances of securing the position.
"""

input_prompt2 = """
You are a highly sophisticated Applicant Tracking System (ATS) with advanced capabilities 
in analyzing and evaluating resumes for a wide range of technology-focused job roles, 
including Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analyst 
positions. Your task is to meticulously compare the provided resume against the detailed job 
description and determine the percentage match. Start by parsing the resume to extract key 
information, including the candidate's skills, experiences, education, and certifications. 
Then, analyze this information against the job description to calculate the match percentage. 
Consider the relevance and frequency of keywords, the alignment of skills and experiences with 
the job requirements, and the overall suitability of the candidate for the role. After calculating 
the match percentage, identify and list any critical keywords or skills that are missing from the 
resume but are essential for the job role. Provide a detailed explanation of why these keywords are
important and how they impact the match percentage. Finally, offer a comprehensive summary of your
findings. Include an overall assessment of the candidate's suitability for the role, highlighting
both strengths and areas for improvement. Provide actionable recommendations for enhancing the 
resume to better meet the job description, such as adding specific skills, gaining relevant 
experience, or obtaining certifications. Your goal is to give the candidate clear and 
constructive feedback to help them improve their chances of being selected for the position. Start
your answer with the match percentage.
"""

input_prompt3 = """
You are a knowledgeable career advisor with a deep understanding of the technology industry and the evolving demands of various tech-related job roles, including Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis. Your task is to thoroughly analyze the provided resume and job description to identify key skills, certifications, and professional development opportunities that would significantly enhance the candidate's profile for the specified job role.
Begin by examining the candidate's current skill set, educational background, and professional experience. Identify any gaps or areas where additional skills or certifications could strengthen their qualifications. Based on your analysis, compile a detailed list of recommended skills and certifications that are highly relevant to the job role. For each suggestion, provide a comprehensive explanation of its importance, including how it aligns with industry trends, the specific job requirements, and the potential benefits for the candidate's career growth.
Additionally, recommend reputable sources or platforms where the candidate can acquire these skills and certifications, such as online courses, training programs, or professional certifications. Offer guidance on the best learning paths and strategies for gaining the recommended skills, ensuring that the candidate has a clear and actionable plan for enhancing their qualifications and increasing their employability.
In your output, provide specific online course or youtube videos, or links to other resources they can use to enhance and expand their skillset.
"""

if submit1:
    if uploaded_file is not None:
        response = get_gemini_response(input_prompt1, pdf_parts, input_text)
        st.subheader("Evaluation Result")
        st.write(response)
    else:
        st.error("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        response = get_gemini_response(input_prompt2, pdf_parts, input_text)
        st.subheader("Percentage Match Result")
        st.write(response)
    else:
        st.error("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        response = get_gemini_response(input_prompt3, pdf_parts, input_text)
        st.subheader("Suggested Skills and Certifications")
        st.write(response)
    else:
        st.error("Please upload the resume")
