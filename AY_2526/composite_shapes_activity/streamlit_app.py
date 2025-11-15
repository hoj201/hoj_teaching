import streamlit as st
import pandas as pd
import random

answer_key = pd.read_csv("fixtures/answer_key.csv", index_col="Question", dtype={"Answer": float})
with open("fixtures/success_images.txt") as f:
    success_images = f.read().splitlines()

st.title("Composite shapes")
with open("fixtures/directions.md") as f:
    directions = f.read()
st.markdown(directions)
st.latex(r"\pi \approx 3.14")
st.write("Area of a rectangle: length × width")
st.write("Area of a triangle: ½ × base × height")
st.write("Area of a circle: π × radius²")

st.header("Check your answers")
selected_question = st.text_input("Question", value="", max_chars=1, key="question_select").upper()
if selected_question not in answer_key.index.get_level_values("Question"):
    st.error("Please enter a valid question. Available questions are: " + ", ".join(answer_key.index.get_level_values("Question")))

submitted_answer = st.text_input("Your answer", value="", key="answer_input")

try:
    submitted_answer = float(submitted_answer)
except ValueError:
    st.error("Please enter a valid number for your answer. Round to two decimal places. For example, enter 12.34.")

if st.button("Check answer"):
    correct_answer = answer_key.loc[selected_question]["Answer"]
    if abs(submitted_answer - correct_answer) < 0.1:
        random.seed(selected_question)
        gif_url = random.choice(success_images)
        st.image(gif_url)
        st.success("Correct!  Ask Mr. Jacobs or Mrs. Finan for another card.")
    else:
        st.error(f"Sorry, try again")