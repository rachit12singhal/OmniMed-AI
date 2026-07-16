import streamlit as st

# 1. UI/UX Page Layout Configuration
st.set_page_config(page_title="OmniMed AI | Portal Home", layout="wide")

# 2. Custom CSS Styles
st.markdown("""
    <style>
    .hero { text-align: center; padding: 60px 0; }
    .btn { font-size: 20px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. Hero Section Display Panel
st.markdown("""
    <div class="hero">
        <h1>Welcome to OmniMed AI 🩺</h1>
        <h3>Your AI-Powered Clinical Diagnostic Assistant</h3>
        <p>Empowering your health journey with real-time, professional analysis.</p>
    </div>
""", unsafe_allow_html=True)

# 4. Call to Action Routing Trigger
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 Start Your Consultation Now", use_container_width=True):
        st.switch_page("app.py")

st.markdown("---")

# 5. Founder Signature Profile Section
col_a, col_b = st.columns([1, 2])
with col_a:
    # Generates a clean profile avatar placeholder block showing your initials: RS
    st.image("https://ui-avatars.com/api/?name=Rachit+Singhal&size=200&background=E2E8F0&color=1E293B", width=200)
    
with col_b:
    st.subheader("Message from the Founder")
    st.write("**Rachit Singhal**")
    st.write(
        "\"I built OmniMed AI to bridge the gap between initial symptom awareness and clinical action. "
        "By putting immediate, safe triage tracking tools directly in the hands of patients, "
        "we can help people optimize how they engage with professional healthcare providers.\""
    )