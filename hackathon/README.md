# Mini-Hackathon — APAC Claude Code Workshop

Welcome to the Mini-Hackathon session! This document covers the full-day agenda, hackathon brief, and submission instructions.

---

## Workshop Agenda

> All times listed in SGT (Singapore Time) and AEDT (Australian Eastern Daylight Time).

| SGT | AEDT | Duration | Activity | Description / Notes | Facilitator |
|-----|------|----------|----------|---------------------|-------------|
| 08:00 – 08:30 | | 30 mins | Early Setup | We can arrive by 8am | |
| 08:30 – 09:00 | 11:30 – 12:00 | 30 mins | Set-up / Final Preparation | Final tech check, participant arrival | Event Team |
| 09:00 – 09:15 | 12:00 – 12:15 | 15 mins | Senior Leaders Kickoff | Welcome remarks and workshop objectives | Yu Yi, Ruchi |
| 09:15 – 10:00 | 12:15 – 13:00 | 45 mins | Anthropic Overview *(Content + How to Deliver)* | Overview of Anthropic and guidance on delivering the session | Janak Sevak |
| 10:00 – 10:30 | 13:00 – 14:00 | 30 mins | Art of the Possible Show & Tell *(Content + How to Deliver)* | Demo of Claude capabilities and storytelling approach | Janak Sevak |
| 11:00 – 11:15 | 14:00 – 14:15 | 15 mins | Morning Break | Coffee break | |
| 11:15 – 12:15 | 14:15 – 15:15 | 75 mins | Claude Code Workshop | Claude Code workshop — Part 1 | Riebeeck V. |
| 12:15 – 13:15 | 15:15 – 16:15 | 60 mins | Lunch | Lunch break and networking | |
| 13:15 – 13:45 | 16:15 – 16:45 | 30 mins | Claude Code Workshop *(Wrapup + How to Facilitate)* | Claude Code workshop — Part 2 | Riebeeck V. |
| 13:45 – 14:15 | 16:45 – 17:15 | 45 mins | How to Facilitate Hackathon / Start Mini-Hackathon | Guidance on running the hackathon session | Caroline M. |
| 14:15 – 14:45 | 17:15 – 17:45 | 15 mins | Afternoon Break | Afternoon refreshment break | |
| 14:45 – 15:45 | 17:45 – 18:45 | 60 mins | Mini-Hackathon | Participants work on challenge tasks | Caroline M. |
| 15:45 – 16:00 | 18:45 – 19:00 | 15 mins | Mini-Hackathon Judging | Review and scoring of submissions | Caroline M. |
| 16:00 – 16:15 | 19:00 – 19:15 | 15 mins | Closing & Discussion | Key takeaways, reflections, and open discussion | All Facilitators |
| 16:15 – 17:00 | 19:15 – 20:00 | | Post-event / Networking | Optional informal networking | |

---

## Mini-Hackathon Brief

**Duration:** 60 minutes (14:45 – 15:45 SGT)

**Objective:** Use Claude Code to build a meaningful improvement or new feature on top of the [inventory-management](https://github.com/beck-source/inventory-management) starter app (or your own project, if agreed with your facilitator).

**Teams:** You will be assigned to a team at the start of the session. Teams are typically 2–4 participants.

**Challenge:** Your team must use Claude Code to:
1. Identify a problem or opportunity in the starter app
2. Implement a solution using Claude Code as your primary coding assistant
3. Document what you built and how Claude Code helped

**Judging Criteria:**

| Criterion | Weighting |
|-----------|-----------|
| Use of Claude Code | 30% |
| Innovation / Creativity | 25% |
| Functionality | 25% |
| Presentation quality | 20% |

---

## Submission Instructions

Each team must submit their work by **uploading a folder** to `hackathon/submissions/` in this repository.

### Folder Naming Convention

```
submissions/
└── teamN_hackathon-name/
```

Replace `N` with your team number and `hackathon-name` with a short slug describing your submission.

**Examples:**
```
team1_smart-reorder
team2_claude-inventory-audit
team3_low-stock-alerts
```

### Required Files

Every submission folder **must** contain exactly these three files:

```
teamN_hackathon-name/
├── README.md          # Project overview and demo notes
├── CLAUDE.md          # Claude Code context for your project
└── submission.html    # Presentation slide (HTML format)
```

---

### `README.md` — What to Include

Your `README.md` should cover:

```markdown
# Team N — [Hackathon Name]

## Team Members
- Name, Role

## Problem Statement
What problem did you tackle and why?

## Solution Overview
What did you build? How does it work?

## How We Used Claude Code
Describe the specific Claude Code features and commands you used.

## Demo
Link to a short demo video or screenshots (optional but encouraged).

## Lessons Learned
What worked well? What would you do differently?
```

---

### `CLAUDE.md` — What to Include

Your `CLAUDE.md` gives Claude Code context about your submission project. Use it to describe:

- The purpose of your project
- Key files and their roles
- Any conventions or patterns Claude should follow
- Commands to build/run/test the project

You can generate a starter `CLAUDE.md` by running `/init` in your project directory with Claude Code.

---

### `submission.html` — Presentation Slide

Your `submission.html` is a **single self-contained HTML file** that acts as a presentation slide. It will be displayed during the judging session.

**Requirements:**
- Single HTML file (inline all CSS and JS — no external dependencies)
- Renders correctly when opened directly in a browser
- Covers: team name, problem, solution, key Claude Code moments, outcome
- Keep it visual — use a clear layout, not a wall of text

**Minimal template to get started:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Team N — Hackathon Submission</title>
  <style>
    body { font-family: sans-serif; background: #0f0f0f; color: #f0f0f0; margin: 0; padding: 2rem; }
    h1 { color: #e8912d; }
    h2 { color: #a78bfa; margin-top: 2rem; }
    ul { line-height: 1.8; }
    .tag { background: #1e1e2e; border: 1px solid #a78bfa; border-radius: 4px; padding: 2px 8px; font-size: 0.85rem; margin-right: 4px; }
  </style>
</head>
<body>
  <h1>Team N — Your Hackathon Name</h1>
  <p><strong>Team Members:</strong> Name 1, Name 2</p>

  <h2>Problem</h2>
  <p>Describe the problem you solved.</p>

  <h2>Solution</h2>
  <p>Describe what you built.</p>

  <h2>How We Used Claude Code</h2>
  <ul>
    <li>Used <code>/init</code> to scaffold the project</li>
    <li>Used Claude Code to generate unit tests</li>
    <li>...</li>
  </ul>

  <h2>Outcome</h2>
  <p>What was the result? What would you do next?</p>
</body>
</html>
```

---

## Submitting via GitHub

1. Fork or clone this repository
2. Create your folder under `hackathon/submissions/teamN_your-name/`
3. Add your three files (`README.md`, `CLAUDE.md`, `submission.html`)
4. Open a Pull Request to this repository with the title: `Submission: Team N — Your Hackathon Name`
5. A facilitator will merge your PR before judging begins

> **Deadline:** All PRs must be open before the judging session starts at **15:45 SGT**.

---

## Questions?

Speak to your facilitator or raise a hand during the session. Good luck!
