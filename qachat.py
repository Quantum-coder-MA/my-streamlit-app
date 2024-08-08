from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load the Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Predefined questions and responses
predefined_qas = {
    " je reçois le rejet Acte | C1P hors nomenclature quand j'ai envoyé la facture à la CNSS. C'est quoi le problème ?": " C1P est l'acte  consultation plus 1 prestation . Cet acte n'est pas connu chez la cnss et doit être remplacé par l'acte de consultation plus la prestationensus",
    "Who created Python?": "Python was created by Guido van Rossum and first released in 1991.",
    # Add more predefined questions and responses here
}

# Function to check if a question is predefined
def check_predefined_question(question):
    return predefined_qas.get(question, None)

# Input field and submit button
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    # Check if the input question has a predefined response
    predefined_response = check_predefined_question(input)
    if predefined_response:
        response = [predefined_response]
    else:
        # If no predefined response, use Gemini to get the response
        response = get_gemini_response(input)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    
    st.subheader("The Response is")
    for chunk in response:
        if isinstance(chunk, str):
            st.write(chunk)
            st.session_state['chat_history'].append(("Bot", chunk))
        else:
            st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", chunk.text))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
