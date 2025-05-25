import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

# Set up the UI
st.set_page_config(page_title="LinkedIn Post Generator", page_icon="✍️")
st.title("✍️ LinkedIn Post Generator")
st.markdown("Enter a title or topic below and generate a professional LinkedIn post using AI!")

# Input from user
topic = st.text_input("Enter your post title or topic:")

# Button to trigger generation
if st.button("Generate Post"):
    if not topic.strip():
        st.warning("Please enter a title or topic.")
    else:
        with st.spinner("Generating your LinkedIn post..."):
            try:
                # Call OpenRouter API
                response = requests.post(
                    url="https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {API_KEY}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
                    },
                    data=json.dumps({
                        "model": "qwen/qwen3-235b-a22b:free",
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are a professional content writer who specializes in creating engaging LinkedIn posts."
                            },
                            {
                                "role": "user",
                                "content": f"Write a professional and engaging and useful LinkedIn post based on the following title: '{topic}'"
                            }
                        ],
                        
                    })
                )

                if response.status_code == 200:
                    post_content = response.json()['choices'][0]['message']['content']
                    st.success("✅ Here is your LinkedIn post:")
                    st.write(post_content)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"An error occurred: {e}")

