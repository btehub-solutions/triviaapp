import streamlit as st
import requests
import random
import html

# Initialize session state
if "started" not in st.session_state:
    st.session_state.started = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "current" not in st.session_state:
    st.session_state.current = 0

st.title("Nigeria Trivia Quiz")

difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

# Start quiz
if st.button("Start Quiz") and not st.session_state.started:
    url = f"https://opentdb.com/api.php?amount=10&category=23&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    st.session_state.questions = response.json()["results"]
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.started = True

# Show question only if quiz started
if st.session_state.started and st.session_state.questions:
    q = st.session_state.questions[st.session_state.current]
    st.subheader(f"Q{st.session_state.current + 1}: {html.unescape(q['question'])}")

    options = q["incorrect_answers"] + [q["correct_answer"]]
    random.shuffle(options)

    # Use radio button for user choice
    user_answer = st.radio("Choose an answer:", options, key=st.session_state.current)

    # Submit button
    if st.button("Submit Answer", key=f"submit{st.session_state.current}"):
        if user_answer == q["correct_answer"]:
            st.session_state.score += 1
        if st.session_state.current + 1 < len(st.session_state.questions):
            st.session_state.current += 1
        else:
            st.write(f"Quiz finished! Your score: {st.session_state.score}/{len(st.session_state.questions)}")
            st.session_state.started = False
