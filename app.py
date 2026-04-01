import streamlit as st
from predict import simplify_text
from utils.helpers import get_readability_score

st.set_page_config(page_title="Legal Simplifier", page_icon="⚖️", layout="wide")

st.title("⚖️ Legal Simplifier")
st.write("Convert complex legal or formal text into simpler language.")

user_input = st.text_area(
    "Enter a sentence or paragraph",
    height=200,
    placeholder="Paste any complex sentence here..."
)

if st.button("Simplify"):
    if user_input.strip():
        result = simplify_text(user_input)

        st.subheader("Simplified Output")
        st.success(result["simplified_output"])

        st.subheader("Closest Matched Training Sentence")
        if result["matched_input"] is not None:
            st.info(result["matched_input"])
        else:
            st.info("No close match found")

        st.subheader("Similarity Score")
        st.write(round(result["similarity_score"], 4))

        st.subheader("Status")
        st.write(result["note"])

        readability = get_readability_score(result["simplified_output"])
        st.subheader("Readability Score")
        st.write(round(readability, 2))
    else:
        st.warning("Please enter some text first.")