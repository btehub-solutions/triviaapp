import requests
import streamlit as st
import random
import html

st.title("Nigeria Trivia Quiz")

difficulty = st.selectbox("Select Difficulty", ["easy", "medium", "hard"])

if st.button("Start Quiz"):

    url = f"https://opentdb.com/api.php?amount=10&category=23&difficulty={difficulty}&type=multiple"
    response = requests.get(url)
    data = response.json()["results"]

    score = 0

    for i, q in enumerate(data):
        st.subheader(f"Question {i+1}")
        st.write(html.unescape(q["question"]))

        options = q["incorrect_answers"] + [q["correct_answer"]]
        random.shuffle(options)

        answer = st.radio("Choose an answer:", options, key=i)

        if st.button("Submit", key=f"submit{i}"):
            if answer == q["correct_answer"]:
                st.success("Correct!")
                score += 1
            else:
                st.error(f"Wrong! Correct answer: {q['correct_answer']}")

    st.write(f"Final Score: {score}/10")
