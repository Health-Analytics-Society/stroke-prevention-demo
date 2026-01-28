# stroke-prevention-demo

Polished web dashboard using public health data to explore stroke prevention patterns
and simulate a clinic-style outreach and decision-support workflow.

This project is developed by the **Health Analytics Society** as an interdisciplinary
health + data science initiative.

---

## 🎯 Project Goal
By the end of the semester, this project will deliver a **Streamlit dashboard** that:
- Predicts stroke risk using clinical and demographic features
- Explains predictions with interpretable biomarkers
- Visualizes dataset insights and model performance
- Serves as an educational and demo tool for health analytics

---

## 🧰 Tech Stack
- Python 3.10+
- Streamlit
- pandas, numpy
- scikit-learn
- matplotlib

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the repository (Preferably in VS Code Terminal)
```bash
git clone https://github.com/Health-Analytics-Society/stroke-prevention-demo.git
cd stroke-prevention-demo

2. Create and activate a virtual environment (no conda)

macOS / Linux

python3 -m venv .venv
source .venv/bin/activate


Windows (PowerShell)

py -m venv .venv

.\.venv\Scripts\Activate.ps1

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

3. Install dependencies
pip install -r requirements.txt

4. Run the Streamlit app
streamlit run app/streamlit_app.py


If the dashboard loads, your setup works ✅
