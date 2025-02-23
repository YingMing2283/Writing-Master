import streamlit as st
import openai
from docx import Document
from PyPDF2 import PdfReader
from langdetect import detect
from googletrans import Translator
import easyocr
import io

# Set up OpenAI API key
openai.api_key = st.secrets["API_KEY"]

# Initialize translator
translator = Translator()

# Initialize EasyOCR for English, Chinese, and Malay, forcing CPU usage
reader = easyocr.Reader(['en', 'ch_sim', 'ms'], gpu=False)

def extract_text(file):
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
            return text if text else "No text could be extracted from the PDF."

        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            text = "\n".join([para.text for para in doc.paragraphs])
            return text if text else "No text could be extracted from the Word document."

        elif file.type in ["image/jpeg", "image/png"]:
            # Convert uploaded image to bytes for EasyOCR
            image_bytes = io.BytesIO(file.read())
            result = reader.readtext(image_bytes.getvalue(), detail=0)
            return " ".join(result) if result else "No text could be extracted from the image."

        else:
            return "Unsupported file format."
    except Exception as e:
        return f"An error occurred while extracting text: {str(e)}"

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
