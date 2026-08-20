# Support Ticket Triage & Resolution Agent

An AI-powered support ticket triage and resolution agent built with LangGraph, RAG, and HITL approval.

## Overview

This agent processes customer support tickets using a synthetic ticket queue and a policy/FAQ knowledge base. For each ticket it decides one of four actions:

- **Auto-Resolve** — draft a response from the knowledge base
- **Escalate** — route to a human support specialist
- **Refuse** — politely decline abusive or out-of-scope requests
- **Ask for More Information** — request clarification from the customer

All drafted replies go through a human approval gate and are never sent automatically.

## Agent Flow

```
Ticket In
    ↓
Sentiment & Policy Check
    ↓
RAG Answer Draft
    ↓
LangGraph Route Decision
    ↓
Confidence Re-check Loop
    ↓
HITL Approval
    ↓
Audit Log
```

## Setup

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd support-ticket-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the agent

```bash
# Phase 1 — process all tickets
python src/main.py
```

Tickets with confidence ≥ 0.95 are auto-approved. All others are paused and written to `outputs/hitl_queue/`. A message is printed listing the queued tickets:

```
7 ticket(s) queued for HITL review: TCK-1001, TCK-1002, ...
Run:  python src/reviewer.py
```

```bash
# Phase 2 — review queued tickets
python src/reviewer.py
```

For each pending ticket the reviewer is shown the draft reply and prompted:

```
Actions: [A]pprove  [R]eject  [G]enerate again  [E]scalate
```

After each decision the paused graph thread resumes and completes (`save_draft → audit_log → END`). Outputs appear in `outputs/drafted_replies/` and `outputs/audit_logs/`.

## Project Structure

```
support-ticket-agent/
├── config/          # App, model, and routing configuration
├── data/            # Tickets, knowledge base, evaluation data
├── src/             # Source code
│   ├── graph/       # LangGraph nodes, edges, and state
│   ├── agents/      # Triage, RAG, policy, sentiment, response agents
│   ├── retrieval/   # Document loading, vector store, retrieval
│   ├── memory/      # Conversation and customer thread memory
│   ├── hitl/        # Human-in-the-loop approval gate + reviewer script
│   ├── safety/      # Policy checking, refusals, abuse detection
│   ├── evaluation/  # Arize and custom evaluators
│   ├── logging/     # Audit and trace logging
│   └── utils/       # Schemas, constants, helpers
├── notebooks/       # Experimentation notebooks
├── tests/           # Unit and integration tests
├── outputs/         # Generated replies, audit logs, reports
└── docs/            # Architecture, guides, rubric, demo script
```

## Safety Principles

- Replies are drafts only — never auto-sent
- Policies quoted only from the knowledge base
- If no policy is found, the agent escalates rather than fabricating
- Abusive content is refused with a polite scripted response

## Running Tests

```bash
pytest tests/
```
