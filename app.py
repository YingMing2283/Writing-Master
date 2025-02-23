import streamlit as st
import openai
from docx import Document
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from langdetect import detect
from googletrans import Translator

# Set up OpenAI API key
openai.api_key = st.secrets["API_KEY"]

# Initialize translator
translator = Translator()

# Function to extract text from uploaded files
def extract_text(file):
    if file.type == "application/pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    elif file.type == "image/jpeg" or file.type == "image/png":
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        return text
    else:
        return None

# Function to generate formal letters (FIXED)
def generate_formal_letter(language, recipient, subject, content):
    prompt = (
        f"Write a formal letter in {language} to {recipient} about '{subject}'.\n"
        f"Content: {content}\n\n"
        "Requirements:\n"
        "1. Keep the answer short, direct, and professional.\n"
        "2. Provide clear explanations in layman's terms when necessary."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Function to translate text
def translate_text(text, target_language):
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Function to explain document content (FIXED)
def explain_document(text, query):
    prompt = f"The following is a document:\n{text}\n\nAnswer this query based on the document: {query}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# Streamlit app
def main():
    st.title("Company AI Assistant")
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox("Choose a feature", ["Write Formal Letter", "Translate Document", "Explain Document"])

    if option == "Write Formal Letter":
        st.header("Write a Formal Letter")
        language = st.selectbox("Select Language", ["English", "Chinese", "Malay"])
        recipient = st.text_input("Recipient")
        subject = st.text_input("Subject")
        content = st.text_area("Content")
        if st.button("Generate Letter"):
            letter = generate_formal_letter(language, recipient, subject, content)
            st.write("Generated Letter:")
            st.write(letter)

    elif option == "Translate Document":
        st.header("Translate Document")
        uploaded_file = st.file_uploader("Upload a document (PDF or Word or JPEG)", type=["pdf", "docx", "jpeg"])
        target_language = st.selectbox("Select Target Language", ["English", "Chinese", "Malay"])
        if uploaded_file and target_language:
            text = extract_text(uploaded_file)
            if text:
                st.write("Extracted Text:")
                st.write(text)
                translated_text = translate_text(text, target_language)
                st.write("Translated Text:")
                st.write(translated_text)
            else:
                st.error("Unsupported file format or unable to extract text.")

    elif option == "Explain Document":
        st.header("Explain Document")
        uploaded_file = st.file_uploader("Upload a document (PDF or Word or JPEG)", type=["pdf", "docx", "jpeg"])
        query = st.text_input("Enter your query about the document")
        if uploaded_file and query:
            text = extract_text(uploaded_file)
            if text:
                st.write("Extracted Text:")
                st.write(text)
                explanation = explain_document(text, query)
                st.write("Explanation:")
                st.write(explanation)
            else:
                st.error("Unsupported file format or unable to extract text.")

if __name__ == "__main__":
    main()
