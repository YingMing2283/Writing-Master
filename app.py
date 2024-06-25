{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "85b2af21-864e-4d85-a85c-cb130d6aee07",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-06-25 20:04:51.631 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\user\\New folder\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n",
      "2024-06-25 20:04:51.631 \n",
      "`st.cache` is deprecated and will be removed soon. Please use one of Streamlit's new caching commands, `st.cache_data` or `st.cache_resource`.\n",
      "More information [in our docs](https://docs.streamlit.io/develop/concepts/architecture/caching).\n",
      "\n",
      "**Note**: The behavior of `st.cache` was updated in Streamlit 1.36 to the new caching logic used by `st.cache_data` and `st.cache_resource`.\n",
      "This might lead to some problems or unexpected behavior in certain edge cases.\n",
      "\n",
      "2024-06-25 20:04:51.631 \n",
      "`st.cache` is deprecated and will be removed soon. Please use one of Streamlit's new caching commands, `st.cache_data` or `st.cache_resource`.\n",
      "More information [in our docs](https://docs.streamlit.io/develop/concepts/architecture/caching).\n",
      "\n",
      "**Note**: The behavior of `st.cache` was updated in Streamlit 1.36 to the new caching logic used by `st.cache_data` and `st.cache_resource`.\n",
      "This might lead to some problems or unexpected behavior in certain edge cases.\n",
      "\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "e6d952011e5446199baa49a4e98358c3",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "config.json:   0%|          | 0.00/665 [00:00<?, ?B/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\user\\New folder\\Lib\\site-packages\\huggingface_hub\\file_download.py:149: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in C:\\Users\\user\\.cache\\huggingface\\hub\\models--gpt2. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.\n",
      "To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to see activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development\n",
      "  warnings.warn(message)\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "aa3191bf317b4f35b0aea6f0c3a18d00",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "model.safetensors:   0%|          | 0.00/548M [00:00<?, ?B/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import streamlit as st\n",
    "from transformers import GPT2LMHeadModel, GPT2Tokenizer, MarianMTModel, MarianTokenizer\n",
    "\n",
    "# Function to load the GPT-2 model and tokenizer\n",
    "@st.cache(allow_output_mutation=True)\n",
    "def load_gpt2_model():\n",
    "    model_name = \"gpt2\"\n",
    "    model = GPT2LMHeadModel.from_pretrained(model_name)\n",
    "    tokenizer = GPT2Tokenizer.from_pretrained(model_name)\n",
    "    return model, tokenizer\n",
    "\n",
    "# Function to load MarianMT models for Malay and Chinese translation\n",
    "@st.cache(allow_output_mutation=True)\n",
    "def load_translation_model(language):\n",
    "    if language == \"Malay\":\n",
    "        model_name = \"Helsinki-NLP/opus-mt-en-ms\"\n",
    "    elif language == \"Chinese\":\n",
    "        model_name = \"Helsinki-NLP/opus-mt-en-zh\"\n",
    "    model = MarianMTModel.from_pretrained(model_name)\n",
    "    tokenizer = MarianTokenizer.from_pretrained(model_name)\n",
    "    return model, tokenizer\n",
    "\n",
    "# Function to translate text\n",
    "def translate_text(text, model, tokenizer):\n",
    "    input_ids = tokenizer.encode(text, return_tensors=\"pt\")\n",
    "    outputs = model.generate(input_ids)\n",
    "    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)\n",
    "    return translated_text\n",
    "\n",
    "# Load the GPT-2 model and tokenizer\n",
    "gpt2_model, gpt2_tokenizer = load_gpt2_model()\n",
    "\n",
    "# Streamlit interface\n",
    "st.title(\"Writing Master\")\n",
    "st.write(\"A tool to help you write formal letters, agreements, etc., in English, Malay, and Chinese.\")\n",
    "\n",
    "language = st.selectbox(\"Select Language\", [\"English\", \"Malay\", \"Chinese\"])\n",
    "input_text = st.text_area(\"Enter the details of the letter/agreement:\")\n",
    "\n",
    "if st.button(\"Generate\"):\n",
    "    if language == \"English\":\n",
    "        input_ids = gpt2_tokenizer.encode(input_text, return_tensors='pt')\n",
    "        output = gpt2_model.generate(input_ids, max_length=500, num_return_sequences=1)\n",
    "        generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)\n",
    "    else:\n",
    "        # Translate input to English\n",
    "        translation_model, translation_tokenizer = load_translation_model(language)\n",
    "        translated_input = translate_text(input_text, translation_model, translation_tokenizer)\n",
    "        \n",
    "        # Generate text in English using GPT-2\n",
    "        input_ids = gpt2_tokenizer.encode(translated_input, return_tensors='pt')\n",
    "        output = gpt2_model.generate(input_ids, max_length=500, num_return_sequences=1)\n",
    "        generated_text = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)\n",
    "        \n",
    "        # Translate the generated text back to the selected language\n",
    "        reverse_translation_model, reverse_translation_tokenizer = load_translation_model(language)\n",
    "        generated_text = translate_text(generated_text, reverse_translation_model, reverse_translation_tokenizer)\n",
    "    \n",
    "    st.write(\"Generated Text:\")\n",
    "    st.write(generated_text)\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8af5897f-4668-46e3-b016-92c3d7ad0b73",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
