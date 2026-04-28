# Setup Guide

Do this once when you join the project. Refer back as needed.

---

## 1. Get write access

If you cannot push or open a PR, you need to be added first.

1. Message the Project Team GC (Slack or Teams)
2. Send your GitHub username
3. A lane lead will add you

```
"My GitHub username is: yourusername"
```

---

## 2. Clone the repository

Run from wherever you want the project to live on your machine:

```bash
git clone https://github.com/<org>/stroke-prevention-demo.git
cd stroke-prevention-demo
```

---

## 3. Create the virtual environment

Do this once per machine.

**macOS / Linux:**

```bash
python3 -m venv .venv
```

**Windows (PowerShell):**

```powershell
python -m venv .venv
```

---

## 4. Activate the virtual environment

Do this every time you open a new terminal session.

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

> If you see a permissions error on Windows, run this once in PowerShell as Administrator, then try again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

You should see `(.venv)` in your terminal prompt. If you do not, stop and activate it before continuing.

---

## 5. Install dependencies

Only run this after activating the venv:

```bash
pip install -r requirements.txt
```

Run this again any time `requirements.txt` changes (e.g., after pulling new changes).

---

## 6. Always run from the project root

Run all commands from `stroke-prevention-demo/`, not from inside a subfolder.

**Example — launch the app:**

```bash
streamlit run app/Stroke_Model.py
```

**Example — run a script:**

```bash
python src/some_script.py
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

