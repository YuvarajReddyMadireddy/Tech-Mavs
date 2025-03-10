import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import speech_recognition as sr

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Custom CSS for ultra-modern UI with animated background and glowing elements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        color: #2c3e50;
        margin: 0;
        padding: 0;
    }
    .stApp {
        background: #cce7ff;
        border-radius: 20px;
        padding: 4rem;
        margin: auto;
        max-width: 1200px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.2);
        text-align: center;
        backdrop-filter: blur(15px);
        animation: fadeIn 1.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    h1 {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(90deg, #6e45e2, #88d3ce);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        text-shadow: 0px 0px 20px rgba(110, 69, 226, 0.8);
    }
    .subtitle {
        font-size: 1.8rem;
        color: #2c3e50;
        margin-bottom: 3rem;
    }
    .input-section {
        background: #f0faff;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    .stTextArea>textarea, .stTextInput>div>div>input {
        border: 3px solid #6e45e2;
        border-radius: 15px;
        font-size: 1.2rem;
        padding: 1.2rem;
        background: #ffffff;
    }
    .stButton>button {
        background: linear-gradient(135deg, #6e45e2, #88d3ce);
        color: white;
        font-size: 1.3rem;
        padding: 1.2rem 4rem;
        border: none;
        border-radius: 50px;
        cursor: pointer;
        margin-top: 1rem;
    }
    .response-box {
        background: #f0faff;
        padding: 2.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        text-align: left;
    }
    .response-box h2 {
        font-size: 2.5rem;
        margin-bottom: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class='stApp'>
        <h1>🍽️ NutriGen: Your AI-Powered Nutrition Assistant</h1>
        <p class='subtitle'>Craft personalized meal plans tailored to your health goals, dietary needs, and taste preferences.</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for diet preferences and search history
if 'diet_preferences' not in st.session_state:
    st.session_state['diet_preferences'] = ""
if 'search_history' not in st.session_state:
    st.session_state['search_history'] = []

# Sidebar for past search history
with st.sidebar:
    st.markdown("### 🔍 Past Search History")
    if st.session_state['search_history']:
        for i, search in enumerate(st.session_state['search_history']):
            st.markdown(f"**Search {i + 1}:** {search}")
    else:
        st.markdown("No past searches yet.")

# User input (Text and Audio)
diet_preferences = st.text_area("Describe your dietary preferences:", value=st.session_state['diet_preferences'])

# Update session state with the latest input
if diet_preferences != st.session_state['diet_preferences']:
    st.session_state['diet_preferences'] = diet_preferences

st.markdown("**Or record your dietary preferences:**")
if st.button("Record Audio 🎙️"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Recording... Please speak now!")
        audio = recognizer.listen(source)
        st.success("Recording complete. Transcribing...")
        try:
            transcript = recognizer.recognize_google(audio)
            st.session_state['diet_preferences'] = transcript
            # Update the text area with the transcribed text
            diet_preferences = st.session_state['diet_preferences']
        except sr.UnknownValueError:
            st.error("Sorry, could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Error with the speech recognition service: {e}")

# AI response
if st.button("Generate My Meal Plan 🥗"):
    if not st.session_state['diet_preferences'].strip():
        st.warning("Please provide some details about your dietary preferences.")
    else:
        with st.spinner("Creating your personalized meal plan..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(f"Generate a personalized week-long meal plan including recipes and grocery lists based on these details: {st.session_state['diet_preferences']}")
                meal_plan = response.text
                st.session_state['meal_plan'] = meal_plan  # Store the meal plan in session state

                # Add the current search to the search history
                st.session_state['search_history'].append(st.session_state['diet_preferences'])

                st.markdown(f"""
                    <div class='response-box'>
                        <h2>Your Personalized Meal Plan</h2>
                        <p>{meal_plan}</p>
                    </div>
                """, unsafe_allow_html=True)

                # Add a download button for the meal plan
                st.download_button(
                    label="Download Meal Plan 📄",
                    data=meal_plan,
                    file_name="meal_plan.txt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")