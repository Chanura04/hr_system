from typing import TypedDict

from langgraph.graph import StateGraph, END

from app.agents.classifier import IntentClassifier
from app.agents.router import AgentRouter


class GraphState(TypedDict):
    query: str
    intent: str
    confidence: float
    response: str
    context: dict
    history: list[str]


classifier = IntentClassifier()
router = AgentRouter()


def inject_context(state: GraphState):
    state["context"] = state.get("context", {})
    state["history"] = state.get("history", [])
    return state


def classify_node(state: GraphState):
    intent, confidence = classifier.classify(state["query"])

    state["intent"] = intent
    state["confidence"] = confidence

    return state


def route_node(state: GraphState):
    agent = router.get_agent(state["intent"])
    context = state.get("context", {})

    print(
        f"\nRouting {state['intent']} -> {agent.__class__.__name__}: "
        f"context_keys={list(context.keys())}, "
        f"short_term={context.get('short_term')}, "
        f"long_term_count={len(context.get('long_term', [])) if isinstance(context.get('long_term'), list) else 'n/a'}"
    )

    result = agent.handle(state["query"], context)

    state["response"] = result
    state["history"].append(f"User: {state['query']}")
    state["history"].append(f"Assistant: {result}")

    return state


def build_graph():
    workflow = StateGraph(GraphState)

    workflow.add_node("inject_context", inject_context)
    workflow.add_node("classify", classify_node)
    workflow.add_node("route", route_node)

    workflow.set_entry_point("inject_context")

    workflow.add_edge("inject_context", "classify")
    workflow.add_edge("classify", "route")
    workflow.add_edge("route", END)

    return workflow.compile()