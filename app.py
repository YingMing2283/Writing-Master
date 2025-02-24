import streamlit as st
import openai
from docx import Document
from PyPDF2 import PdfReader
from fpdf import FPDF
from datetime import datetime  # For today's date

# Set up OpenAI API key
openai.api_key = st.secrets["API_KEY"]

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
    else:
        return None

# Function to generate formal letters
def generate_formal_letter(language, recipient, recipient_address, sender, sender_address, subject, content):
    # Format recipient and sender addresses with line breaks
    formatted_recipient_address = recipient_address.replace(", ", ",\n")
    formatted_sender_address = sender_address.replace(", ", ",\n")

    # Get today's date in the format: Day Month Year (e.g., 25 October 2023)
    today_date = datetime.today().strftime("%d %B %Y")

    prompt = (
        f"Write a formal letter in {language} with the following details:\n"
        f"Sender: {sender}\n"
        f"Sender Address: {formatted_sender_address}\n"
        f"Recipient: {recipient}\n"
        f"Recipient Address: {formatted_recipient_address}\n"
        f"Date: {today_date}\n"
        f"Subject: {subject}\n"
        f"Content: {content}\n\n"
        "Requirements:\n"
        "1. Use a professional letter format with proper address formatting.\n"
        "2. Keep the answer short, direct, and professional.\n"
        "3. Include the date at the top of the letter.\n"
        "4. Provide clear explanations in layman's terms when necessary."
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

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

# Function to summarize document content
def summarize_document(text, language):
    prompt = f"Summarize the following document in {language}:\n{text}\n\nKeep the summary concise and clear."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

# Function to create a PDF from text
def create_pdf(text, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Add text to PDF (multi_cell for wrapping text)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(filename)

# Streamlit app
def main():
    st.title("Company AI Assistant")
    st.sidebar.header("Navigation")
    option = st.sidebar.selectbox("Choose a feature", ["Write Formal Letter", "Explain Document"])

    if option == "Write Formal Letter":
        st.header("Write a Formal Letter")
        language = st.selectbox("Select Language", ["English", "Chinese", "Malay"])
        recipient = st.text_input("Recipient Name")
        recipient_address = st.text_area("Recipient Address (e.g., Andy Law\nLot 4353, Taman Niaga\n98000 Miri\nSarawak)")
        sender = st.text_input("Sender Name")
        sender_address = st.text_area("Sender Address (e.g., Majlis Bandaraya Miri\nLot 1234, Marina Bay\n96100 Miri\nSarawak)")
        subject = st.text_input("Subject")
        content = st.text_area("Content")
        if st.button("Generate Letter"):
            letter = generate_formal_letter(language, recipient, recipient_address, sender, sender_address, subject, content)
            st.write("Generated Letter:")
            st.write(letter)

            # Create a PDF and provide a download button
            pdf_filename = "formal_letter.pdf"
            create_pdf(letter, pdf_filename)
            with open(pdf_filename, "rb") as file:
                st.download_button(
                    label="Download Letter as PDF",
                    data=file,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )

    elif option == "Explain Document":
        st.header("Explain Document")
        uploaded_file = st.file_uploader("Upload a document (PDF or Word)", type=["pdf", "docx"])
        if uploaded_file:
            text = extract_text(uploaded_file)
            if text:
                st.write("Extracted Text:")
                st.write(text)

                # Generate summary
                st.subheader("Document Summary")
                summary_language = st.selectbox("Select Summary Language", ["English", "Chinese", "Malay"])
                if st.button("Generate Summary"):
                    summary = summarize_document(text, summary_language)
                    st.write("Summary:")
                    st.write(summary)

                # Chatbot-like interface for further queries
                st.subheader("Chat with Document")
                user_query = st.text_input("Ask a question about the document")
                if user_query:
                    explanation = explain_document(text, user_query)
                    st.write("Answer:")
                    st.write(explanation)
            else:
                st.error("Unsupported file format or unable to extract text.")

if __name__ == "__main__":
    main()
