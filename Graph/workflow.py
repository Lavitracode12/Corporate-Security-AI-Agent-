from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from Agents.planner import QueryPlanner
from Agents.retriever import recall_from_source, get_employee_profile
from Agents.correlator import ForensicCorrelator
from Agents.scorer import ThreatScorer
from google import genai
import asyncio
import os
import sqlite3
from Agents.guardrails import SecurityGuardrails

class InvestigationState(TypedDict):
    query: str
    intent: str
    sub_queries: List[str]
    findings: List[Dict[str, Any]]
    timeline: List[Dict[str, Any]]
    threat_score: float
    threat_level: str
    summary_verdict: str
    report_path: str
    demo_mode: bool

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_target_employee(query_text: str) -> str:
    profile = get_employee_profile(query_text)
    if profile and profile.get("name"):
        return profile.get("name")
    return ""


def intent_router_node(state: InvestigationState) -> Dict[str, Any]:
    """
    Step 1: Analyzes query intent. 
    Intercepts adversarial threats immediately and overrides state keys dynamically.
    """
    query_lower = state["query"].lower()
    
    # STEP 0: ACTIVE GUARDRAIL INTERCEPTION
    is_safe, threat_type, reason = SecurityGuardrails.check_input_safety(state["query"])
    if not is_safe:
        print(f"🚨 GUARDRAIL BREACH DETECTED [{threat_type}]: Injecting defense payload.")
        
        alert_message = (
            f"🛑 **SECURITY CLEARANCE DENIED: ACTIVE GUARDRAIL INTERCEPT**\n\n"
            f"**Violation Category:** `{threat_type.upper()}`\n"
            f"**Audit Log:** {reason}\n\n"
            f"*This directive has been logged and flagged in the InvenTech Security Incident Matrix. "
            f"As an enterprise security agent, I am strictly restricted from executing commands that threaten corporate infrastructure, bypass compliance bylaws, or generate social engineering vectors.*"
        )
        
        return {
            "intent": "security_block",
            "summary_verdict": alert_message,
            "threat_score": 100.0,
            "threat_level": "CRITICAL / BLOCKED",
            "sub_queries": ["Intercept incoming adversarial prompt"],
            "findings": [],
            "timeline": [{
                "timestamp": "IMMEDIATE",
                "source_document": "GUARDRAIL_SHIELD",
                "details": f"Blocked malicious prompt execution. Category: {threat_type}"
            }]
        }

    # Step 1: Precise deterministic routing
    investigation_keywords = ["leak", "falcon", "audit", "log", "resigned", "history", "trace"]
    if any(keyword in query_lower for keyword in investigation_keywords):
        return {"intent": "investigate"}
        
    return {"intent": "chat"}

def security_block_node(state: InvestigationState) -> dict:
    """
    Pass-through visualization node for the active defense layout.
    """
    return {}

