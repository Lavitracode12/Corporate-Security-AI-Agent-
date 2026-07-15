import sqlite3
import os
import json

def recall_from_source(employee_name: str) -> list:
    """
    RAG Step 1: Adaptive Document Retrieval with Active Local Terminal Auditing.
    """
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(CURRENT_DIR)

    path_uppercase = os.path.join(ROOT_DIR, "Memory", "corporate_security_agent.db")
    path_lowercase = os.path.join(ROOT_DIR, "memory", "corporate_security_agent.db")

    if os.path.exists(path_uppercase):
        db_path = path_uppercase
    elif os.path.exists(path_lowercase):
        db_path = path_lowercase
    else:
        db_path = os.path.join(ROOT_DIR, "corporate_security_agent.db")

    print(f"\n🔍 [IDE TERMINAL AUDIT] Path targeted for analysis: '{db_path}'")
    
    if not os.path.exists(db_path):
        print(f"⚠️ [IDE TERMINAL AUDIT] File does not exist at target destination.")
        return []
        
    # File size check to capture generated blank 0 KB files
    file_size = os.path.getsize(db_path)
    print(f"📦 [IDE TERMINAL AUDIT] Targeted database file size is: {file_size} bytes")
    if file_size == 0:
        print("🛑 [IDE TERMINAL AUDIT] ALERT: This database file is an empty 0 KB block. Delete this file and copy the original data file here!")
        return []

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT source_file, log_data FROM processed_logs")
        rows = cursor.fetchall()
        print(f"📖 [IDE TERMINAL AUDIT] Successfully scanned processed_logs table. Total raw rows in DB: {len(rows)}")
    except Exception as e:
        print(f"❌ [IDE TERMINAL AUDIT] Failed to query table 'processed_logs': {e}")
        conn.close()
        return []
        
    conn.close()
    
    retrieved_logs = []
    target_lower = employee_name.strip().lower()
    
    for source_file, raw_data in rows:
        try:
            log_obj = json.loads(raw_data)
            full_log_text = (str(source_file) + " " + str(raw_data)).lower()
            
            # Substring extraction validation
            if target_lower in full_log_text:
                log_obj["source_document"] = os.path.basename(source_file).replace(".json", "").upper()
                retrieved_logs.append(log_obj)
        except Exception:
            continue
            
    print(f"📊 [RAG RETRIEVAL] Matching complete. Found {len(retrieved_logs)} target matches for string: '{employee_name}'\n")
    return retrieved_logs

def get_employee_profile(query_text: str):
    return {"name": "Alex", "role": "Exiting Employee"}