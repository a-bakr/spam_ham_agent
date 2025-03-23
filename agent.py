from langchain_core.messages import HumanMessage
from typing import TypedDict, Dict, List, Any, Optional
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv


load_dotenv('.env')

# Initialize LLM
# model_id = "gpt-4o-mini"
# model = ChatOpenAI(model=model_id, temperature=0)
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0)

class EmailState(TypedDict):
    email: Dict[str, Any]
    is_spam: Optional[bool]
    draft_response: Optional[str]
    messages: List[Dict[str, Any]]

# Define nodes
def read_email(state: EmailState):
    email = state["email"]
    print(f"Alfred is processing an email from {email['sender']} with subject: {email['subject']}")
    return {}

def classify_email(state: EmailState):
    email = state["email"]
    
    prompt = f"""
As Alfred the butler of Mr wayne and it's SECRET identity Batman, analyze this email and determine if it is spam or legitimate and should be brought to Mr wayne's attention.

Email:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}

First, determine if this email is spam.
answer with SPAM or HAM if it's legitimate. Only reurn the answer
Answer :
    """
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    
    response_text = response.content.lower()
    print(response_text)
    is_spam = "spam" in response_text and "ham" not in response_text
    
    if not is_spam:
        new_messages = state.get("messages", []) + [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response.content}
        ]
    else :
        new_messages = state.get("messages", [])
    
    return {
        "is_spam": is_spam,
        "messages": new_messages
    }

def handle_spam(state: EmailState):
    print(f"Alfred has marked the email as spam.")
    print("The email has been moved to the spam folder.")
    return {}

def drafting_response(state: EmailState):
    email = state["email"]
    
    prompt = f"""
As Alfred the butler, draft a polite preliminary response to this email.

Email:
From: {email['sender']}
Subject: {email['subject']}
Body: {email['body']}

Draft a brief, professional response that Mr. Wayne can review and personalize before sending.
    """
    
    messages = [HumanMessage(content=prompt)]
    response = model.invoke(messages)
    
    new_messages = state.get("messages", []) + [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response.content}
    ]
    
    return {
        "draft_response": response.content,
        "messages": new_messages
    }

def notify_mr_wayne(state: EmailState):
    email = state["email"]
    
    print("\n" + "="*50)
    print(f"Sir, you've received an email from {email['sender']}.")
    print(f"Subject: {email['subject']}")
    print("\nI've prepared a draft response for your review:")
    print("-"*50)
    print(state["draft_response"])
    print("="*50 + "\n")
    
    return {}

# Define routing logic
def route_email(state: EmailState) -> str:
    if state["is_spam"]:
        return "spam"
    else:
        return "legitimate"

def create_graph():
    # Create the graph
    email_graph = StateGraph(EmailState)

    # Add nodes
    email_graph.add_node("read_email", read_email) 
    email_graph.add_node("classify_email", classify_email) 
    email_graph.add_node("handle_spam", handle_spam) 
    email_graph.add_node("drafting_response", drafting_response) 
    email_graph.add_node("notify_mr_wayne", notify_mr_wayne) 


    # Add edges
    email_graph.add_edge(START, "read_email") 
    email_graph.add_edge("read_email", "classify_email") 
    email_graph.add_conditional_edges(
        "classify_email", 
        route_email,
        {
            "spam": "handle_spam",
            "legitimate": "drafting_response" 
        }
    )
    # Add final edges
    email_graph.add_edge("handle_spam", END) 
    email_graph.add_edge("drafting_response", "notify_mr_wayne")
    email_graph.add_edge("notify_mr_wayne", END) 

    return email_graph.compile()


def run_agent(legitimate_email: str) -> str:

    # Process legitimate email
    print("\nProcessing legitimate email...")

    agent = create_graph()

    res = agent.invoke({
        "email": legitimate_email,
        "is_spam": None,
        "draft_response": None,
        "messages": []
    })

    print(res)
    return res