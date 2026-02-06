# Daily Workflow: How to Start, Pull, Work, and Push

Follow these steps **every time** you work on the project.

---

## 🟢 START OF EVERY WORK SESSION

### 1️⃣ Open Your Project
- Open **VS Code**
- Open the `stroke-prevention-demo` folder
- Open the terminal in VS Code

---

### 2️⃣ Go to `main` and pull latest changes (REQUIRED)
Always start here.

```bash
git checkout main
git pull origin main
````

Confirm:

```bash
git status
```

You should see:

```
On branch main
```

---

### 3️⃣ Create your feature branch (first time only)

If this is your **first time working on the issue**:

```bash
git checkout -b feature/week2-your-task
```

Example:

```bash
git checkout -b feature/week2-missing-values
```

⚠️ Do NOT work on `main`.

If you already created your branch previously, just switch to it:

```bash
git checkout feature/week2-your-task
```

---

### 4️⃣ Activate the virtual environment (only if running Python)

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
```

If you see `(.venv)` in the terminal, you’re good.

> If you are only editing docs, you can skip this step.

---

## 🧑‍💻 WORK SESSION

* Create or edit your notebook:

  ```
  notebooks/week2_<netid>_<issue>.ipynb
  ```
* Run analysis
* Save your work

---

## 🔵 END OF WORK SESSION (SAVE YOUR WORK)

### 5️⃣ Check what you changed

```bash
git status
```

---

### 6️⃣ Commit your changes

```bash
git add notebooks/
git commit -m "Week 2: add notebook for issue #<number>"
```

Small commits are OK.

---

### 7️⃣ Push your branch

```bash
git push origin feature/week2-your-task
```

Branches appear on GitHub **only after pushing**.

---

### 8️⃣ Open or update your Pull Request (PR)

* Go to GitHub
* Click **Compare & open pull request**
* In the description, include:

```
Closes #<issue-number>
```

Draft PRs are allowed.

---

## 🔴 IMPORTANT RULES

* Always pull from `main`
* Never pull from someone else’s branch
* Never push to `main`
* One issue → one branch → one PR
* Do NOT commit `.venv/`

---

## 🛑 OPTIONAL: Deactivate the virtual environment

When done running Python:

```bash
deactivate
```

---

