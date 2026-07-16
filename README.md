# OmniMed AI — Advanced Clinical Triage & Symptom Assistant

OmniMed AI is a production-grade Generative AI application engineered during the IBM Internship Track. It leverages state-of-the-art Large Language Models (LLMs) to bridge the gap between initial symptom awareness and actionable clinical triage pathways.

---

## 🚀 Key Features

- **Dynamic Context Engineering:** Captures demographic variables (Age and Biological Gender) and dynamically injects them into the system prompt array to contextualize risk assessments.
- **Low-Latency Inference Gateway:** Integrated with the serverless **Llama-3.3-70b** model via the Groq Cloud API, utilizing strict temperature controls (`0.3`) to dramatically reduce hallucinations.
- **Relational Persistence Layer:** Implements a localized relational storage configuration using **SQLite** to securely manage multi-turn conversation logs and patient profiles across browser sessions.
- **Defensive Export Pipeline:** Features a secure text-sanitation system built on **FPDF** that filters raw markdown outputs down to safe ASCII boundaries, generating instant clinical summary reports.

---

## 🏗️ Architecture Stack

- **Frontend Interface:** Streamlit (Python-native reactive state-management ecosystem)
- **Data Architecture:** SQLite3 (Local Transactional Datastore)
- **AI Core Execution:** Llama-3.3-70b Gateway API (Groq Serverless Architecture)
- **Document Engine:** FPDF (Defensive String Sanitation Pipeline)

---

## 🛠️ Installation & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rachit12singhal/OmniMed-AI
cd OmniMed-AI
