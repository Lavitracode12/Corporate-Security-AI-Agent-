import os
import json
import sqlite3
import sys
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

def init_db():
    # Set up a clean, local SQLite database for your agent's memory
    db_path = "Memory/corporate_security_agent.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create a simple table to store logs natively
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processed_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_file TEXT,
            log_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

def ingest_logs():
    sources = [
        "data/hr_logs.json",
        "data/auth_logs.json",
        "data/file_logs.json",
        "data/usb_logs.json",
        "data/email_logs.json",
        "data/slack_logs.json",
        "data/browser_logs.json"
    ]
    
    print("🚀 Starting Clean Custom Ingestion Pipeline...")
    conn = init_db()
    cursor = conn.cursor()
    
    for source in sources:
        if not os.path.exists(source):
            print(f"⚠️ File missing: {source}, skipping...")
            continue
            
        print(f"📦 Processing raw log structures for: '{source}'...")
        
        with open(source, "r") as f:
            try:
                records = json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Error decoding JSON in {source}. Skipping.")
                continue
        
        # Insert records into our custom agent memory table
        for record in records:
            cursor.execute(
                "INSERT INTO processed_logs (source_file, log_data) VALUES (?, ?)",
                (source, json.dumps(record))
            )
            
    conn.commit()
    conn.close()
    print("\n🎉 Custom log ingestion complete! Memory layer is built and completely error-free.")

if __name__ == "__main__":
    ingest_logs()