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
    query_lower = state["query"].lower()
    
    # 1. ACTIVE GUARDRAIL INTERCEPTION
    is_safe, threat_type, reason = SecurityGuardrails.check_input_safety(state["query"])
    if not is_safe:
        alert_message = (
            f"🛑 **SECURITY CLEARANCE DENIED: ACTIVE GUARDRAIL INTERCEPT**\n\n"
            f"**Violation Category:** `{threat_type.upper()}`\n"
            f"**Audit Log:** {reason}\n\n"
            f"*This directive has been logged and flagged in the InvenTech Security Incident Matrix.*"
        )
        return {
            "intent": "security_block",
            "summary_verdict": alert_message,
            "threat_score": 100.0,
            "threat_level": "CRITICAL / BLOCKED",
            "sub_queries": ["Intercept incoming adversarial prompt"],
            "findings": [],
            "timeline": []
        }

    # 2. CHAT OVERRIDE (For performance matrix or policies)
    # If they ask about performance, review, rating or general rules/policies,
    # force it to route to "chat" node even if it contains a monitored name.
    chat_keywords = ["performance", "review", "rating", "manager", "policy", "policies", "rule", "guideline", "bylaw"]
    if any(kw in query_lower for kw in chat_keywords):
        print("🟢 [ROUTER] Chat/Corporate Database intent matched (Overriding investigation routing).")
        return {"intent": "chat"}

    # 3. Precise Forensic Investigation Routing
    investigation_keywords = ["leak", "falcon", "audit", "log", "resigned", "history", "trace", "timeline", "check", "profile", "did"]
    name_keywords = ["alex", "susan", "brett", "michael"]
    
    if any(keyword in query_lower for keyword in investigation_keywords) or any(name in query_lower for name in name_keywords):
        print("🔍 [ROUTER] Forensic investigation intent isolated.")
        return {"intent": "investigate"}
        
    return {"intent": "chat"}

def security_block_node(state: InvestigationState) -> dict:
    return {}

def general_chat_node(state: dict) -> Dict[str, Any]:
    query = state.get("query", "")
    q_lower = query.lower()
    
    api_key = os.environ.get("GEMINI_API_KEY", "")
    client = genai.Client(api_key=api_key) if api_key else None
    
    retrieved_corporate_context = ""
    
    # DYNAMIC PATH TO TARGET THE POLICY VAULT DATABASE
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(CURRENT_DIR)
    
    # Targeting the correct security_vault.db in the root folder!
    db_path = os.path.join(ROOT_DIR, "security_vault.db")

    print(f"📁 [GENERAL CHAT DATABASE AUDIT] Connecting to: {db_path}")

    try:
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Scenario A: Performance Matrix Lookup
            if any(kw in q_lower for kw in ["perform", "review", "rate", "rating", "manager"]):
                target_name = None
                for name in ["alex", "susan", "brett", "michael"]:
                    if name in q_lower:
                        target_name = name
                        break
                
                if target_name:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='performance_reviews'")
                    if cursor.fetchone():
                        cursor.execute(
                            "SELECT role, manager, rating, review_text FROM performance_reviews WHERE employee_name LIKE ?", 
                            (f"%{target_name}%",)
                        )
                        row = cursor.fetchone()
                        if row:
                            retrieved_corporate_context += (
                                f"\n[INTERNAL HR PERFORMANCE MATRIX]\n"
                                f"Employee: {target_name.capitalize()} | Role: {row[0]} | Manager: {row[1]}\n"
                                f"Performance Rating: {row[2]}\n"
                                f"Manager Evaluation Brief: {row[3]}\n"
                            )

            # Scenario B: Corporate Policy Rule Lookup (using robust substring matches)
            if any(kw in q_lower for kw in ["polic", "rule", "prohibit", "allow", "guideline", "bylaw", "company", "data", "threat"]):
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='company_policies'")
                if cursor.fetchone():
                    cursor.execute("SELECT policy_section, policy_title, policy_content FROM company_policies")
                    policies = cursor.fetchall()
                    
                    matched_policies = []
                    for sec, title, content in policies:
                        content_lower = content.lower()
                        title_lower = title.lower()
                        # Matching singular/plurals and synonyms dynamically
                        if "polic" in q_lower or any(kw in content_lower or kw in title_lower for kw in ["rule", "guideline", "bylaw", "prohibited", "allowed", "falcon", "data", "threat"]):
                            matched_policies.append(f"Section {sec} - {title}: {content}")
                    
                    if matched_policies:
                        retrieved_corporate_context += "\n[CORPORATE COMPLIANCE POLICIES]\n" + "\n".join(matched_policies) + "\n"
            
            conn.close()
        else:
            print(f"⚠️ [GENERAL CHAT DATABASE AUDIT] security_vault.db not found at: {db_path}")
    except Exception as db_err:
        print(f"❌ SQLite general chat retrieval error: {db_err}")

    # GENERATION LAYER
    def _get_local_chat_response(q: str, context: str) -> str:
        q_lower = q.lower()
        if "name" in q_lower and ("company" in q_lower or "organization" in q_lower or "enterprise" in q_lower):
            return "🏢 The name of the company under audit is **InvenTech Solutions**."
        elif any(greet in q_lower for greet in ["hi", "hello", "hey"]):
            return "Hello! I am your automated Smart Enterprise & Operations Agent. How can I assist you today, CEO?"
        
        if context:
            return f"📊 **Executive Enterprise Information System [LOCAL ENGINE ACTIVE]**\n\n{context}"
        
        return f"I received your query: '{q}'. I am connected to the InvenTech Solutions network compliance engine. Please state a targeted operational directive."

    if state.get("demo_mode") or not client:
        verdict = _get_local_chat_response(query, retrieved_corporate_context)
    else:
        try:
            system_instruction = (
                "You are an Elite Enterprise Operations & Security Intelligent Assistant serving the CEO.\n"
                "Review the context block populated from the SQL backend database and answer the general security query with authority.\n"
                "Do not reference database names or system strings directly to the CEO. Speak naturally as an executive advisor."
            )
            prompt = f"{system_instruction}\n\nInternal Database Context:\n{retrieved_corporate_context}\n\nUser Query: {query}"
            
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=prompt,
                config={"temperature": 0.0}
            )
            verdict = response.text.strip()
        except Exception as api_err:
            print(f"⚠️ Gemini API execution failed, falling back to local database context parsing: {api_err}")
            verdict = _get_local_chat_response(query, retrieved_corporate_context)

    return {
        "summary_verdict": verdict,
        "intent": "chat",
        "threat_level": "N/A",
        "timeline": [],
        "sub_queries": ["General Chat Sequence Executed"]
    }

