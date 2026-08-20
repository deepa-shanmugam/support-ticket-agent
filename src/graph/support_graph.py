"""
Builds and compiles the LangGraph support ticket agent graph.
"""
import os
import sqlite3
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

from graph.graph_state import GraphState
from graph.nodes import (
    sentiment_check_node,
    policy_check_node,
    rag_draft_node,
    route_decision_node,
    confidence_recheck_node,
    hitl_approval_node,
    refuse_node,
    save_draft_node,
    audit_log_node,
)
from graph.edges import (
    route_after_decision,
    route_after_confidence_recheck,
    route_after_hitl,
)

CHECKPOINT_DB = "./outputs/hitl_checkpoints.db"


def build_support_graph():
    graph = StateGraph(GraphState)

    graph.add_node("sentiment_check", sentiment_check_node)
    graph.add_node("policy_check", policy_check_node)
    graph.add_node("rag_draft", rag_draft_node)
    graph.add_node("route_decision", route_decision_node)
    graph.add_node("confidence_recheck", confidence_recheck_node)
    graph.add_node("hitl_approval", hitl_approval_node)
    graph.add_node("refuse", refuse_node)
    graph.add_node("save_draft", save_draft_node)
    graph.add_node("audit_log", audit_log_node)

    graph.set_entry_point("sentiment_check")
    graph.add_edge("sentiment_check", "policy_check")
    graph.add_edge("policy_check", "rag_draft")
    graph.add_edge("rag_draft", "route_decision")

    graph.add_conditional_edges(
        "route_decision",
        route_after_decision,
        {
            "refuse": "refuse",
            "hitl_approval": "hitl_approval",
            "confidence_recheck_or_hitl": "confidence_recheck",
        },
    )

    graph.add_conditional_edges(
        "confidence_recheck",
        route_after_confidence_recheck,
        {
            "hitl_approval": "hitl_approval",
            "confidence_recheck": "confidence_recheck",
        },
    )

    graph.add_conditional_edges(
        "hitl_approval",
        route_after_hitl,
        {
            "save_draft": "save_draft",
            "rag_draft": "rag_draft",
            "refuse": "refuse",
        },
    )

    graph.add_edge("refuse", "save_draft")
    graph.add_edge("save_draft", "audit_log")
    graph.add_edge("audit_log", END)

    import sqlite3
    os.makedirs(os.path.dirname(CHECKPOINT_DB), exist_ok=True)
    conn = sqlite3.connect(CHECKPOINT_DB, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    return graph.compile(checkpointer=checkpointer)
