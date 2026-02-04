import streamlit as st
import fitz  # To read PDF
import re

# 1. Page Style & Colors (UI/UX)
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    .main-title { color: #ff4b4b; text-align: center; font-size: 45px; font-weight: bold; }
    .score-card { 
        background-color: white; padding: 25px; border-radius: 15px; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1); text-align: center;
    }
    .tag-found { background-color: #28a745; color: white; padding: 5px 12px; border-radius: 20px; margin: 3px; display: inline-block; }
    .tag-missing { background-color: #dc3545; color: white; padding: 5px 12px; border-radius: 20px; margin: 3px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

# 2. Function to read PDF
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.lower()

# --- APP UI ---
st.markdown("<h1 class='main-title'>🚀 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Unga Resume-ah AI moolama check panni skills-ah analyze pannunga!</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Step 1: Upload Resume")
    uploaded_file = st.file_uploader("Upload PDF format", type=["pdf"])

with col2:
    st.subheader("🎯 Step 2: Job Skills")
    skills_input = st.text_area("Enna skills venum? (Ex: Java, Python, SQL, Design)", height=150)

if st.button("🔍 ANALYZE NOW"):
    if uploaded_file and skills_input:
        with st.spinner('AI processing...'):
            # Text Extraction
            resume_text = extract_text(uploaded_file)
            
            # Simple Matching Logic
            target_skills = [s.strip().lower() for s in skills_input.split(',')]
            found = [s for s in target_skills if s in resume_text and len(s) > 1]
            missing = [s for s in target_skills if s not in found]
            
            score = (len(found) / len(target_skills)) * 100 if target_skills else 0

            # --- DISPLAY RESULTS ---
            st.balloons() # Success celebration!
            
            st.markdown(f"""
                <div class='score-card'>
                    <h2 style='color: #555;'>Match Percentage</h2>
                    <h1 style='color: #ff4b4b; font-size: 70px;'>{round(score, 1)}%</h1>
                </div>
            """, unsafe_allow_html=True)
            
            st.progress(score / 100)

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.success("### ✅ Skills Found")
                for s in found:
                    st.markdown(f"<span class='tag-found'>{s.upper()}</span>", unsafe_allow_html=True)
            
            with res_col2:
                st.error("### ❌ Missing Skills")
                for s in missing:
                    st.markdown(f"<span class='tag-missing'>{s.upper()}</span>", unsafe_allow_html=True)

            # --- DOWNLOAD OPTION ---
            report = f"Resume Analysis Report\nScore: {score}%\nFound: {', '.join(found)}\nMissing: {', '.join(missing)}"
            st.download_button("📥 Download Report", report, file_name="AI_Report.txt")
    else:
        st.warning("Please upload a file and enter skills!")