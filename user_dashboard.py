
import streamlit as st
import pandas as pd
import json
from datetime import datetime
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("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")
)



def generate_ai_response(prompt):
    response = client.chat.completions.create(
        model="meta-llama/llama-3.1-8b-instruct:free",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

DATA_FILE = 'reviews.json'

@st.cache_data(ttl=10)
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return pd.DataFrame(json.load(f))
    except:
        return pd.DataFrame()

def save_data(df):
    with open(DATA_FILE, 'w') as f:
        json.dump(df.to_dict('records'), f)

st.title("🗣️ User Review Dashboard")

with st.form("review_form"):
    rating = st.select_slider("Rating", options=[1,2,3,4,5], value=3)
    review = st.text_area("Write your review")
    submitted = st.form_submit_button("Submit Review")
    
    if submitted and review:
        prompt = f"User gave {rating} stars: '{review}'. Respond empathetically as business owner."
        response = generate_ai_response(prompt)
        
        new_entry = {
            'timestamp': datetime.now().isoformat(),
            'user_rating': rating,
            'user_review': review,
            'ai_response': response
        }
        df = load_data()
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        save_data(df)
        
        st.success("✅ Review submitted!")
        st.write("**AI Response:**", response)
