import streamlit as st
from predict import simplify_text
from utils.helpers import get_readability_score
from translator import detect_language, translate_text
from PyPDF2 import PdfReader
from docx import Document

st.set_page_config(page_title="Legal Simplifier", page_icon="⚖️", layout="wide")


def extract_text_from_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8", errors="ignore")


def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf = PdfReader(uploaded_file)
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def extract_text_from_docx(uploaded_file):
    doc = Document(uploaded_file)
    paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs).strip()


def extract_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return extract_text_from_txt(uploaded_file)
    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    if file_name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)

    return ""


st.title("⚖️ Multilingual Legal Simplifier")
st.write("Convert complex legal or formal text into simpler language in multiple languages.")

input_mode = st.radio("Choose input type", ["Type Text", "Upload Document"])

user_input = ""

if input_mode == "Type Text":
    user_input = st.text_area(
        "Enter a sentence or paragraph",
        height=200,
        placeholder="Paste legal or formal text here..."
    )
else:
    uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf", "docx"])

    if uploaded_file is not None:
        extracted_text = extract_text(uploaded_file)

        if extracted_text.strip():
            st.subheader("Extracted Text")
            st.text_area("Document Content", extracted_text, height=250)
            user_input = extracted_text
        else:
            st.warning("Could not extract text from the uploaded file.")

if st.button("Simplify"):
    if user_input.strip():
        try:
            detected_lang = detect_language(user_input)

            if detected_lang != "en":
                translated_to_english = translate_text(user_input, detected_lang, "en")
                result = simplify_text(translated_to_english)
                translated_back = translate_text(result["simplified_output"], "en", detected_lang)

                st.subheader("Detected Language")
                st.write(detected_lang)

                st.subheader("Translated to English")
                st.info(translated_to_english)

                st.subheader("Simplified English Output")
                st.success(result["simplified_output"])

                st.subheader("Simplified Output in Original Language")
                st.success(translated_back)

                st.subheader("Closest Matched Training Sentence")
                if result["matched_input"] is not None:
                    st.info(result["matched_input"])
                else:
                    st.info("No close match found")

                st.subheader("Similarity Score")
                st.write(round(result["similarity_score"], 4))

                st.subheader("Status")
                st.write(result["note"])

            else:
                result = simplify_text(user_input)

                st.subheader("Detected Language")
                st.write("en")

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

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter text or upload a document first.")