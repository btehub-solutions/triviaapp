import streamlit as st
import requests
import random

# Function to fetch trivia questions
def fetch_questions(difficulty):
    url = f"https://opentdb.com/api.php?amount=10&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    data = response.json()
    return data['results']

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = 0

st.title("Nigeria Trivia Quiz")

difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

# Start quiz button
if st.button("Start Quiz"):
    st.session_state.questions = fetch_questions(difficulty)
    st.session_state.score = 0
    st.session_state.current = 0

# Show current question
if st.session_state.questions:
    q = st.session_state.questions[st.session_state.current]
    st.subheader(f"Q{st.session_state.current + 1}: {q['question']}")

    options = q['incorrect_answers'] + [q['correct_answer']]
    random.shuffle(options)

    user_answer = st.radio("Choose an answer:", options)

    if st.button("Submit Answer"):
        if user_answer == q['correct_answer']:
            st.session_state.score += 1
        if st.session_state.current + 1 < len(st.session_state.questions):
            st.session_state.current += 1
        else:
            st.write(f"Quiz finished! Your score: {st.session_state.score}/{len(st.session_state.questions)}")
            st.session_state.questions = []
