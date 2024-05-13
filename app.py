import streamlit as st
from PIL import Image
import google.generativeai as genai

genai.configure(api_key="AIzaSyCRDCwvE15Ig8RG_XJRqEgDKuWaqf6wpXc")

# Function to load gemini pro vision
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_text, image, prompt):
    if image is not None:
        response = model.generate_content([input_text, image[0], prompt])
    else:
        response = model.generate_content([input_text, prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None

st.set_page_config(page_title="RecipeGem page")
# Add some custom CSS for styling
st.markdown(
    """
    <style>
    .st-emotion-cache-1r4qj8v {
        background-image: url('https://images.unsplash.com/photo-1490818387583-1baba5e638af?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D');  /* Add your background image URL here */
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: Arial, sans-serif;  /* Specify your preferred font family */
    }
    .st-emotion-cache-gh2jqd{
            width: 84%;
    margin-left: 32%;
    padding: 6rem 1rem 10rem;
    max-width: 46rem;
    }
    .header {
        color: #008080;
        text-align: center;
        font-size: 36px;
        margin-bottom: 20px;
    }
    .subheader {
        color: #696969;
        text-align: center;
        font-size: 24px;
        margin-bottom: 10px;
    }
    .button {
        background-color: #008080;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .error-message {
        color: red;
        text-align: center;
        font-size: 18px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("RecipeGem")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

# Text input for user to type ingredients
user_input = st.text_input("Type ingredients here...")

submit = st.button("Generate Recipe")

# Prompt for gemini
input_prompt = """
You are an expert in understanding invoices. We will upload an image
as an invoice which will have some vegetables. Additionally, you have typed some ingredients. Using either the uploaded image or the typed ingredients, 
generate a recipe that user can follow to make a dish out of the vegetables in the invoice along with the typed ingredients.
"""

if submit:
    if uploaded_file is None and not user_input:
        st.error("Please upload an image or type ingredients.")
    else:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(user_input, image_data, input_prompt)
        st.subheader("The response is")
        st.write(response)
