# Developer Notes 

These are notes should be read after being assigned to a Data & Pipeline Ticket. Once read and multiple participates want to work on the same ticket. This is the guide to how to start working on the same branch.

---

### Creating a notebook

To begin working on the same Data & Pipeline Ticket as your partner, first ONE individual needs go on their device and create a notebook in the notebooks folder. Follow the notebook-rules.md if not sure how!

**Examples**
- `week2_missing_values.ipynb`
- `week2_feature_types.ipynb`
- `week2_biomarkers.ipynb`
Don't worry about the netID, just write <week>_<Task>.ipynb

---

### Creating a Branch

After creating a notebook, the same individual then needs to create a feature branch with the task and week.

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

### Joining the newly Created Branch

On your teammates or whoever you are collaborating device, they need to then join the newly created branch.

```bash
git checkout feature/week2-your-task
```

Example:

```bash
git checkout feature/week2-missing-values
```
--- 

### Pushing your Branch
After creating the notebook

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

## ✅ DO 
- Use this command in bash!
```bash
git status
```
If it shows that you are on branch the right branch, you are good!

---

- If you are have someone else that joined the DP Ticket branch and pushed their work, use this command in bash!
```bash
git pull origin feature/<Branch>
```
Example:

```bash
git pull origin feature/week2_dp2
```
--- 

- Make sure your **venv** (Virtual Machine) is activated! if your terminal shows (.venv) you are good.

## Communication is key
if all the steps are meant, you are on your way to creating this project! If not message one of the exec members!