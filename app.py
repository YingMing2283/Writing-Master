#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer, MarianMTModel, MarianTokenizer
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to load the GPT-2 Large model and tokenizer
@st.cache(allow_output_mutation=True)
def load_gpt2_large_model():
    try:
        model_name = "gpt2-large"
        model = GPT2LMHeadModel.from_pretrained(model_name)
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        logging.error(f"Error loading GPT-2 model: {e}")
        st.error("Error loading GPT-2 model. Please check the logs.")

# Function to load MarianMT models for Malay and Chinese translation
@st.cache(allow_output_mutation=True)
def load_translation_model(language):
    try:
        if language == "Malay":
            model_name = "Helsinki-NLP/opus-mt-en-ms"
        elif language == "Chinese":
            model_name = "Helsinki-NLP/opus-mt-en-zh"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        logging.error(f"Error loading translation model for {language}: {e}")
        st.error(f"Error loading translation model for {language}. Please check the logs.")

# Function to translate text
def translate_text(text, model, tokenizer):
    try:
        input_ids = tokenizer.encode(text, return_tensors="pt")
        outputs = model.generate(input_ids)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        st.error("Error translating text. Please check the logs.")

# Load the GPT-2 Large model and tokenizer
gpt2_large_model, gpt2_large_tokenizer = load_gpt2_large_model()

# Streamlit interface
st.title("Writing Master")
st.write("A tool to help you write formal letters, agreements, etc., in English, Malay, and Chinese.")

language = st.selectbox("Select Language", ["English", "Malay", "Chinese"])
input_text = st.text_area("Enter the details of the letter/agreement:")

def generate_text(input_text, language):
    try:
        if language != "English":
            # Translate input to English
            translation_model, translation_tokenizer = load_translation_model(language)
            translated_input = translate_text(input_text, translation_model, translation_tokenizer)
        else:
            translated_input = input_text
        
        # Construct a detailed and specific prompt for the letter
        prompt = (
            f"You are a Writing Master. Your task is to write a formal letter or agreement based on the provided details. "
            f"Make sure the writing is clear, simple, and easy to understand. Use the following template as a guide:\n\n"
            f"Details: {translated_input}\n\n"
            f"Example:\n\n"
            f"Dear [Recipient],\n\n"
            f"I am writing to inform you about the closure of our company and the subsequent need to close our bank account. "
            f"Due to the closure of the company, we need to close our bank account associated with the company. "
            f"Please let us know if you need any further information or if there are any additional steps we need to take.\n\n"
            f"Thank you for your understanding.\n\n"
            f"Sincerely,\n"
            f"[Your Name]\n\n"
            f"Now write a similar letter based on the provided details:\n\n"
        )
        
        # Generate text in English using GPT-2 Large
        input_ids = gpt2_large_tokenizer.encode(prompt, return_tensors='pt')
        output = gpt2_large_model.generate(input_ids, max_length=300, num_return_sequences=1, temperature=0.7, top_p=0.9, top_k=50)
        generated_text = gpt2_large_tokenizer.decode(output[0], skip_special_tokens=True)
        
        if language != "English":
            # Translate the generated text back to the selected language
            reverse_translation_model, reverse_translation_tokenizer = load_translation_model(language)
            generated_text = translate_text(generated_text, reverse_translation_model, reverse_translation_tokenizer)
        
        return generated_text
    except Exception as e:
        logging.error(f"Error generating text: {e}")
        st.error("Error generating text. Please check the logs.")

if st.button("Generate"):
    generated_text = generate_text(input_text, language)
    if generated_text:
        st.write("Generated Text:")
        st.write(generated_text)

# Function to load MarianMT models for Malay and Chinese translation
@st.cache(allow_output_mutation=True)
def load_translation_model(language):
    try:
        if language == "Malay":
            model_name = "Helsinki-NLP/opus-mt-en-ms"
        elif language == "Chinese":
            model_name = "Helsinki-NLP/opus-mt-en-zh"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        return model, tokenizer
    except Exception as e:
        logging.error(f"Error loading translation model for {language}: {e}")
        st.error(f"Error loading translation model for {language}. Please check the logs.")

# Function to translate text
def translate_text(text, model, tokenizer):
    try:
        input_ids = tokenizer.encode(text, return_tensors="pt")
        outputs = model.generate(input_ids)
        translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        st.error("Error translating text. Please check the logs.")








