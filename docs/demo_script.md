# Demo Script

Use this script to walk through the agent end-to-end during a live demo or recorded submission.

---

## Setup (2 min)

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Confirm environment variables are set
cat .env | grep OPENAI_API_KEY

# 3. Confirm dependencies are installed
pip list | findstr langgraph
```

---

## Step 1: Verify the Knowledge Base (2 min)

Open `notebooks/rag_experimentation.ipynb` and run all cells.

**Show**: Retrieval results for "refund request" — confirm `refund_policy.md` is returned as a top-3 result.

**Talking point**: "The agent can only quote what's in the knowledge base. If nothing is found, it escalates — it never makes up a policy."

---

## Step 2: Run the Full Agent Graph (5 min)

```bash
python src/main.py
```

**Demonstrate each ticket path**:

| Ticket | Expected Route | HITL | Talking Point |
|--------|---------------|------|---------------|
| TCK-1001 | AUTO_RESOLVE | Queued | Below auto-approve threshold — held for human review |
| TCK-1005 | REFUSE | N/A | Abusive content — scripted refusal, bypasses HITL gate |
| TCK-1006 | ESCALATE | Queued | Repeated refund within 90 days — rule-based escalation |
| TCK-1008 | AUTO_RESOLVE | Queued | Confidence below 0.95 — held for human review |

At the end of the run the terminal prints:

```
7 ticket(s) queued for HITL review: TCK-1001, TCK-1002, ...
Run:  python src/reviewer.py
```

**Talking point**: "Tickets that complete (REFUSE) write audit logs immediately. All others are paused — the graph checkpoint is persisted in `outputs/hitl_checkpoints.db` until a reviewer responds."

---

## Step 3: Show HITL Gate (3 min)

```bash
python src/reviewer.py
```

The reviewer script reads `outputs/hitl_queue/*.json` and displays each pending ticket:

```
============================================================
TICKET: TCK-1001
ROUTE:  AUTO_RESOLVE  (confidence: 0.71)
SOURCES: refund_policy.md

DRAFT REPLY:
...
============================================================
Actions: [A]pprove  [R]eject  [G]enerate again  [E]scalate
Reviewer action: A
Comments (optional): Looks good
  TCK-1001: APPROVED — COMPLETE
```

**Talking point**: "After each decision the paused LangGraph thread resumes from the checkpoint — `save_draft → audit_log → END`. The final draft and audit entry are written only after human approval."

Show the queue file before and after:

```bash
cat outputs/hitl_queue/TCK-1001.json
```

## Step 4: Evaluation Report (2 min)

Open `notebooks/evaluation_analysis.ipynb` and run the route accuracy cell.

**Show**: 
- Route accuracy against `data/evaluation/expected_routes.json`
- Confidence distribution stats
- Groundedness score for a sample draft

---

## Step 5: Audit Log (1 min)

```bash
cat outputs/audit_logs/TCK-1001.json
```

**Talking point**: "Every ticket produces an immutable audit entry with the route decision, confidence score, sources used, and reviewer action — a complete record for compliance."

---

## Wrap-up (1 min)

Key safety guarantees demonstrated:
1. Replies are drafts — never auto-sent
2. Policies are KB-grounded — no hallucination
3. Abusive content is refused with a scripted template
4. Missing policy always escalates — never fabricated
