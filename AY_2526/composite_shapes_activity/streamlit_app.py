import streamlit as st
import pandas as pd

answer_key = pd.read_csv("fixtures/answer_key.csv", index_col="Question", dtype={"Answer": float})

st.title("Composite shapes")
with open("fixtures/directions.md") as f:
    directions = f.read()
st.markdown(directions)

st.header("Check your answers")
selected_question = st.text_input("Question", value="", max_chars=1, key="question_select").upper()
if selected_question not in answer_key.index.get_level_values("Question"):
    st.error("Please enter a valid question.")

submitted_answer = st.text_input("Your answer", value="", key="answer_input")

try:
    submitted_answer = float(submitted_answer)
except ValueError:
    st.error("Please enter a valid number for your answer.")

if st.button("Check answer"):
    correct_answer = answer_key.loc[selected_question]["Answer"]
    if abs(submitted_answer - correct_answer) < 0.1:
        st.success("Correct!")
    else:
        st.error(f"Incorrect. The correct answer is {correct_answer}.")