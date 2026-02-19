# 00 Start Here (Stroke Prevention Demo v1)

Welcome. This page is the single entry point for the whole project.

If you are new, do this in order:
1) Read “What we are building” below
2) Get write access (quick step, explained below)
3) Follow the workflow steps
4) Pick ONE GitHub issue and start

---

## What we are building (v1)

We are building a simple demo that:
- Takes health inputs (age, BP, smoking, etc.)
- Runs a risk scoring model
- Outputs a stroke risk score plus prevention tips

Final deliverable:
- Streamlit demo
- Short presentation

This is educational, not medical advice.

---

## Before you start: get write access (so you can push and open PRs)

If you cannot push code or open a PR, you probably do not have write access yet.

To get access:
1) Message the Project Team GC (Slack or Teams) with:
   - Your GitHub username
2) A lane lead will add you as a collaborator

Example message:
- “I'd like to contribute to the project, my GitHub username is: ________”

Once you have access, you can create branches and open pull requests normally.

---

## Where communication happens

We use two spaces for different purposes:

### Slack GC (general project members)
Use Slack for:
- announcements
- meeting reminders
- quick questions that anyone can answer
- links and updates that the whole project should see

### Teams GC (active contributors only, you get access to this GC after coming to a meeting)
Use the Team GC for:
- getting write access (send your GitHub username here)
- fast help when you are blocked during work time
- coordinating lane work in real time
- tagging leads when you need a quick decision

Simple rule:
If you are actively working tickets, use the Teams GC.

---

## Where everything lives

### 1) Weekly recaps (what happened each meeting)
Folder: `docs/recaps/`  
What it contains:
- One file per meeting week
- What got done, what is blocked, what is next

Start here if you missed a meeting.

Example links:
- [Recaps folder](./recaps/)
- [Latest recap](./recaps/week-04.md)

---

### 2) Workflow and how to contribute (how we work every time)
Folder: `docs/workflow/`  
What it contains:
- How to sync with main, make a branch, and open a PR
- Dev setup notes
- Notebook rules and collaboration rules

Links:
- [Workflow overview](./workflow/workflow.md)
- [Dev notes](./workflow/dev-notes.md)
- [Ticket collaboration rules](./workflow/ticket-collab.md)
- [Notebook rules](./workflow/notebook-rules.md)

---

### 3) Project docs (what the project is, decisions, scope)
Folder: `docs/project/`  
What it contains:
- Project state and current status
- Scope and deliverables
- Decisions made so we do not re debate the same stuff
- Dataset summary and provenance

Links:
- [Project state (always current)](./project/project_state.md)
- [Scope and deliverables](./project/scope.md)
- [Decisions log](./project/decisions.md)
- [Dataset summary](./project/dataset.md)

---

### 4) Data docs (what the dataset columns mean and what is safe to use)
Folder: `docs/data/`  
What it contains:
- Data dictionary
- Leakage candidates (columns we should not use as model inputs)
- Preprocessing notes

Links:
- [Data dictionary](./data/data_dictionary.md)
- [Leakage candidates](./data/leakage_candidates.md)
- [Preprocessing notes](./data/preprocessing_notes.md)

---

### 5) Content docs (the words the Streamlit app will show to users)
Folder: `docs/content/`  
What it contains:
- Recommended Next Steps mapping (risk factor to tips)
- Risk level labels (low, medium, high)
- Disclaimers and limitations
- FAQ and learn more text

Links:
- [Recommended Next Steps](./content/recommended_next_steps.md)
- [Risk level labels](./content/risk_level_labels.md)
- [Disclaimer and limitations](./content/disclaimer_and_limitations.md)
- [FAQ](./content/faq.md)

Rule:
If the user will read it in the app, it belongs in `docs/content/`.

---

## How to start working

1) Go to the GitHub Issues tab
2) Pick ONE issue
3) Comment “Claiming this” so people do not duplicate work
4) Make a branch (do not work on main)
5) Open a PR when you are done

If you get stuck for 5 minutes:
- Post the error in the issue comments
- Tag your lane lead in the Project Team GC

---

## Lanes and who to ask

We work in 3 lanes:
- Data + Pipeline: loading, preprocessing, training, metrics
- Docs + Content: data dictionary, leakage notes, app text content
- App: Streamlit pages and wiring outputs

Ask your lane lead first. If it blocks multiple lanes, tag the Project Manager.

---

## If you were not here last meeting

Do these two things:
1) Read the latest recap: [Latest recap](./recaps/week-04.md)
2) Check the project state: [Project state](./project/project_state.md)