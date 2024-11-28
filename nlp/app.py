import streamlit as st
from streamlit_shortcuts import button, add_keyboard_shortcuts

color = st.color_picker("Pick A Color", "#00f900")

add_keyboard_shortcuts({"ArrowUp": "Flip",
                        "ArrowDown": "Flip", 
                        "ArrowRight": "Next",
                        "ArrowLeft": "Previous"})

# Sample flashcards (question-answer pairs)
flashcards = [
    {"question": "What is the capital of France?", "answer": "Paris"},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"},
    {"question": "What year did the Titanic sink?", "answer": "1912"},
]

# Track the current flashcard index
if 'index' not in st.session_state:
    st.session_state.index = 0

st.write(st.session_state)

# Display the current question
current_flashcard = flashcards[st.session_state.index]

# Create a button to toggle between the question and answer
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

if st.button("Flip"):
    st.session_state.show_answer = not st.session_state.show_answer

# Display either the question or the answer
if st.session_state.show_answer:
    st.write(f"**Answer:** {current_flashcard['answer']}")
else:
    st.write(f"**Question:** {current_flashcard['question']} - ")

# Buttons to move to the next or previous flashcard
col1, col2 = st.columns(2)
with col1:
    if st.button("Previous"):
        st.session_state.index = (st.session_state.index - 1) % len(flashcards)
        st.session_state.show_answer = False  # Reset to show question

with col2:
    if st.button("Next"):
        st.session_state.index = (st.session_state.index + 1) % len(flashcards)
        st.session_state.show_answer = False  # Reset to show question

st.write(st.session_state)