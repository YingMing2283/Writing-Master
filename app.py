import streamlit as st
import openai
from docx import Document
from PyPDF2 import PdfReader
from langdetect import detect
from googletrans import Translator
import pytesseract
from PIL import Image

# Set up OpenAI API key
openai.api_key = st.secrets["API_KEY"]

# Initialize translator
translator = Translator()

# Function to extract text from uploaded files (added JPEG support)
def extract_text(file):
    try:
        # For PDF files
        if file.type == "application/pdf":
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        
        # For Word documents
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(file)
            return "\n".join([para.text for para in doc.paragraphs])
        
        # For JPEG/Image files (OCR)
        elif file.type in ["image/jpeg", "image/png"]:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
            return text
        
        else:
            return None
            
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None

# Function to generate formal letters
def generate_formal_letter(language, recipient, subject, content):
    prompt = f"Write a formal letter in {language} to {recipient} about {subject}. Content: {content}"
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

# Function to explain document content
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
        # ... (keep existing code unchanged) ...

    elif option == "Translate Document":
        st.header("Translate Document")
        uploaded_file = st.file_uploader("Upload a document (PDF, Word, JPEG)", 
                                       type=["pdf", "docx", "jpg", "jpeg"])
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
        uploaded_file = st.file_uploader("Upload a document (PDF, Word, JPEG)", 
                                       type=["pdf", "docx", "jpg", "jpeg"])
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
