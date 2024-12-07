from dotenv import load_dotenv
load_dotenv() # loading all the .env variables
import os
import streamlit as st

# The PIL format, short for Python Imaging Library, is a powerful library in 
# Python that allows users to open, manipulate, and save various image file formats.
from PIL import Image 
import google.generativeai as genai

genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

# function for interacting in a model
def get_gemini_response(input, img ):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, img[0]])
    return response.text

# process the image
def process_input_image(uploader_file):
    # check if the file has been uploaded
    if uploader_file is not None:
        #Read the bytes data
        bytes_data = uploader_file.getvalue()

        #particular format which gemini vision pro accepts
        image_parts =[
            {
                "mime_type": uploader_file.type,
                "data": bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No File found")
    

# Create a streamlit app (FRONT END SETUP)
st.set_page_config(page_title = "Gemini Health app")
st.header("Gemini Health application")

uploaded_file = st.file_uploader("Choose an image...", type = ['jpg', 'jpeg', 'png', 'webp'])
image = ""

if uploaded_file is not None:
    image = Image.open(uploaded_file) # this will be string data type
    st.image(image, caption = "Uploaded Image", use_container_width = True)

submit = st.button("Tell me about the total calories")


input_prompt = """
You are an expert nutritionist where you need to see the food items from the image and calculate
the total calories, also provide the details of every food item with calories intake.
You should display the result in the below format:

1. Item -1 - number of calories
2. Item -2 - number of calories
----
----
Finally you can also mention that the food is healthy or not, addtionally you should also mention the percentage
split of the carbohydrates, fats, proteins, fibers, sugars and other important things required in the diet.

"""

if submit:
    image_data = process_input_image(uploader_file=uploaded_file)
    response = get_gemini_response(input=input_prompt, img=image_data)
    st.header("The response is: ")
    st.write(response)