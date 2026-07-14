# init_corporate_kb.py
import sqlite3

def setup_corporate_knowledge_base():
    # Connect to your existing SQLite database file
    conn = sqlite3.connect("security_vault.db") 
    cursor = conn.cursor()
    
    # 1. Create the Performance Reviews Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT UNIQUE,
            role TEXT,
            manager TEXT,
            rating TEXT,
            review_text TEXT
        )
    """)
    
    # 2. Create the Company Policies Table (Our Structured Knowledge Base)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS company_policies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            policy_section TEXT UNIQUE,
            policy_title TEXT,
            policy_content TEXT
        )
    """)
    
    # 3. Inject Performance Data
    mock_reviews = [
        ("alex", "Senior Infrastructure Engineer", "Sarah Jenkins", "4.2/5", 
         "Alex shows exceptional technical execution and consistently meets system infrastructure goals. However, recent behavioral indicators note a sudden disengagement from team syncs."),
        ("susan", "Financial Operations Lead", "Sarah Jenkins", "4.8/5", 
         "Susan maintains flawless performance, keeping corporate ledger tracking highly accurate. Exceptional attention to regulatory protocols and data privacy compliance."),
        ("michael", "Research Scientist", "Sarah Jenkins", "4.5/5", 
         "Michael drives core engineering innovation effectively. Demonstrates high engagement across experimental development milestones."),
        ("brett", "Data Engineering Specialist", "Sarah Jenkins", "3.9/5", 
         "Brett delivers solid architectural designs, though documentation updates have lagged recently. Performance is standard, but upcoming exit transition protocols must be monitored.")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO performance_reviews (employee_name, role, manager, rating, review_text)
        VALUES (?, ?, ?, ?, ?)
    """, mock_reviews)
    
    # 4. Inject Corporate Compliance Policies
    mock_policies = [
        ("SEC_4.1", "Data Classification and Confidentiality", 
         "All internal project documentation—specifically engineering data relating to Project Falcon—is categorized as strictly restricted corporate intelligence. Unauthorized disclosure, sharing, or replication constitutes a tier-1 compliance violation."),
        ("SEC_4.2", "Removable Mass Storage Restrictions", 
         "The connection of unauthorized external hardware assets, including personal USB mass storage devices, removable flash drives, or standalone hard disk media to corporate workstations is strictly prohibited. All data transit actions must occur via monitored internal channels."),
        ("SEC_4.3", "Exfiltration Paths and Webmail Use", 
         "The transmission of internal company intellectual property, source archives, or project files to personal email accounts, unapproved cloud backup repositories, or public webmail applications is strictly tracked and prohibited under active corporate security bylaws."),
        ("HR_7.5", "Employee Resignation Protocols and Asset Return", 
         "Upon submission of an official resignation notice, the departing employee enters a structured offboarding window. The employee must immediately surrender access to confidential storage vaults and return all company hardware devices upon request.")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO company_policies (policy_section, policy_title, policy_content)
        VALUES (?, ?, ?)
    """, mock_policies)
    
    conn.commit()
    conn.close()
    print("🚀 Corporate Enterprise Knowledge Base initialized successfully inside SQLite!")

if __name__ == "__main__":
    setup_corporate_knowledge_base()