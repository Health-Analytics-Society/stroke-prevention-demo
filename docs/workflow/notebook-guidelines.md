# Notebook Guidelines

Notebooks help us explore data, test ideas, and share findings without breaking the main code.

---

## Where notebooks go

All notebooks must go in:

```
notebooks/
```

---

## Naming convention (required)

Each person must use their own notebook file.

Format:

```text
<netid>_<ticket-id>_<short-name>.ipynb
```

Examples:

- dokeke_DP3_data-sanity-check.ipynb
- edarkwa_DC1_data-dictionary-explore.ipynb
- jdoe_DP1_baseline-logreg.ipynb

Rules:

- Do not overwrite someone else's notebook
- Do not reuse the same filename
- If you are pairing, each person still uses their own notebook

---

## Minimum notebook structure (required)

Your notebook must include these sections.

### 1) Title and ownership (Markdown cell)

```markdown
# <Short Title>

Name: <Your Name>
NetID: <netid>
Ticket: <ticket-id>
GitHub Issue: #<github-issue-number> (if you know it)

Goal: <1 sentence>
```

---

### 2) Imports (Code cell)

```python
import pandas as pd
import numpy as np
```

---

### 3) Load data (Code cell)

Use the project's loader if one exists.
If not, clearly state the path you used.

Example:

```python
import pandas as pd
df = pd.read_csv("data/raw/stroke_data.csv")
df.head()
```

---

### 4) Analysis (Code and Markdown)

Include at least two outputs, such as:

- value counts
- summary stats
- missingness table
- simple plot

---

### 5) Conclusions (Markdown cell)

Include 3 to 6 bullets:

- key findings
- recommended decision
- open questions or concerns

---

## How notebooks get submitted

- Create a branch for your ticket (see workflow doc)
- Commit your notebook
- Open a PR
- In the PR description, include:
  - Closes #<github-issue-number>
  - Ticket: <ticket-id>

Draft PRs are allowed.

---

## One line summary

One person equals one notebook, named with netID and ticket id, submitted via PR.

