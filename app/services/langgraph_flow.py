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


classifier = IntentClassifier()
router = AgentRouter()


def inject_context(state: GraphState):
    state["context"] = state.get("context", {})
    return state


def classify_node(state: GraphState):
    intent, confidence = classifier.classify(state["query"])

    state["intent"] = intent
    state["confidence"] = confidence

    return state


def route_node(state: GraphState):
    agent = router.get_agent(state["intent"])

    result = agent.handle(state["query"], state.get("context", {}))

    state["response"] = result

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