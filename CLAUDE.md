# CLAUDE.md — APAC Claude Code Workshop (Accenture)

This file provides context and guidance for Claude Code when working within this repository.

## Repository Purpose

This repo is the student workshop package for the APAC Claude Code Workshop (Accenture cohort). It contains workshop materials, guides, slides, code snippets, and the mini-hackathon brief and submissions.

## Directory Structure

```
apac-cc-workshop-acn/
├── agenda/          # Workshop schedule files
├── faq/             # Frequently asked questions and troubleshooting
├── guides/          # Student setup and walkthrough guides
├── hackathon/       # Mini-hackathon materials
│   ├── README.md    # Hackathon agenda + submission instructions
│   └── submissions/ # Team submission folders (one folder per team)
│       └── team1_hackathon-name/   # Example: each team creates their own
│           ├── README.md
│           ├── CLAUDE.md
│           └── submission.html
├── slides/          # Presentation decks
├── snippets/        # Code snippets and reference implementations
├── CLAUDE.md        # This file
└── README.md        # Repo overview
```

## Key Conventions

- **Hackathon submissions** live under `hackathon/submissions/` and follow the naming convention `teamN_hackathon-name` (e.g. `team1_claude-inventory`, `team2_smart-search`).
- Each team submission folder must contain: `README.md`, `CLAUDE.md`, and `submission.html`.
- Do not modify files inside `hackathon/submissions/` unless you are the submitting team.
- All workshop content files use Markdown (`.md`) unless otherwise specified.

## Working with Student Code

When helping students during the workshop:

- Encourage use of Claude Code's `/init` command to generate a `CLAUDE.md` in their project.
- Reference `snippets/` for approved code patterns.
- Direct questions to `faq/` before troubleshooting from scratch.

## Facilitation Notes

- The starter app for the workshop is [beck-source/inventory-management](https://github.com/beck-source/inventory-management).
- Students should fork the starter app to their own GitHub account before the session.
- API keys are sourced from [console.anthropic.com](https://console.anthropic.com).