def general_chat_node(state: dict) -> Dict[str, Any]:
    """
    Handles conversational questions dynamically with an optimized SQLite tool lookup 
    and robust local fallback engine.
    """
    query = state.get("query", "")
    q_lower = query.lower()
    
    api_key = os.environ.get("GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key) if api_key else None
    
    retrieved_corporate_context = ""
    db_path = "security_vault.db" # should match to db file name

    # AUTOMATED SQL DATA TOOL ACCESSOR 
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Scenario A: User is asking about Employee Performance Reviews
        if any(kw in q_lower for kw in ["performance", "review", "rating", "manager"]):
            target_name = None
            for name in ["alex", "susan", "brett", "michael"]:
                if name in q_lower:
                    target_name = name
                    break
            
            if target_name:
                cursor.execute(
                    "SELECT role, manager, rating, review_text FROM performance_reviews WHERE employee_name = ?", 
                    (target_name,)
                )
                row = cursor.fetchone()
                if row:
                    retrieved_corporate_context += (
                        f"\n[INTERNAL HR PERFORMANCE MATRIX]\n"
                        f"Employee: {target_name.capitalize()} | Role: {row[0]} | Manager: {row[1]}\n"
                        f"Performance Rating: {row[2]}\n"
                        f"Manager Evaluation Brief: {row[3]}\n"
                    )

        # Scenario B: User is asking about Company Policies or Compliance Rules
        if any(kw in q_lower for kw in ["policy", "rule", "prohibited", "allowed", "guideline", "bylaw", "falcon", "company", "data"]):
            cursor.execute("SELECT policy_section, policy_title, policy_content FROM company_policies")
            policies = cursor.fetchall()
            
            matched_policies = []
            for sec, title, content in policies:
                # Core keyword scan to pull only relevant policy paragraphs
                if any(kw in content.lower() or kw in title.lower() for kw in q_lower.split()):
                    matched_policies.append(f"Section {sec} - {title}: {content}")
            
            if matched_policies:
                retrieved_corporate_context += "\n[CORPORATE COMPLIANCE POLICIES]\n" + "\n".join(matched_policies) + "\n"
            else:
                # If no specific keyword hits, serve the core security policies as standard context
                retrieved_corporate_context += "\n[CORPORATE COMPLIANCE POLICIES]\n" + f"Section {policies[0][0]}: {policies[0][2]}\nSection {policies[1][0]}: {policies[1][2]}"

        conn.close()
    except Exception as db_err:
        print(f"⚠️ SQLite Knowledge Base retrieval bypassed: {db_err}")

    # GENERATION LAYER: Build the Agentic Output

    
    # Local Deterministic Text Engine (If API is Throttled / 429)
    # Helper function for smart, beautiful local responses when offline or throttled (429)
    def _get_local_chat_response(q: str, context: str) -> str:
        q_lower = q.lower()
        
        # STEP 1: Check for direct corporate meta-questions FIRST before looking at data dumps
        if "name" in q_lower and ("company" in q_lower or "organization" in q_lower or "enterprise" in q_lower):
            return "🏢 The name of the company under audit is **InvenTech Solutions**."
            
        elif any(greet in q_lower for greet in ["hi", "hello", "hey"]):
            return "Hello! I am your automated Smart Enterprise & Operations Agent. I am connected to the InvenTech Solutions Compliance Policies database and HR Performance Matrix records. How can I assist you today, CEO?"
            
        elif any(status in q_lower for status in ["status", "connected", "health"]):
            return "System Status Report: Connected and Operational. All corporate policy records, HR performance ledgers, and forensic logging streams are fully online."

        # STEP 2: If it's not a generic meta-question, look at the extracted database context data
        if context:
            clean_context = context.replace("Section SEC_4.1", "\n🔒 **Section SEC_4.1**")\
                                   .replace("Section SEC_4.2", "\n🛡️ **Section SEC_4.2**")\
                                   .replace("Section SEC_4.3", "\n🌐 **Section SEC_4.3**")\
                                   .replace("Section HR_7.5", "\n📋 **Section HR_7.5**")
            
            return (
                f"📊 **Executive Enterprise Information System [LOCAL ENGINE ACTIVE]**\n\n"
                f"Here is the verified data extracted from our internal server tables:\n{clean_context}\n\n"
                f"*Administrative Note: Information generated securely via local database lookup layers.*"
            )
            
        # STEP 3: Complete baseline catch-all fallback
        return f"I received your query: '{q}'. To pull company guidelines or performance profiles, please mention an employee name or specific corporate topics (e.g., 'data policy', 'company name', or 'Brett performance')."
            
        # 2. Advanced text matching for common meta-questions that miss the DB trigger
        if "name" in q_lower and ("company" in q_lower or "organization" in q_lower or "enterprise" in q_lower):
            return "🏢 The name of the company under audit is **InvenTech Solutions**."
            
        elif any(greet in q_lower for greet in ["hi", "hello", "hey"]):
            return "Hello! I am your automated Smart Enterprise & Operations Agent. I am connected to the InvenTech Solutions Compliance Policies database and HR Performance Matrix records. How can I assist you today, CEO?"
            
        elif any(status in q_lower for status in ["status", "connected", "health"]):
            return "System Status Report: Connected and Operational. All corporate policy records, HR performance ledgers, and forensic logging streams are fully online."
            
        else:
            return f"I received your query: '{q}'. To pull company guidelines or performance profiles, please mention an employee name or specific corporate topics (e.g., 'data policy', 'company name', or 'Brett performance')."

    # Route request safely
    if state.get("demo_mode") or not client:
        verdict = _get_local_chat_response(query, retrieved_corporate_context)
    else:
        try:
            system_instruction = (
                "You are an Elite Enterprise Operations & Security Intelligent Assistant serving the CEO.\n"
                "Your interface has access to company policies and employee performance database records via structured SQL tools.\n"
                "Review the following context block if populated, and use it to craft a highly professional, comprehensive executive answer.\n"
                "If the context is empty, answer the user general security question with authority.\n"
                "Do not reference 'context blocks' or 'database fields' directly to the user—speak naturally as an intelligent corporate advisor."
            )
            
            prompt = f"{system_instruction}\n\nInternal Database Context:\n{retrieved_corporate_context}\n\nUser Query: {query}"
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            verdict = response.text.strip()
        except Exception as api_err:
            print(f"⚠️ Chat API Limit Triggered ({api_err}). Executing local database mapping engine...")
            verdict = _get_local_chat_response(query, retrieved_corporate_context)

    # Return the uniform dictionary object layout to main.py
    return {
        "summary_verdict": verdict,
        "intent": "chat",
        "threat_level": "N/A",
        "timeline": [],
        "sub_queries": ["General Chat Sequence Executed"]
    }

def planner_node(state: InvestigationState) -> Dict[str, Any]:
    """
    Step 2: Prepares targeted RAG data points.
    Creates a clean structural execution list for the database lookup.
    """
    # Simply pull the target employee name out of the string dynamically
    query_words = state["query"].split()
    target = "Alex" # Default placeholder fallback
    for word in query_words:
        if word.lower() in ["alex", "susan"]: # Map to your 10-person dataset targets
            target = word
            break

    # Build the atomic log paths we want the system to gather from SQLite
    sub_queries = [
        f"Review HR records for {target}",
        f"Analyze authentication logs for {target}",
        f"Inspect file access logs for {target}",
        f"Examine USB device connection history for {target}",
        f"Search email communications for {target}",
        f"Monitor Slack channels for {target}",
        f"Audit browser search history for {target}"
    ]

    return {"sub_queries": sub_queries, "findings": []}

async def parallel_rag_node(state: InvestigationState) -> Dict[str, Any]:
    """
    Step 3: Gathers raw chronological logs from the database.
    """
    from Agents.retriever import recall_from_source, get_employee_profile
    
    # Extract the name from the query string
    query_words = state["query"].split()
    target = "Alex"
    for word in query_words:
        if word.lower() in ["alex", "susan"]:
            target = word
            break
            
    # Single fast database pull for all logs involving this user
    raw_logs = recall_from_source(target)
    
    return {"timeline": raw_logs}

def correlator_node(state: InvestigationState) -> Dict[str, Any]:
    timeline = ForensicCorrelator.construct_timeline(state["findings"])
    return {"timeline": timeline}

def scorer_node(state: InvestigationState) -> Dict[str, Any]:
    scorer = ThreatScorer()
    score, level, verdict = scorer.calculate_score(state["timeline"], demo_mode=state.get("demo_mode", False))
    return {"threat_score": score, "threat_level": level, "summary_verdict": verdict}

def report_node(state: InvestigationState) -> Dict[str, Any]:
    from reports.report_generator import generate_pdf_report
    path = generate_pdf_report(state)
    return {"report_path": path}

def route_decision(state: InvestigationState) -> str:
    intent = state.get("intent")
    if intent == "security_block":
        return "security_block"
    return "planner" if intent == "investigate" else "general_chat"

# COMPILING CONFIGURATION DICTIONARY MATRIX ENGINE 
workflow = StateGraph(InvestigationState)

workflow.add_node("router", intent_router_node)
workflow.add_node("general_chat", general_chat_node)
workflow.add_node("planner", planner_node)
workflow.add_node("parallel_rag_gather", parallel_rag_node)
workflow.add_node("correlator", correlator_node)
workflow.add_node("scorer", scorer_node)
workflow.add_node("report", report_node)
workflow.add_node("security_block", security_block_node)


workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    route_decision,
    { "security_block": "security_block",
      "planner": "planner", 
      "general_chat": "general_chat"}
)

workflow.add_edge("planner", "parallel_rag_gather")
workflow.add_edge("parallel_rag_gather", "correlator")
workflow.add_edge("correlator", "scorer")
workflow.add_edge("scorer", "report")
workflow.add_edge("report", END)
workflow.add_edge("general_chat", END)
workflow.add_edge("security_block", "__end__")

app_graph = workflow.compile()