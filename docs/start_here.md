# Start Here

This repository contains the Stroke Prevention Demo, an educational Streamlit
dashboard for exploring stroke risk prediction, prevention scenarios, and
fairness limitations with public health data.

## Run the App

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/Stroke_Model.py
```

The app entry point is `app/Stroke_Model.py`.

## Repository Map

- `app/` - Streamlit app pages and shared model/UI helpers
- `data/raw/` - NHANES-derived source CSV used by the demo
- `docs/app_content/` - user-facing FAQ, disclaimer, risk labels, and input schema
- `docs/reference/` - data dictionary, leakage notes, project state, and recaps
- `docs/workflow/` - contributor setup and collaboration guidance
- `extra_analysis/` - health equity and counterfactual analysis notebooks/figures
- `notebooks/` - exploratory notebooks
- `reports/` - model metrics and experiment results
- `src/` - reproducible training and experiment scripts

## Current Status

The dashboard is demo-ready for educational use. It is not a clinical product,
has not been externally validated, and should not be used for medical decisions.

See [project_state.md](reference/project_state.md) for the current model summary
and known limitations.
