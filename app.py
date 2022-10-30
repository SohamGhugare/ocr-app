import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import pytesseract
from model import GeneralModel

st.set_page_config(page_title="OCR App", page_icon="favicon.png")
st.title("Poison")
st.subheader("Wendy Edwards Lablab Hackathon Project")

# Hiding menu and footer (Production use only)
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden; }
    footer {visibility: hidden; }
    </style>
"""
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Creating an object of prediction service
pred = GeneralModel()

api_key = st.sidebar.text_input("APIkey", type="password")
# Using the streamlit cache
@st.cache
def process_prompt(input):

    return pred.model_prediction(input=input.strip() , api_key=api_key)


# Initilizing certain variables to supress not defined error
uploaded_image = None
url = None

uploaded_image = st.file_uploader(
    label = "Please select a file and click the Extract button. Or just enter the ingredients manually into the box",
    type = ["png", "jpg", "jpeg"],
    accept_multiple_files=False
)

# Extract button
button = st.button(label = "Extract")
button_ingred = st.button(label = "Enter manually")

ingredients = st.empty()
button_gpt = st.button(label = "Analyze")

# ingredients = st.text_area('Ingredients list', st.empty())

def read_image(image):
    with st.spinner("Extracting text"):
        try:
            result = pytesseract.image_to_string(image)
        except:
            return st.error("Could not extract text from image")
        if not result:
            return st.error("Could not extract text from image")
        # st.write("## Extracted Text: ")
        # st.write(result)
        formatted_result = ''
        for line in result:
            formatted_result = formatted_result + line.replace('\n', ' ')
        #ingredients = st.text_area('Ingredients list', result)
        #ingredients = st.text_area('Ingredients list', formatted_result)
        ingredients.text_area('Ingredients here', formatted_result)
        #button_gpt = st.button(label = "Analyze")
        

# Button click event
if button:
    if uploaded_image:
        st.success("Successfully uploaded image")
        image = Image.open(BytesIO(uploaded_image.getvalue()))
        st.image(image, caption = "Image you uploaded")
        read_image(image)

    elif url:
        try:
            image = Image.open(BytesIO(requests.get(url).content))
            st.success("Successfully fetched url")
            st.image(image, caption = "Image you uploaded")
            read_image(image)
        except:
            st.error("Invalid URL, please try again.")
 
if button_ingred:
    ingredients.text_area('Ingredients here', '')
 
if button_gpt:
    st.write(ingredients)
    

   

st.caption("Credit to @SohamGhugare for Tesseract/Streamlit project")
