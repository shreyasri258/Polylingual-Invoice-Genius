from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Load Gemini pro vision
model=genai.GenerativeModel('gemini-pro-vision')

def get_gemini_respose(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    
    if uploaded_file is not None:
        
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file is uploaded")

## streamlit setup

st.set_page_config(page_title="Polylingual Invoice Genius")

st.header("Polylingual Invoice Genius")
input=st.text_input("User Enquiry: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image is uploaded", use_column_width=True)


submit=st.button("Initiate Inquiry")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

#after clicking submit button

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_respose(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)