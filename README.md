# Stroke Prevention Demo

Educational Streamlit dashboard for exploring stroke risk patterns in an
NHANES-derived public health dataset. The app estimates relative stroke-risk
scores, shows model drivers, simulates prevention-oriented "what if" scenarios,
and surfaces subgroup fairness limitations.

This is a demo and data-literacy project, not a medical device or diagnostic
tool.

## What Is Included

- Multi-page Streamlit app in `app/`
- Main modeling page labeled **Stroke Model**
- Reproducible baseline model training from `data/raw/stroke_data.csv`
- App copy, disclaimers, and input schema in `docs/app_content/`
- Supporting model reports in `reports/`
- Exploratory notebooks and extended analyses in `notebooks/` and `extra_analysis/`

## Quick Start

Use Python 3.10 or newer.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/Stroke_Model.py
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app/Stroke_Model.py
```

The app trains the baseline model once at startup from the checked-in CSV. A
serialized model artifact is not required to run the dashboard.

## Optional Analysis Environment

Install notebook and plotting tools only if you plan to work in the exploratory
notebooks:

```bash
pip install -r requirements-dev.txt
```

## Verification

```bash
python3 -m compileall -q app src
python3 src/train_baseline.py
```

## Medical Disclaimer

The model is trained on survey data and has not been clinically validated. Do
not use outputs from this project to diagnose, treat, or manage a medical
condition. Consult a qualified healthcare professional for medical guidance.
