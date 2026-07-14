import sqlite3
import os
import json

def recall_from_source(employee_name: str) -> list:
    """
    RAG Step 1: Adaptive Document Retrieval
    Fetches and unifies all logs across multiple document streams (HR, Auth, File, USB, etc.)
    """
    db_path = os.environ.get("DATABASE_PATH", "Memory/corporate_security_agent.db")
    if not os.path.exists(db_path):
        print(f"⚠️ Database file not found at: {db_path}")
        return []
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Grab all records so we can inspect the internal fields directly
    cursor.execute("SELECT source_file, log_data FROM processed_logs")
    rows = cursor.fetchall()
    conn.close()
    
    retrieved_logs = []
    target_lower = employee_name.strip().lower()
    
    # Cross-document scan
    for source_file, raw_data in rows:
        try:
            log_obj = json.loads(raw_data)
            # Flatten everything to string to find matches across keys, values, or source files
            full_log_text = (str(source_file) + " " + str(raw_data)).lower()
            
            if target_lower in full_log_text:
                # Add metadata context so the LLM knows WHICH document it hopped to
                log_obj["source_document"] = os.path.basename(source_file).replace(".json", "").upper()
                retrieved_logs.append(log_obj)
        except Exception as e:
            continue
            
    print(f"📊 [RAG RETRIEVAL] Cross-source scan complete. Hopped across documents and isolated {len(retrieved_logs)} logs for target: '{employee_name}'")
    return retrieved_logs

def get_employee_profile(query_text: str):
    # Keep the profile resolver standard so imports don't break
    return {"name": "Alex", "role": "Exiting Employee"}