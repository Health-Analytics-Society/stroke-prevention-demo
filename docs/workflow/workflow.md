# Daily Workflow: How to Start, Pull, Work, and Push

Follow these steps every time you work on the project.

---

## 0) Before you start (required if you want to push)

If you cannot push to GitHub or open a PR, you probably do not have write access yet.

To get write access:

1. Message the Project Team GC (Slack or Teams)
2. Send your GitHub username
3. A lane lead will add you

Example message:

```
"My GitHub username is: yourusername"
```

---

## START OF EVERY WORK SESSION

### 1) Open the project

- Open VS Code
- Open the `stroke-prevention-demo` folder
- Open the terminal in VS Code

---

### 2) Sync your local code with main (required)

Always start here.

```bash
git checkout main
git pull origin main
git status
```

You should see:

- On branch main
- Working tree clean (or it will show your local changes)

---

### 3) Create or switch to your feature branch

Branch format:

```
feature/<ticket-id>-short-name
```

Examples:

- feature/DP1-baseline-model
- feature/DC3-disclaimer-text
- feature/APP2-example-mode

**If this is your first time working on the ticket**

Create a new branch:

```bash
git checkout -b feature/<ticket-id>-short-name
```

Example:

```bash
git checkout -b feature/DP-1-baseline-model
```

**If you already created your branch earlier**

Switch to it:

```bash
git checkout feature/<ticket-id>-short-name
```

Important:

- Do NOT work on main
- One ticket should normally equal one branch

---

### 4) Activate the virtual environment (only if running Python)

If you are running Python scripts, notebooks, or Streamlit, activate the venv first.

macOS or Linux:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

If you see `(.venv)` in your terminal, you are good.

If you are only editing docs, you can skip this step.

---

## WORK SESSION

- Do your work
- Save files frequently
- If you are coding, run the script or notebook before pushing

---

## END OF WORK SESSION (SAVE YOUR WORK)

### 5) Check what you changed

```bash
git status
```

---

### 6) Stage your changes

Examples:

For notebooks:

```bash
git add notebooks/
```

For docs:

```bash
git add docs/
```

For code:

```bash
git add src/ app/ reports/
```

---

### 7) Commit your changes

```bash
git commit -m "<ticket-id>: short description"
```

Examples:

```bash
git commit -m "DP-1: baseline logistic regression + metrics"
git commit -m "DC-3: add disclaimer + limitations text"
git commit -m "APP-2: add example mode toggle"
```

Small commits are OK.
Draft work is OK.

---

### 8) Push your branch

```bash
git push origin feature/<ticket-id>-short-name
```

Branches show up on GitHub only after pushing.

---

### 9) Open or update your Pull Request (PR)

- Go to GitHub
- Click "Compare & pull request"
- In the PR description, include:

```
Closes #<github-issue-number>
Ticket: <ticket-id>
```

Example:

```
Closes #26
Ticket: APP-2
```

Draft PRs are allowed.

---

## Important rules

- Always pull from main
- Never push to main
- One ticket equals one branch equals one PR (unless a lead says you are pairing)
- Do not commit .venv/
- If stuck for 5 minutes, post the exact error in the issue comments and tag your lane lead

---

## One line summary

Sync main → create branch → do work → commit small → push → open PR

