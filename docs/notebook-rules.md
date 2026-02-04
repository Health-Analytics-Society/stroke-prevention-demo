# 📘 Week 2: Notebooks & Pull Request Instructions

## 🎯 Goal
Everyone submits **one Jupyter notebook (`.ipynb`)** showing data understanding or analysis.

---

## 1️⃣ Create Your Notebook (REQUIRED)

### 📁 Location
All notebooks must go in:
```

notebooks/

```

### 📝 Naming Convention
```

week2_<netid>_<issue>.ipynb

````

**Examples**
- `week2_edarkwa_missing_values.ipynb`
- `week2_jdoe_feature_types.ipynb`
- `week2_asmith_biomarkers.ipynb`

❌ Do not overwrite someone else’s notebook  
❌ Do not reuse the same filename  

---

## 2️⃣ Notebook Minimum Requirements

Your notebook must include **all five sections below**.

---

### 1. Title & Ownership (Markdown cell)

**This is required.**

```md
# Week 2 – Missing Values Analysis

**Name:** Emmanuel Darkwa  
**NetID:** edarkwa  
**Issue:** #12  

**Goal:** Analyze missing data and propose a handling strategy.
````

---

### 2. Imports (Code cell)

```python
import pandas as pd
import numpy as np
```

---

### 3. Load the Dataset (Code cell)

```python
df = pd.read_csv("data/raw/your_dataset.csv")
df.head()
```

---

### 4. Analysis (Code + Markdown)

Include **at least two outputs**, such as:

* missing value percentages
* summary statistics
* value counts
* simple plots

---

### 5. Conclusions (Markdown cell)

Include **3–6 bullet points**:

* key findings
* recommended decisions
* open questions or concerns

---

## 3️⃣ Create Your Branch (Before Working)

In the VS Code terminal:

```bash
git checkout -b feature/week2-your-task
```

Example:

```bash
git checkout -b feature/week2-missing-values
```

❌ Do **NOT** work on `main`.

---

## 4️⃣ Activate the Virtual Environment (Only if running code)

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

If you see `(.venv)` → you’re good.

---

## 5️⃣ Save, Commit, and Push

```bash
git add notebooks/
git commit -m "Week 2: add notebook for issue #<number>"
git push origin feature/week2-your-task
```

---

## 6️⃣ Open a Pull Request (PR)

1. Go to GitHub
2. Click **Compare & open pull request**
3. In the PR description, include:

```
Closes #<issue-number>
```

✅ Draft PRs are allowed
✅ Partial work is allowed

---

## 7️⃣ What Counts as Done

You are done for the week if you:

* opened a PR with your notebook **OR**
* opened a draft PR with partial analysis

> **Progress beats perfection.**

---

## ❗ Important Rules (Read Once)

* One person → one notebook
* One issue → one branch → one PR
* Do NOT share branches unless explicitly pairing
* Do NOT commit `.venv/`
* Ask for help early (post the exact error)

---

## 🧠 One-line Summary

> Create a notebook → include **Name + NetID** → commit → open a PR → done.

```

---

### Where to paste this
- ✅ `docs/week-2.md` (recommended)
- ✅ GitHub Issue description
- ✅ Slack → formatted code block
- ❌ Not inside a notebook

If you want, next I can:
- trim this into a **short Slack version**
- make a **Week 2 checklist slide**
- or create a **grading / review rubric** for notebooks
```
