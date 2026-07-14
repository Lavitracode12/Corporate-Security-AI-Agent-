import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()

from Graph.workflow import app_graph
from Agents.retriever import recall_from_source
from Agents.scorer import ThreatScorer
from Agents.guardrails import SecurityGuardrails

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    demo_mode: bool = False

@app.post("/query")
async def run_investigation(request: QueryRequest):
    # ENTRY DOOR GUARDRAIL INTERCEPT
    # Stop malicious or phishing prompts before they touch ANY engine pipelines!
    is_safe, threat_type, reason = SecurityGuardrails.check_input_safety(request.query)
    
    if not is_safe:
        print(f"🚨 [API INTERCEPT] Guardrail violation caught: {threat_type}")
        return {
            "status": "blocked",
            "intent": "security_block",
            "threat_score": 100.0,
            "threat_level": "CRITICAL / BLOCKED",
            "summary_verdict": (
                f"🛑 **SECURITY CLEARANCE DENIED: ACTIVE GUARDRAIL INTERCEPT**\n\n"
                f"**Violation Category:** `{threat_type.upper()}`\n"
                f"**Audit Log:** {reason}\n\n"
                f"*This directive has been logged and flagged in the InvenTech Security Incident Matrix. "
                f"As an enterprise security agent, I am strictly restricted from executing commands that threaten corporate infrastructure, bypass compliance bylaws, or generate social engineering vectors.*"
            ),
            "sub_queries": ["Intercept incoming adversarial prompt"],
            "findings": [],
            "timeline": []
        }

  
    # NORMAL PIPELINE (Only runs if query passes safety checks)
   
    initial_state = {
        "query": request.query,
        "demo_mode": request.demo_mode,
        "intent": "chat",  # Default 
        "sub_queries": [],
        "findings": [],
        "timeline": [],
        "threat_score": 0.0,
        "threat_level": "N/A",  
        "summary_verdict": ""
    }
    
    try:
        # Execute the LangGraph flow steps
        final_state = await app_graph.ainvoke(initial_state)
        
        # INTERCEPT FOCUS: Check if the graph router isolated conversational chat intent
        if final_state.get("intent") == "chat" or final_state.get("threat_level") == "N/A":
            if not final_state.get("summary_verdict"):
                final_state["summary_verdict"] = "Hello! I am your Corporate Security Assistant. Please provide an explicit forensic directive or designate an employee's identity footprint to initialize a multi-hop timeline search sequence."
            
            final_state["threat_level"] = "N/A"
            final_state["timeline"] = []
            final_state["sub_queries"] = ["General Chat Sequence Executed"]
            return final_state

        # FULL INVESTIGATION PIPELINE (Only runs for real security queries)

        clean_q = request.query.lower().replace("?", "").replace(".", "").replace("'", "")
        query_words = clean_q.split()
        
        target_name = None
        if "employee" in query_words:
            idx = query_words.index("employee")
            if idx + 1 < len(query_words):
                target_name = query_words[idx + 1]
                
        if not target_name or target_name in ["has", "is", "was", "the"]:
            for name in ["alex", "susan", "brett", "michael"]:
                if name in query_words:
                    target_name = name
                    break
                    
        if not target_name:
            target_name = "alex"
            
        print(f"🎯 [BACKEND PARSER] Dynamic Forensics Target: '{target_name}'")
        
        # Load the exact timeline documents
        validated_logs = recall_from_source(target_name)
        final_state["timeline"] = validated_logs
        
        # Run threat intelligence calculations
        scorer = ThreatScorer()
        score, level, verdict = scorer.calculate_score(validated_logs, demo_mode=request.demo_mode)
        
        final_state["threat_score"] = score
        final_state["threat_level"] = level
        final_state["summary_verdict"] = verdict
        
        if not final_state.get("sub_queries") or "Alex" in final_state.get("sub_queries")[0]:
            final_state["sub_queries"] = [
                f"Review HR records for {target_name.capitalize()}",
                f"Analyze authentication logs for {target_name.capitalize()}",
                f"Inspect file access logs for {target_name.capitalize()}",
                f"Examine USB device connection history for {target_name.capitalize()}",
                f"Search email communications for {target_name.capitalize()}",
                f"Monitor Slack channels for {target_name.capitalize()}",
                f"Audit browser search history for {target_name.capitalize()}"
            ]
            
        return final_state
        
    except Exception as e:
        print(f"❌ Core API transmission pipeline failure: {e}")
        raise HTTPException(status_code=500, detail=str(e))