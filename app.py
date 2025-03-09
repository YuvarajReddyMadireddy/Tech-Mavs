import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure GeminiAI client
genai.configure(api_key=api_key)

# Custom CSS for advanced styling with animations and background color
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #fdfbfb, #ebedee);
        color: #2c3e50;
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 3rem;
        margin: auto;
        max-width: 900px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }
    h1, h2, h3 {
        text-align: center;
        color: #2c3e50;
        font-weight: bold;
    }
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 2rem;
    }
    .stTextArea>textarea {
        border: 2px solid #0072ff;
        border-radius: 12px;
        font-size: 1.1rem;
        padding: 1rem;
        transition: all 0.3s ease-in-out;
        background: #f4f4f4;
    }
    .stTextArea>textarea:focus {
        border-color: #6e45e2;
        box-shadow: 0 0 15px rgba(110, 69, 226, 0.5);
        transform: scale(1.02);
    }
    .stButton>button {
        background: linear-gradient(135deg, #6e45e2, #88d3ce);
        color: white;
        font-size: 1.2rem;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
    }
    .response-box {
        background: #ecf0f1;
        color: #2c3e50;
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1.5rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.markdown("<h1>🍎 Advancing Nutrition Science through GeminiAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Explore the future of nutrition with AI-powered insights</p>", unsafe_allow_html=True)

# Format AI responses
def format_response(response):
    return f"<div class='response-box'><strong>Nutrition Insights:</strong><br><br>{response}</div>"

# User input
user_input = st.text_area("Enter your nutrition-related question:")

# AI response
if st.button("Get Insights ✨"):
    if user_input.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing with GeminiAI..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(user_input)
                formatted_response = format_response(response.text)
                st.success("Here’s what GeminiAI says:")
                st.markdown(formatted_response, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")

# Advanced Insights Section
st.markdown("<h2>🔬 Advanced Nutrition Insights</h2>", unsafe_allow_html=True)
st.markdown("Discover the latest trends and AI-driven meal plans tailored just for you.")

if st.button("Generate Advanced Insights 🌿"):
    with st.spinner("Gathering advanced data..."):
        try:
            prompt = "Provide a detailed breakdown of the latest nutrition science trends and meal planning strategies."
            response = model.generate_content(prompt)
            st.markdown(format_response(response.text), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error: {e}")
