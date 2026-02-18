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
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""

st.title("Nigeria Trivia Quiz")
difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

# Start Quiz
if st.button("Start Quiz") and not st.session_state.started:
    url = f"https://opentdb.com/api.php?amount=10&category=23&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    st.session_state.questions = response.json()["results"]
    st.session_state.score = 0
    st.session_state.current = 0
    st.session_state.started = True
    st.session_state.last_feedback = ""

# Show question if quiz started
if st.session_state.started and st.session_state.current < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current]
    st.subheader(f"Q{st.session_state.current + 1}: {html.unescape(q['question'])}")

    options = q["incorrect_answers"] + [q["correct_answer"]]
    random.shuffle(options)

    with st.form(key=f"question_form_{st.session_state.current}"):
        user_answer = st.radio("Choose an answer:", options)
        submit = st.form_submit_button("Submit Answer")
        if submit:
            if user_answer == q["correct_answer"]:
                st.session_state.score += 1
                st.session_state.last_feedback = "Correct!"
            else:
                st.session_state.last_feedback = f"Wrong! Correct answer: {q['correct_answer']}"
            st.session_state.current += 1

    # Show feedback for last question
    if st.session_state.last_feedback:
        st.info(st.session_state.last_feedback)
    st.write(f"Current Score: {st.session_state.score}")

# Show final score
if st.session_state.started and st.session_state.current >= len(st.session_state.questions):
    st.write(f"Quiz finished! Your score: {st.session_state.score}/{len(st.session_state.questions)}")
    st.session_state.started = False
