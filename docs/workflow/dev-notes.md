# Dev Notes (Read This Once)

These notes explain how to work locally without running into common issues.  
You do not need to memorize this. Just follow the rules.

---

## 0) Write access reminder

If you cannot push or open a PR:

1. Message the Project Team GC (Slack or Teams)
2. Send your GitHub username
3. A lane lead will add you

Example message:

```
"My GitHub username is: yourusername"
```

---

## DO

### Activate the virtual environment before running code

If you run Python scripts, notebooks, or Streamlit, activate the venv first.

macOS or Linux:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

If you see `(.venv)` in your terminal, you are good.

---

### Run commands from the project root

Always run commands from the project root folder:

```
stroke-prevention-demo/
```

Example:

```bash
streamlit run app/streamlit_app.py
```

---

### Install dependencies inside the venv

Only install packages after activating the venv:

```bash
pip install -r requirements.txt
```

---

### Use a new branch for each issue

```bash
git checkout -b feature/<issue-number>-short-name
```

Example:

```bash
git checkout -b feature/23-disclaimer-text
```

---

### Push small changes

- Partial notebooks are OK
- Draft PRs are OK
- Notes and docs count

Progress beats perfection.

---

## DONT

### Do not cd into .venv

The venv is activated, not entered.

Bad:

```bash
cd .venv
```

Good:

```bash
source .venv/bin/activate
```

---

### Do not run code without the venv active

If you do not see `(.venv)` in your terminal, stop and activate it.

---

### Do not commit .venv/

`.venv/` is local only.

If it is accidentally staged:

```bash
git restore --staged .venv
```

---

### Do not install packages globally

Avoid installing Python packages outside the venv.

---

### Do not work on main

Always work on a feature branch and open a PR.

---

## If you are stuck

Paste the exact error message in:

1. The GitHub issue comments
2. The Project Team GC (if urgent)

Do not summarize the error. Copy paste it.

