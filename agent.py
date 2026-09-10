import os
from typing import TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


# -----------------------------
# State
# -----------------------------

class AgentState(TypedDict):
    query: str
    category: str
    context: str
    response: str


# -----------------------------
# Node 1: Query Classification
# -----------------------------

def classify_query(state: AgentState):

    query = state["query"]

    prompt = f"""
    Classify the following customer query into one of these categories:

    - billing
    - technical
    - account
    - general

    Customer query:
    {query}

    Return only the category name.
    """

    result = llm.invoke([HumanMessage(content=prompt)])

    category = result.content.strip().lower()

    return {
        "category": category
    }


# -----------------------------
# Node 2: Information Retrieval
# -----------------------------

def retrieve_information(state: AgentState):

    category = state["category"]

    knowledge_base = {
        "billing":
            "Customers can ask about payments, invoices, refunds, and subscription charges.",

        "technical":
            "Technical support includes troubleshooting login issues, application errors, and system problems.",

        "account":
            "Account support includes password reset, profile updates, and account access.",

        "general":
            "General support covers product information and common customer questions."
    }

    context = knowledge_base.get(
        category,
        knowledge_base["general"]
    )

    return {
        "context": context
    }


# -----------------------------
# Node 3: Response Generation
# -----------------------------

def generate_response(state: AgentState):

    query = state["query"]
    context = state["context"]

    prompt = f"""
    You are a helpful customer support agent.

    Use the following information to answer the customer.

    Information:
    {context}

    Customer Query:
    {query}

    Give a clear, polite and concise response.
    """

    result = llm.invoke([HumanMessage(content=prompt)])

    return {
        "response": result.content
    }


# -----------------------------
# Node 4: Answer Validation
# -----------------------------

def validate_response(state: AgentState):

    response = state["response"]

    prompt = f"""
    Check whether this customer support response is clear,
    relevant and professional.

    Response:
    {response}

    If it is good, return it unchanged.
    Otherwise, rewrite it to make it clearer.
    """

    result = llm.invoke([HumanMessage(content=prompt)])

    return {
        "response": result.content
    }


# -----------------------------
# Build LangGraph
# -----------------------------

workflow = StateGraph(AgentState)

workflow.add_node(
    "classify",
    classify_query
)

workflow.add_node(
    "retrieve",
    retrieve_information
)

workflow.add_node(
    "generate",
    generate_response
)

workflow.add_node(
    "validate",
    validate_response
)


# Workflow edges

workflow.set_entry_point("classify")

workflow.add_edge(
    "classify",
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "generate"
)

workflow.add_edge(
    "generate",
    "validate"
)

workflow.add_edge(
    "validate",
    END
)


# Compile graph

customer_support_agent = workflow.compile()


# Function used by Streamlit

def run_agent(query: str):

    result = customer_support_agent.invoke({
        "query": query,
        "category": "",
        "context": "",
        "response": ""
    })

    return result