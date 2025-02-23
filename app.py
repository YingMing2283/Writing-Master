import os
import streamlit as st
from langchain.chains import AnalyzeDocumentChain
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_openai import OpenAI
from transformers import pipeline
from functools import lru_cache

# Initialize OpenAI with Streamlit secrets
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
}

class TranslationSystem:
    def __init__(self):
        self.models = {
            ('en', 'ms'): pipeline("translation", model="Helsinki-NLP/opus-mt-en-ms"),
            ('ms', 'en'): pipeline("translation", model="Helsinki-NLP/opus-mt-ms-en"),
            ('zh', 'en'): pipeline("translation", model="Helsinki-NLP/opus-mt-zh-en"),
        }
    
    @lru_cache(maxsize=100)
    def translate(self, text: str, source: str, target: str) -> str:
        if (source, target) in self.models:
            return self.models[(source, target)](text)[0]['translation_text']
        else:
            return self.gpt_translate(text, source, target)
    
    def gpt_translate(self, text: str, source: str, target: str) -> str:
        prompt = f"Translate this {source} text to {target}: {text}"
        return OpenAI().invoke(prompt).strip()

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
            return f"Error: {str(e)}"

def main():
    st.set_page_config(page_title="Company AI Assistant", layout="wide")
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
        {"en": "📝 Letter Type", "zh": "信件类型", "ms": "Jenis Surat"}[lang],
        ["Official Inquiry", "Complaint", "Application"]
    )
    
    content = st.text_area(
        {"en": "📄 Enter details", "zh": "输入内容", "ms": "Masukkan butiran"}[lang],
        height=200
    )
    
    if st.button({"en": "Generate", "zh": "生成", "ms": "Hasilkan"}[lang]):
        with st.spinner({"en": "Generating...", "zh": "生成中...", "ms": "Menghasilkan..."}[lang]):
            prompt = f"Generate formal {letter_type} letter in {lang}: {content}"
            st.write(OpenAI().invoke(prompt))

def handle_document_analysis(lang: str, analyzer: DocumentAnalyzer):
    st.subheader(TRANSLATIONS["document_analysis"][lang])
    uploaded_file = st.file_uploader(
        {"en": "📤 Upload (PDF/DOCX)", "zh": "上传文件", "ms": "Muat Naik Dokumen"}[lang],
        type=["pdf", "docx"]
    )
    
    if uploaded_file:
        question = st.text_input(
            {"en": "❓ Ask about document", "zh": "文档问题", "ms": "Soalan dokumen"}[lang]
        )
        
        if question:
            with st.spinner({"en": "Analyzing...", "zh": "分析中...", "ms": "Menganalisis..."}[lang]):
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.write(analyzer.analyze(temp_path, question))
                os.remove(temp_path)

def handle_translation(lang: str, translator: TranslationSystem):
    st.subheader(TRANSLATIONS["translation"][lang])
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox(
            {"en": "From", "zh": "源语言", "ms": "Dari"}[lang],
            ["en", "zh", "ms"],
            format_func=lambda x: {"en": "English", "zh": "中文", "ms": "Bahasa Melayu"}[x]
        )
    
    with col2:
        target_lang = st.selectbox(
            {"en": "To", "zh": "目标语言", "ms": "Ke"}[lang],
            ["en", "zh", "ms"],
            format_func=lambda x: {"en": "English", "zh": "中文", "ms": "Bahasa Melayu"}[x]
        )
    
    text = st.text_area(
        {"en": "📝 Text to translate", "zh": "输入文本", "ms": "Teks untuk terjemah"}[lang],
        height=150
    )
    
    if st.button({"en": "Translate", "zh": "翻译", "ms": "Terjemah"}[lang]):
        with st.spinner({"en": "Translating...", "zh": "翻译中...", "ms": "Menterjemah..."}[lang]):
            st.write(translator.translate(text, source_lang, target_lang))

if __name__ == "__main__":
    main()
