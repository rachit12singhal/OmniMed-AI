import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv
from fpdf import FPDF
# Import our new persistent database engine layers
from database import init_db, get_patient_profile, update_patient_profile, get_chat_history, save_chat_message, clear_chat_history

# 1. Initialize & Seed Database File
init_db()
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("🔑 GROQ_API_KEY not found in your .env file. Please check your configurations.")
    st.stop()

client = Groq(api_key=api_key)

# 2. UI/UX Page Layout Configuration
st.set_page_config(
    page_title="OmniMed AI Doctor | Clinical Assistant", 
    page_icon="🩺", 
    layout="wide"
)

# Sidebar Navigation Control
st.sidebar.markdown("### Navigation")
if st.sidebar.button("🏠 Back to Landing Page", use_container_width=True):
    st.switch_page("pages/home.py")
st.sidebar.markdown("---")

# Enterprise CSS Styling Grid
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6, 
    .main p, .main span, .main label, .main li, .main ol, .main ul { color: #1E293B !important; }
    .stChatMessage [data-testid="stMarkdownContainer"] p,
    .stChatMessage [data-testid="stMarkdownContainer"] li { color: #1E293B !important; }
    .stChatMessage { border-radius: 12px; padding: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
    .sidebar .stButton>button { border-radius: 6px; border: 1px solid #008080; }
    </style>
""", unsafe_allow_html=True)

st.title("🩺 OmniMed AI Doctor")
st.subheader("AI-Powered Clinical Diagnosis & Symptom Assistant")

st.warning(
    "⚠️ **Clinical Disclaimer:** This application leverages Generative AI for preliminary symptom analysis and "
    "educational guidance. It does not provide definitive medical diagnoses, prescriptions, or clinical treatment plans. "
    "Always consult a licensed medical professional for urgent clinical concerns."
)
st.markdown("---")

# 3. Pull Current Database States into Memory Abstraction
db_profile = get_patient_profile(patient_id=1)
st.session_state.age = db_profile["age"]
st.session_state.gender = db_profile["gender"]
st.session_state.messages = get_chat_history(patient_id=1)

# Sidebar Panel: Profile Configurations & State Management
with st.sidebar:
    st.header("👤 Patient Profile")
    
    input_age = st.number_input("Demographic Age", min_value=1, max_value=120, value=int(st.session_state.age))
    input_gender = st.selectbox("Biological Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(st.session_state.gender))
    
    if st.button("Save & Update Profile", use_container_width=True):
        update_patient_profile(input_age, input_gender, patient_id=1)
        st.success(f"Profile saved to database: {input_age}yo {input_gender}")
        st.rerun()

    st.divider()
    
    st.markdown("### 📊 Session Status")
    st.metric(label="Total Saved Interactions", value=len(st.session_state.messages))
    
    if len(st.session_state.messages) > 0:
        if st.sidebar.button("🗑️ Clear Database History", use_container_width=True, type="secondary"):
            clear_chat_history(patient_id=1)
            st.rerun()

    st.divider()
    
    # PDF Summary Document Exporter Engine
    if len(st.session_state.messages) > 0:
        st.header("📄 Clinical Export")
        if st.button("Compile Medical Summary", use_container_width=True):
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="OmniMed AI - Clinical Summary Report", ln=True, align='C')
            pdf.ln(5)
            
            pdf.set_font("Arial", 'B', 11)
            pdf.cell(200, 10, txt=f"Patient Demographics: {st.session_state.age} Year Old {st.session_state.gender}", ln=True)
            pdf.line(10, 32, 200, 32)
            pdf.ln(5)
            
            for msg in st.session_state.messages:
                role_label = "PATIENT" if msg['role'] == "user" else "CLINICAL AI ASSISTANT"
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(0, 6, txt=f"{role_label}:", ln=True)
                
                raw_content = str(msg['content'])
                raw_content = raw_content.replace("°", " degrees ").replace("—", " - ").replace("–", " - ")
                clean_content = raw_content.encode('ascii', 'ignore').decode('ascii')
                
                lines = clean_content.split('\n')
                for line in lines:
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    
                    try:
                        if clean_line.startswith("**") and clean_line.endswith("**"):
                            pdf.set_font("Arial", 'B', 10)
                            text = clean_line.replace("**", "")
                            pdf.multi_cell(0, 5, txt=text)
                        elif clean_line.startswith("**"):
                            pdf.set_font("Arial", 'B', 10)
                            text = clean_line.replace("**", "")
                            pdf.multi_cell(0, 5, txt=text)
                        elif clean_line.startswith("* ") or clean_line.startswith("- "):
                            pdf.set_font("Arial", size=10)
                            text = f"  . {clean_line[2:]}" 
                            pdf.multi_cell(0, 5, txt=text)
                        elif clean_line.startswith("+ "):
                            pdf.set_font("Arial", size=10)
                            text = f"    - {clean_line[2:]}"
                            pdf.multi_cell(0, 5, txt=text)
                        else:
                            pdf.set_font("Arial", size=10)
                            pdf.multi_cell(0, 5, txt=clean_line)
                    except Exception:
                        try:
                            pdf.set_font("Arial", size=10)
                            pdf.multi_cell(0, 5, txt=str(clean_line.encode('latin-1', 'replace').decode('latin-1')))
                        except Exception:
                            pass
                    
                    pdf.ln(1)
                pdf.ln(3)
            
            try:
                pdf_output = pdf.output()
                pdf_bytes = pdf_output if isinstance(pdf_output, bytes) else bytes(pdf_output, 'latin-1')
            except Exception:
                pdf_bytes = bytes(pdf.output())

            st.download_button(
                label="📥 Download Clinical PDF",
                data=pdf_bytes,
                file_name=f"OmniMed_AI_Report_{st.session_state.age}_{st.session_state.gender}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# 4. Asynchronous Chat Interface Core Orchestration Flow
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Describe your current symptoms or triage concerns..."):
    # Save the human prompt to the database permanently
    save_chat_message("user", prompt, patient_id=1)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        system_prompt = {
            "role": "system", 
            "content": (
                f"You are a sophisticated, highly analytical medical diagnostic AI assistant. "
                f"The current user context profile is a {st.session_state.age}-year-old {st.session_state.gender}. "
                f"Analyze their symptoms carefully considering their age and gender parameters. "
                f"Structure your clinical findings clearly with bullet points. "
                f"Always provide actionable triage tracking (e.g., when to rest vs. when to go to the emergency room). "
                f"Maintain an empathetic, professional clinical tone, and end with an appropriate disclaimer."
            )
        }
        
        # Pull the fully updated contextual log history straight from the database
        active_history = get_chat_history(patient_id=1)
        
        try:
            response = client.chat.completions.create(
                messages=[system_prompt] + active_history,
                model="llama-3.3-70b-versatile",
                temperature=0.3  
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            
            # Save the AI response to the database permanently
            save_chat_message("assistant", full_response, patient_id=1)
        except Exception as e:
            st.error(f"Execution Error dispatched from Inference Node: {e}")
            
    st.rerun()