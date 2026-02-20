# Collaboration Rules (When Multiple People Work Together)

This explains how to collaborate without overwriting each other.

---

## Default rule

One ticket equals one person equals one branch equals one PR.

Only share a branch if:

- A lane lead says you are pairing, or
- The GitHub issue explicitly says "pair work"

---

## Branch naming (required)

Branch format:

```text
feature/<ticket-id>-short-name
```

Examples:

- feature/DP1-baseline-model
- feature/DC1-data-dictionary
- feature/APP2-example-mode

---

## If you are pairing on the same ticket (shared branch)

Use this process.

### Step 1) Decide who is the branch owner

One person is the branch owner.
The branch owner creates the branch and pushes it.

Example:

```bash
git checkout -b feature/DP1-baseline-model
git push origin feature/DP1-baseline-model
```

---

### Step 2) Partner joins the branch

Partner runs:

```bash
git checkout main
git pull origin main
git checkout feature/<ticket-id>-short-name
git pull origin feature/<ticket-id>-short-name
```

Example:

```bash
git checkout feature/DP1-baseline-model
git pull origin feature/DP1-baseline-model
```

---

### Step 3) Avoid conflicts (simple rules)

- Do not edit the same lines at the same time
- If you are both working in notebooks, use separate notebooks (see notebook guidelines)
- For docs, decide who edits which section before typing

---

### Step 4) Keep the branch updated

Before pushing, always pull first:

```bash
git pull origin feature/<ticket-id>-short-name
```

Then commit and push:

```bash
git status
git add .
git commit -m "<ticket-id>: short description"
git push origin feature/<ticket-id>-short-name
```

Example:

```bash
git commit -m "DP1: baseline logistic regression + metrics"
git push origin feature/DP1-baseline-model
```

---

## If you get a merge conflict

Do not panic.

1. Stop
2. Copy paste the conflict text into the GitHub issue comments
3. Tag your lane lead in the Project Team GC

---

## Communication rule

If you are stuck for more than 5 minutes:

- Comment the blocker on the GitHub issue
- Tag your lane lead

