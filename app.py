import os
import streamlit as st
from dotenv import load_dotenv
from langchain.chains import AnalyzeDocumentChain
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_openai import OpenAI
from transformers import pipeline
from functools import lru_cache

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Localization dictionary
TRANSLATIONS = {
    "title": {
        "zh": "公司智能助手",
        "en": "Company AI Assistant",
        "ms": "Pembantu AI Syarikat"
    },
    "function_select": {
        "zh": "选择功能",
        "en": "Select Function",
        "ms": "Pilih Fungsi"
    },
    "write_letter": {
        "zh": "撰写正式信件",
        "en": "Write Formal Letter",
        "ms": "Tulis Surat Rasmi"
    },
    "document_analysis": {
        "zh": "文件分析",
        "en": "Document Analysis",
        "ms": "Analisis Dokumen"
    },
    "translation": {
        "zh": "翻译服务",
        "en": "Translation Service",
        "ms": "Perkhidmatan Terjemahan"
    },
    # Add more translations as needed
}

class TranslationSystem:
    def __init__(self):
        self.models = {
            ('en', 'ms'): pipeline("translation_en_to_ms", 
                                 model="Helsinki-NLP/opus-mt-en-ms"),
            ('ms', 'en'): pipeline("translation_ms_to_en", 
                                  model="Helsinki-NLP/opus-mt-ms-en"),
            ('zh', 'en'): pipeline("translation_zh_to_en",
                                 model="Helsinki-NLP/opus-mt-zh-en"),
            # Add more language pairs
        }
    
    @lru_cache(maxsize=100)
    def translate(self, text: str, source: str, target: str) -> str:
        if (source, target) in self.models:
            return self.models[(source, target)](text)[0]['translation_text']
        else:
            # Fallback to OpenAI translation
            return self.gpt_translate(text, source, target)
    
    def gpt_translate(self, text: str, source: str, target: str) -> str:
        prompt = f"Translate the following {source} text to {target}: {text}"
        response = OpenAI().invoke(prompt)
        return response.strip()

class DocumentAnalyzer:
    def __init__(self):
        self.qa_chain = AnalyzeDocumentChain(llm=OpenAI(temperature=0))
    
    def analyze(self, file_path: str, question: str) -> str:
        try:
            if file_path.endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            else:
                return "Unsupported file format"
            
            docs = loader.load()
            return self.qa_chain.run(input_documents=docs, question=question)
        except Exception as e:
            return f"Error analyzing document: {str(e)}"

def main():
    st.set_page_config(page_title="Company AI Assistant", layout="wide")
    
    # Initialize services
    translator = TranslationSystem()
    analyzer = DocumentAnalyzer()
    
    # Language selection
    lang = st.sidebar.selectbox(
        "🌐 Select Language / 选择语言 / Pilih Bahasa",
        options=["en", "zh", "ms"],
        format_func=lambda x: {"en": "English", "zh": "中文", "ms": "Bahasa Melayu"}[x]
    )
    
    # Function selection
    function = st.sidebar.radio(
        TRANSLATIONS["function_select"][lang],
        options=["write_letter", "document_analysis", "translation"],
        format_func=lambda x: TRANSLATIONS[x][lang]
    )
    
    # Main content
    st.header(TRANSLATIONS["title"][lang])
    
    if function == "write_letter":
        handle_letter_writing(lang, translator)
    elif function == "document_analysis":
        handle_document_analysis(lang, analyzer)
    elif function == "translation":
        handle_translation(lang, translator)

def handle_letter_writing(lang: str, translator: TranslationSystem):
    st.subheader(TRANSLATIONS["write_letter"][lang])
    letter_type = st.selectbox(
        "📝 Letter Type" if lang == "en" else 
        "信件类型" if lang == "zh" else "Jenis Surat",
        ["Official Inquiry", "Complaint", "Application"]
    )
    
    # Letter content input
    content = st.text_area(
        "📄 Enter letter details" if lang == "en" else 
        "输入信件内容" if lang == "zh" else "Masukkan butiran surat",
        height=200
    )
    
    if st.button("Generate Letter"):
        with st.spinner("Generating..."):
            prompt = f"Generate a formal {letter_type} letter in {lang}: {content}"
            response = OpenAI().invoke(prompt)
            st.write(response)

def handle_document_analysis(lang: str, analyzer: DocumentAnalyzer):
    st.subheader(TRANSLATIONS["document_analysis"][lang])
    uploaded_file = st.file_uploader(
        "📤 Upload Document (PDF/DOCX)" if lang == "en" else 
        "上传文件 (PDF/DOCX)" if lang == "zh" else "Muat Naik Dokumen (PDF/DOCX)",
        type=["pdf", "docx"]
    )
    
    if uploaded_file:
        question = st.text_input(
            "❓ Ask about the document" if lang == "en" else 
            "关于文档的问题" if lang == "zh" else "Soalan tentang dokumen"
        )
        
        if question:
            with st.spinner("Analyzing..."):
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                result = analyzer.analyze(temp_path, question)
                os.remove(temp_path)
                st.write(result)

def handle_translation(lang: str, translator: TranslationSystem):
    st.subheader(TRANSLATIONS["translation"][lang])
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            "From" if lang == "en" else "源语言" if lang == "zh" else "Dari",
            ["en", "zh", "ms"],
            format_func=lambda x: {"en": "English", "zh": "中文", "ms": "Bahasa Melayu"}[x]
        )
    
    with col2:
        target_lang = st.selectbox(
            "To" if lang == "en" else "目标语言" if lang == "zh" else "Ke",
            ["en", "zh", "ms"],
            format_func=lambda x: {"en": "English", "zh": "中文", "ms": "Bahasa Melayu"}[x]
        )
    
    text = st.text_area(
        "📝 Enter text to translate" if lang == "en" else 
        "输入要翻译的文本" if lang == "zh" else "Masukkan teks untuk diterjemahkan",
        height=150
    )
    
    if st.button("Translate"):
        with st.spinner("Translating..."):
            translated = translator.translate(text, source_lang, target_lang)
            st.write(translated)

if __name__ == "__main__":
    main()
