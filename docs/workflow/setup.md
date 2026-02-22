# First-Time Setup & Local Rules

Do this once when you join the project. Refer back as needed.

---

## Get write access

If you cannot push or open a PR, you need to be added first.

1. Message the Project Team GC (Slack or Teams)
2. Send your GitHub username
3. A lane lead will add you

```
"My GitHub username is: yourusername"
```

---

## Activate the virtual environment

Always activate the venv before running Python scripts, notebooks, or Streamlit.

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` in your terminal. If you do not, stop and activate it.

---

## Install dependencies

Only run this after activating the venv:

```bash
pip install -r requirements.txt
```

---

## Always run from the project root

Run all commands from `stroke-prevention-demo/`, not from inside a subfolder.

Example:

```bash
streamlit run app/streamlit_app.py
```

---

## DO / DON'T quick reference

**DO:**

- Activate the venv before running any code
- Run commands from the project root
- Install packages inside the venv only
- Push small changes — partial notebooks and draft PRs are OK
- Use a new branch for each ticket (see [workflow.md](workflow.md))

**DON'T:**

- Run code without `(.venv)` showing in your terminal
- `cd` into `.venv/` — activate it, don't navigate into it
- Install packages globally (outside the venv)
- Commit the `.venv/` folder
- Work directly on `main` — always use a feature branch

If `.venv/` is accidentally staged:

```bash
git restore --staged .venv
```

---

## If you are stuck

Paste the **exact error message** (do not summarize it) in:

1. The GitHub issue comments
2. The Project Team GC if it is urgent

Tag your lane lead.

