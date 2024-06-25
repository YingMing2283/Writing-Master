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

if st.button("Generate"):
    if language == "English":
        input_ids = gpt2_tokenizer.encode(input_text, return_tensors='pt')
        output = gpt2_model.generate(input_ids, max_length=500, num_return_sequences=1)
        generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)
    else:
        # Translate input to English
        translation_model, translation_tokenizer = load_translation_model(language)
        translated_input = translate_text(input_text, translation_model, translation_tokenizer)
        
        # Generate text in English using GPT-2
        input_ids = gpt2_tokenizer.encode(translated_input, return_tensors='pt')
        output = gpt2_model.generate(input_ids, max_length=500, num_return_sequences=1)
        generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Translate the generated text back to the selected language
        reverse_translation_model, reverse_translation_tokenizer = load_translation_model(language)
        generated_text = translate_text(generated_text, reverse_translation_model, reverse_translation_tokenizer)
    
    st.write("Generated Text:")
    st.write(generated_text)


