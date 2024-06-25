#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer, MarianMTModel, MarianTokenizer

# Function to load the GPT-2 model and tokenizer
@st.cache(allow_output_mutation=True)
def load_gpt2_model():
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    return model, tokenizer

# Function to load MarianMT models for Malay and Chinese translation
@st.cache(allow_output_mutation=True)
def load_translation_model(language):
    if language == "Malay":
        model_name = "Helsinki-NLP/opus-mt-en-ms"
    elif language == "Chinese":
        model_name = "Helsinki-NLP/opus-mt-en-zh"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Function to translate text
def translate_text(text, model, tokenizer):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text

# Load the GPT-2 model and tokenizer
gpt2_model, gpt2_tokenizer = load_gpt2_model()

# Streamlit interface
st.title("Writing Master")
st.write("A tool to help you write formal letters, agreements, etc., in English, Malay, and Chinese.")

language = st.selectbox("Select Language", ["English", "Malay", "Chinese"])
input_text = st.text_area("Enter the details of the letter/agreement:")

def generate_text(input_text, language):
    if language != "English":
        # Translate input to English
        translation_model, translation_tokenizer = load_translation_model(language)
        translated_input = translate_text(input_text, translation_model, translation_tokenizer)
    else:
        translated_input = input_text
    
    # Construct a detailed and specific prompt for the letter
    prompt = (
        f"You are a Writing Master. Your task is to write a formal letter or agreement based on the provided details. "
        f"Make sure the writing is clear, simple, and easy to understand.\n\n"
        f"Details: {translated_input}\n\n"
        f"Letter/Agreement:\n"
        f"Dear [Recipient],\n\n"
        f"I am writing to inform you about the closure of our company and the subsequent need to close our bank account. "
        f"Due to the closure of the company, we need to close our bank account associated with the company. "
        f"Please let us know if you need any further information or if there are any additional steps we need to take.\n\n"
        f"Thank you for your understanding.\n\n"
        f"Sincerely,\n"
        f"[Your Name]\n"
    )
    
    # Generate text in English using GPT-2
    input_ids = gpt2_tokenizer.encode(prompt, return_tensors='pt')
    output = gpt2_model.generate(input_ids, max_length=300, num_return_sequences=1, temperature=0.7, top_p=0.9, top_k=50)
    generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)
    
    if language != "English":
        # Translate the generated text back to the selected language
        reverse_translation_model, reverse_translation_tokenizer = load_translation_model(language)
        generated_text = translate_text(generated_text, reverse_translation_model, reverse_translation_tokenizer)
    
    return generated_text

if st.button("Generate"):
    generated_text = generate_text(input_text, language)
    st.write("Generated Text:")
    st.write(generated_text)

# Function to load MarianMT models for Malay and Chinese translation
@st.cache(allow_output_mutation=True)
def load_translation_model(language):
    if language == "Malay":
        model_name = "Helsinki-NLP/opus-mt-en-ms"
    elif language == "Chinese":
        model_name = "Helsinki-NLP/opus-mt-en-zh"
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Function to translate text
def translate_text(text, model, tokenizer):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_text