def planner_node(state: InvestigationState) -> Dict[str, Any]:
    query_words = state["query"].lower().split()
    target = "alex"
    for word in query_words:
        if word in ["alex", "susan", "brett", "michael"]:
            target = word
            break
    sub_queries = [f"Review HR records for {target.capitalize()}", f"Analyze authentication logs for {target.capitalize()}"]
    return {"sub_queries": sub_queries, "findings": [], "intent": "investigate"}

async def parallel_rag_node(state: InvestigationState) -> Dict[str, Any]:
    query_words = state["query"].lower().split()
    target = "alex"
    for word in query_words:
        if word in ["alex", "susan", "brett", "michael"]:
            target = word
            break
    raw_logs = recall_from_source(target)
    return {"timeline": raw_logs}

def correlator_node(state: InvestigationState) -> Dict[str, Any]:
    return {"timeline": state.get("timeline", [])}

def scorer_node(state: InvestigationState) -> Dict[str, Any]:
    scorer = ThreatScorer()
    score, level, verdict = scorer.calculate_score(state["timeline"], demo_mode=state.get("demo_mode", False))
    return {"threat_score": score, "threat_level": level, "summary_verdict": verdict}

def report_node(state: InvestigationState) -> Dict[str, Any]:
    return {"report_path": "report.pdf"}

def route_decision(state: InvestigationState) -> str:
    intent = state.get("intent")
    if intent == "security_block":
        return "security_block"
    return "planner" if intent == "investigate" else "general_chat"

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
workflow.add_conditional_edges("router", route_decision, {"security_block": "security_block", "planner": "planner", "general_chat": "general_chat"})
workflow.add_edge("planner", "parallel_rag_gather")
workflow.add_edge("parallel_rag_gather", "correlator")
workflow.add_edge("correlator", "scorer")
workflow.add_edge("scorer", "report")
workflow.add_edge("report", END)
workflow.add_edge("general_chat", END)
workflow.add_edge("security_block", "__end__")

app_graph = workflow.compile()