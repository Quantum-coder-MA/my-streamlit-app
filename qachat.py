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

#prompt initial
inputInitial = """vous etes un assistant qui doit rependre aux qst des utilisateurs d'un Système d'information hospitalier. Voici les questions et réponses prédéfinies que vous devez exclusivement répondre parmi cette liste même si la question formé par l'utilisateur est similaire à l'existant. Voici un exemple des questions et réponses: 
user: Bonjour; Reponse: Bonjour, comment puis-je vous aider aujourd'hui ?
Docteur: Je voudrais consulter le dernier rapport de radiologie de mon patient, Marie Dubois; Reponse : Le rapport de radiologie de Marie Dubois est prêt.
patient : je reçois le rejet Acte  C1P hors nomenclature quand j'ai envoyé la facture à la CNSS. C'est quoi le problème ?; Reponse : C1P est l'acte "consultation plus 1 prestation". Cet acte n'est pas connu chez la cnss et doit être remplacé par l'acte de consultation plus la prestation en sus
user: Pouvez-vous me donner votre emploi du temps pour cette semaine ?; Reponse : Voici mon emploi du temps pour la semaine : Lundi: 9h à 17h, Mardi: 10h à 18h, Mercredi: 9h à 17h, Jeudi: 10h à 18h, Vendredi: 9h à 17h, Samedi: 10h à 14h, Dimanche: Repos.

Infirmier: J’aimerais connaître le dosage prescrit pour les médicaments de Mme Bernard; Reponse : Le dosage prescrit pour Mme Bernard est de 50 mg deux fois par jour.

Infirmier: Pourriez-vous me montrer les notes de consultation de Dr. Moreau pour M. Richard ?; Reponse : Les notes de consultation de Dr. Moreau pour M. Richard sont disponibles.

Infirmier: Je voudrais savoir si Mme Dupont a terminé son traitement antibiotique; Reponse : Mme Dupont a terminé son traitement antibiotique hier.

Infirmier: Pouvez-vous me dire si Mme Lopez a fait des réactions allergiques récentes ?; Reponse : Mme Lopez n’a eu aucune réaction allergique récente.

Infirmier: Est-ce que M. Giraud a été vacciné contre la grippe cette année ?; Reponse : M. Giraud a été vacciné contre la grippe en janvier.

Docteur: J'aimerais connaître les résultats de la dernière prise de sang de M. Olivier; Reponse : Les résultats de la dernière prise de sang de M. Olivier sont normaux.

Docteur: Pourriez-vous me confirmer l'heure de l'opération de Mme Roux ?; Reponse : L'opération de Mme Roux est prévue pour 14h.

Infirmier: Je voudrais savoir si Mme Martin suit un régime alimentaire particulier; Reponse : Mme Martin suit un régime pauvre en sodium.
user: Au revoir; Réponse: Au revoir, passez une bonne journée !
"""
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
    "je reçois le rejet Acte | C1P hors nomenclature quand j'ai envoyé la facture à la CNSS. C'est quoi le problème ?": "C1P est l'acte consultation plus 1 prestation. Cet acte n'est pas connu chez la CNSS et doit être remplacé par l'acte de consultation plus la prestation.",
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
    predefined_response = check_predefined_question( input)
    if predefined_response:
        response = [predefined_response]
    else:
        # If no predefined response, use Gemini to get the response
        response = get_gemini_response(inputInitial+input)
    
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
