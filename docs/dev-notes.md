# Developer Notes 

These notes explain how to work on this project locally without running into common issues.
You do **not** need to memorize this — just follow the rules below.

---

## ✅ DO

### Activate the virtual environment when running code
If you are running Python scripts, notebooks, or Streamlit, **activate the venv first**.

**macOS / Linux**
```bash
source .venv/bin/activate
````

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see:

```
(.venv)
```

at the start of your terminal prompt.

---

### Run commands from the project root

Always run commands from:

```
stroke-prevention-demo/
```

Example:

```bash
streamlit run app/streamlit_app.py
```

---

### Install dependencies inside the venv

Only install packages **after** activating the venv:

```bash
pip install -r requirements.txt
```

---

### Create a new branch for each issue

```bash
git checkout -b feature/week2-short-description
```

---

### Push small changes

* Partial notebooks are OK
* Draft PRs are OK
* Notes and docs count

Progress beats perfection.

---

## ❌ DON’T

### Don’t `cd` into `.venv`

The virtual environment is **activated**, not entered.

❌ Bad:

```bash
cd .venv
```

✅ Good:

```bash
source .venv/bin/activate
```

---

### Don’t run code without the venv active

If you don’t see `(.venv)` in your terminal, stop and activate it.

---

### Don’t commit `.venv/`

The `.venv/` folder is local-only and should never be pushed to GitHub.

If it’s accidentally staged:

```bash
git restore --staged .venv
```

---

### Don’t install packages globally

Avoid installing Python packages outside the venv.

---

### Don’t work directly on `main`

Always work on a feature branch and open a Pull Request.

---

## 🧠 One rule to remember

> **Activate venv → run code → commit small → open PR**

If you’re stuck, paste the **exact error message** in Slack.

```

---

## 📍 Where to paste it

1. GitHub → your repo  
2. **Add file → Create new file**  
3. Filename:
```

docs/dev-notes.md

```
4. Paste the content  
5. Click **Commit new file**

That’s it. Nothing else to copy.



Once this is committed, you’re done with dev notes.  
If you want, next we can set up a **PR template** or prep **Sprint 3 modeling issues**.
```
