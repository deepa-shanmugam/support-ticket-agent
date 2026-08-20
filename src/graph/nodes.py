"""
LangGraph node functions for the support ticket agent.
"""
from agents.sentiment_agent import SentimentAgent
from agents.rag_agent import RAGAgent
from agents.triage_agent import TriageAgent
from agents.response_agent import ResponseAgent
from safety.abuse_detection import AbuseDetector
from safety.policy_checker import PolicyChecker
from hitl.approval_queue import ApprovalQueue
from app_logging.audit_logger import AuditLogger

sentiment_agent = SentimentAgent()
rag_agent = RAGAgent()
triage_agent = TriageAgent()
response_agent = ResponseAgent()
abuse_detector = AbuseDetector()
policy_checker = PolicyChecker()
approval_queue = ApprovalQueue()
audit_logger = AuditLogger()


def sentiment_check_node(state: dict) -> dict:
    sentiment = sentiment_agent.analyze(state["ticket"]["message"])
    return {**state, "sentiment": sentiment}


def policy_check_node(state: dict) -> dict:
    sources, found = policy_checker.check(state["ticket"])
    return {**state, "retrieved_sources": sources, "policy_found": found}


def rag_draft_node(state: dict) -> dict:
    draft, confidence = rag_agent.draft_reply(state["ticket"], state["retrieved_sources"])
    return {**state, "draft_reply": draft, "confidence_score": confidence}


def route_decision_node(state: dict) -> dict:
    route = triage_agent.decide(
        sentiment=state["sentiment"],
        policy_found=state["policy_found"],
        confidence=state["confidence_score"],
        ticket=state["ticket"],
    )
    return {**state, "route_decision": route}


def confidence_recheck_node(state: dict) -> dict:
    retry_count = state.get("retry_count", 0) + 1
    draft, confidence = rag_agent.draft_reply(
        state["ticket"], state["retrieved_sources"], retry=retry_count
    )
    return {**state, "draft_reply": draft, "confidence_score": confidence, "retry_count": retry_count}


def hitl_approval_node(state: dict) -> dict:
    result = approval_queue.submit(state)
    return {**state, "reviewer_action": result.get("reviewer_action"), "reviewer_comments": result.get("reviewer_comments")}


def refuse_node(state: dict) -> dict:
    from safety.refusal_templates import get_refusal_message
    draft = get_refusal_message(state["sentiment"])
    return {**state, "draft_reply": draft, "route_decision": "REFUSE"}


def save_draft_node(state: dict) -> dict:
    response_agent.format_draft(
        ticket=state["ticket"],
        draft=state.get("draft_reply", ""),
        route=state.get("route_decision", ""),
        confidence=state.get("confidence_score", 0.0),
        sources=state.get("retrieved_sources", []),
    )
    return state


def audit_log_node(state: dict) -> dict:
    audit_logger.log(state["ticket"]["ticket_id"], state)
    return state
