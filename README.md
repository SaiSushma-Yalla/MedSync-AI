MedSync AI — Medical Report Coordination Agent

MedSync AI is an AI-powered medical report coordination system that analyzes new medical reports alongside a patient's previous medical history to identify changes, potential coordination gaps, and follow-up recommendations for better continuity of care.

## Demo 
Demo Video:
https://github.com/user-attachments/assets/9919407b-7a95-45a3-98ef-7c9f8695d57f
Screenshots:
<img width="1920" height="1080" alt="Screenshot 2026-10-20 162124" src="https://github.com/user-attachments/assets/5aa73a5a-7a79-4977-9254-ebf4f7304a31" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 162105" src="https://github.com/user-attachments/assets/2bd64328-23cb-4662-92e2-9903574d0735" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 162058" src="https://github.com/user-attachments/assets/27cc0253-2208-4709-9a85-97d969ddc49f" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 162034" src="https://github.com/user-attachments/assets/11f06b97-3053-4267-bf6a-1554394c791a" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 162011" src="https://github.com/user-attachments/assets/d817e2a8-7cbd-492b-852f-893ad86d619f" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 161921" src="https://github.com/user-attachments/assets/3e7f70eb-da90-4e9d-89dc-cf77ecdd7fed" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 161833" src="https://github.com/user-attachments/assets/64c1a059-efc2-4862-b812-951271010fd9" />
<img width="1920" height="1080" alt="Screenshot 2026-10-20 161817" src="https://github.com/user-attachments/assets/65b6b158-f71d-45ef-87c6-dcfdc1d84669" />


Features

Medical Report Processing: Upload medical reports in PDF format and extract relevant information for analysis.

Patient History Tracking: Store and retrieve previous medical reports associated with the same patient using SQLite.

Historical Report Comparison: Compare a new report against earlier reports to identify changes and potential gaps in care coordination.

AI-Powered Reasoning: Use Groq's LLM API to analyze extracted information and generate insights.

Context-Aware Retrieval: Use FAISS-based vector search to retrieve relevant information from available medical report context.

Coordination Alerts: Highlight potential follow-up needs and coordination concerns based on the available report history.

Clinical Guideline Retrieval: Support analysis with relevant guideline information where configured.

Tech Stack

Language: Python

User Interface: Streamlit

LLM API: Groq API — Llama 3.3 70B Versatile

Database: SQLite

Vector Search: FAISS

Embeddings: Sentence Transformers (all-MiniLM-L6-v2)

Document Processing: PyMuPDF

Text Processing: LangChain Text Splitters

AI Workflow: Python-based processing pipeline

How to Run

Prerequisites

Python 3.11 or compatible version

Git

A Groq API key

1. Clone the repository

git clone https://github.com/SaiSushma-Yalla/MedSync-AI.git
cd MedSync-AI

2. Create a virtual environment

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

3. Install dependencies

If the repository contains a requirements.txt file, run:

pip install -r requirements.txt

Otherwise, install the dependencies used by the project, making sure their versions match your implementation.

4. Configure environment variables

Create a file named .env in the project root and add your Groq API key:

GROQ_API_KEY=your_groq_api_key_here

Make sure .env is included in .gitignore. Never commit your actual API key or real patient medical reports.

5. Run the application

streamlit run app.py

Open the local URL displayed in the terminal to access the application.

Known Limitations

AI-generated findings are intended to support medical information review and care coordination, not replace professional medical judgment.

The quality of the analysis depends on report readability, extracted information, and the availability of relevant historical records.

AI-generated alerts and recommendations may require verification by a qualified healthcare professional.

The application requires a valid Groq API key and an internet connection for LLM API calls.

This project is a prototype and has not been established as a clinically validated medical device.

Author

Gayatri NK  Sai Sushma Yalla





