import streamlit as st
from PIL import Image
from io import BytesIO
import requests
import pytesseract
from model import GeneralModel

st.set_page_config(page_title="OCR App", page_icon="favicon.png")
st.title("Poison - GPT-3/Tesseract OCR")
st.subheader("Disclaimer: If you think your pet may have been exposed to poison, contact a professional and not GPT-3")
st.write("""This is pretty rough. The extract will try to extract ingredients from images of food labels. 
Then you have to copy/paste it into the ingredients box and clean it up as needed. When you've entered
all your ingredients, click 'Analyze' and GPT-3 will tell you what it thinks is poisonous to dogs. 
You may also need to manually clear out the text boxes if you want to run it again. Sorry. """)

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

ingredients = st.empty()
ingredients = st.text_area('Ingredients here', '', key="ingred_text")
button_gpt = st.empty()
button_gpt = st.button(label = "Analyze")
gpt_results = st.empty()

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
        #ingredients = st.text_area('Ingredients here', formatted_result, key="ingred_text")
        st.write(formatted_result)
        

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
 

if button_gpt:
    if api_key:
            with st.spinner(text="In progress"):
                ingredients_text = ingredients
                ingredients_text = ingredients_text.replace(',', ', ')
                ingredients_text = ingredients_text.replace('  ', ' ')
                ingredients_text = ingredients_text + '\n\n'
                report_text = process_prompt(ingredients_text)
                # st.markdown(report_text)
                gpt_results = st.text_area('GPT results', report_text)
    else:
        st.error("🔑 Please enter API Key")
        

 


st.caption("Credit to @SohamGhugare for Tesseract/Streamlit project")
