# Open Tickets

All currently open GitHub issues for this project, as of 2026-02-21.

---

## Issue #26 — "Example Mode" toggle (APP-2)

**Lane:** App  
**Difficulty:** 🟡 Medium  
**Dependencies:** ⛓️ Depends on: **APP-1 exists** (or equivalent Results section)

**Goal**  
Let users switch between "example output" and "real model output coming soon."

**Tasks**
- Add a checkbox/toggle: "Use example output"
- If checked, show:
  - Example risk score
  - Example prevention tips (3 bullets)
- If unchecked, show:
  - "Model output coming soon" message

**Output:** Streamlit app file(s)

---

## Issue #25 — Results section layout (placeholders only) (APP-1)

**Lane:** App  
**Difficulty:** 🟢 Easy  
**Dependencies:** ✅ none

**Goal**  
Make the Streamlit app look real even before model wiring is finished.

**Tasks**
- In Streamlit, add a Results section/page that shows:
  - Header: "Your Stroke Risk Score"
  - Placeholder: "Risk score: 12% (example)"
  - Header: "Prevention Tips"
  - Placeholder list of 3 bullets
  - Header: "Disclaimer"
  - Placeholder disclaimer text (or paste DC-3 if available)

**Output:** Streamlit app file(s)

---

## Issue #24 — Risk level labels (low/medium/high) (DC-5)

**Lane:** Docs + Content  
**Difficulty:** 🟢 Easy  
**Dependencies:** ⛓️ Depends on: **DP-1 baseline metrics OR at least seeing typical risk score range**

**Goal**  
Make the risk score easier to understand by adding simple labels.

**Tasks**
- Create: `docs/risk_level_labels.md`
- After seeing DP-1 outputs, choose bins like:
  - Low: __% to __%
  - Medium: __% to __%
  - High: above __%
- Add this sentence: "These are demo labels, not clinical thresholds."

**Output:** `docs/risk_level_labels.md`

---

## Issue #23 — Disclaimer + limitations text (DC-3)

**Lane:** Docs + Content  
**Difficulty:** 🟢 Easy  
**Dependencies:** ✅ none

**Goal**  
Have clean wording we can paste into the app, README, and final slides.

**Tasks**
- Create: `docs/disclaimer_and_limitations.md`
- Add these 3 sections:
  - **Not medical advice** (2–3 sentences)
  - **Educational purpose** (1–2 sentences)
  - **Limitations** (3 bullets)

**Output:** `docs/disclaimer_and_limitations.md`

---

## Issue #22 — Data sanity check notebook (DP-3)

**Lane:** Data + Pipeline  
**Difficulty:** 🟢 Easy  
**Dependencies:** ⛓️ Depends on: **Dataset loads successfully**

**Goal**  
Confirm the data looks normal before we trust any model results.

**Tasks**
- Create a notebook: `notebooks/data_sanity_check.ipynb`
- In the notebook, print:
  - Number of rows and columns
  - Stroke label counts and percent
  - Full list of column names
  - For 5 numeric columns: min and max values

**Output:** `notebooks/data_sanity_check.ipynb`

---

## Issue #18 — Draft "Recommended Next Steps" mapping (DC-2)

**Lane:** Docs + Content  
**Difficulty:** 🟡 Medium  
**Dependencies:** ⛓️ Depends on: **DC-1 has at least the key risk factor columns identified**

**Goal**  
Turn health inputs into clear "what to do next" tips that are easy to understand.

**Tasks**
- Create or edit: `docs/content/recommended_next_steps.md`
- Pick 10 modifiable factors that match real dataset columns (use DC-1)
- For each factor, write:
  - **Risk factor:**
  - **Why it matters:** (1 short sentence)
  - **Recommended next steps:** (2–3 bullets)

**Output:** `docs/content/recommended_next_steps.md`
