# Workflow, Collaboration & Notebook Guidelines

> New to the project? See [setup.md](setup.md) first to get write access and set up your environment.

---

## Daily Workflow

Follow these steps every time you work on the project.

### 1. Open the project

- Open VS Code
- Open the `stroke-prevention-demo` folder
- Open the terminal in VS Code

---

### 2. Sync with main (required every session)

Always start here.

```bash
git checkout main
git pull origin main
git status
```

You should see:

- `On branch main`
- `Your branch is up to date` (or it will show your local changes)

---

### 3. Create or switch to your feature branch

Branch format:

```
feature/<ticket-id>-short-name
```

Examples:

- `feature/DP1-baseline-model`
- `feature/DC3-disclaimer-text`
- `feature/APP2-example-mode`

**First time on this ticket — create a new branch:**

```bash
git checkout -b feature/<ticket-id>-short-name
```

**Returning to an existing branch:**

```bash
git checkout feature/<ticket-id>-short-name
```

Rules:

- Do NOT work on `main`
- One ticket = one branch

---

### 4. Activate the venv (if running Python)

See [setup.md](setup.md) for your OS-specific activation command.
You should see `(.venv)` in your terminal. If you are only editing docs, skip this step.

---

### 5. Do your work

- Save files frequently
- Run your script or notebook before pushing to confirm it works

---

### 6. Stage, commit, and push

**Check what changed:**

```bash
git status
```

**Stage your changes:**

```bash
git add notebooks/        # for notebooks
git add docs/             # for docs
git add src/ app/ reports/ # for code
```

**Commit:**

```bash
git commit -m "<ticket-id>: short description"
```

Examples:

```bash
git commit -m "DP-1: baseline logistic regression + metrics"
git commit -m "DC-3: add disclaimer + limitations text"
git commit -m "APP-2: add example mode toggle"
```

Small commits are OK. Draft work is OK.

**Push:**

```bash
git push origin feature/<ticket-id>-short-name
```

---

### 7. Open or update your Pull Request (PR)

- Go to GitHub
- Click **Compare & pull request**
- In the PR description, include:

```
Closes #<github-issue-number>
Ticket: <ticket-id>
```

Draft PRs are allowed.

---

**One-line summary:**
Sync main → create branch → activate venv → do work → commit small → push → open PR

---

## Collaboration Rules

The default rule: **one ticket = one person = one branch = one PR.**

Only share a branch if a lane lead says you are pairing.

---

### Pairing on the same ticket

**Step 1 — Branch owner creates and pushes the branch:**

```bash
git checkout -b feature/DP1-baseline-model
git push origin feature/DP1-baseline-model
```

**Step 2 — Partner joins the branch:**

```bash
git checkout main
git pull origin main
git checkout feature/<ticket-id>-short-name
git pull origin feature/<ticket-id>-short-name
```

**Step 3 — Avoid conflicts:**

- Do not edit the same lines at the same time
- If you are both working in notebooks, use separate notebook files (see Notebook Guidelines below)
- For docs, decide who edits which section before typing

**Step 4 — Keep the branch updated (before every push):**

```bash
git pull origin feature/<ticket-id>-short-name
git status
git add .
git commit -m "<ticket-id>: short description"
git push origin feature/<ticket-id>-short-name
```

---

### Merge conflicts

Do not panic.

1. Stop
2. Paste the conflict text into the GitHub issue comments
3. Tag your lane lead in the Project Team GC

---

### Communication rule

If you are stuck for more than 5 minutes:

- Comment the blocker on the GitHub issue
- Tag your lane lead

---

## Notebook Guidelines

Notebooks are for exploration, testing ideas, and sharing findings. They should not replace `src/` code that needs to be reused.

---

### Where notebooks go

All notebooks must go in:

```
notebooks/
```

---

### Naming convention (required)

Each person uses their own notebook file. Never overwrite someone else's notebook.

Format:

```
<netid>_<ticket-id>_<short-name>.ipynb
```

Examples:

- `dokeke_DP3_data-sanity-check.ipynb`
- `edarkwa_DC1_data-dictionary-explore.ipynb`
- `jdoe_DP1_baseline-logreg.ipynb`

> If you are pairing, each person still uses their own notebook.

---

### Required notebook structure

Every notebook must include these sections in order.

**1. Title and ownership (Markdown cell)**

```markdown
# <Short Title>


Ticket: <ticket-id>
Contributors: <contributor-names>
Goal: <1 sentence>
```

**2. Imports (Code cell)**

```python
import pandas as pd
import numpy as np
```

**3. Load data (Code cell)**

Use the project's loader if one exists. Otherwise, state the path clearly.

```python
df = pd.read_csv("data/raw/stroke_data.csv")
df.head()
```

**4. Analysis (Code and Markdown cells)**

Include at least two outputs, such as:

- Value counts
- Summary stats
- Missingness table
- Simple plot

**5. Conclusions (Markdown cell)**

Include 3–6 bullets covering:

- Key findings
- Recommended decision
- Open questions or concerns

---

### Submitting a notebook

- Follow the daily workflow above (branch → commit → push → PR)
- In the PR description, include:
  - `Closes #<github-issue-number>`
  - `Ticket: <ticket-id>`

---

**One-line summary:**
One person = one notebook, named with netID and ticket ID, submitted via PR.

