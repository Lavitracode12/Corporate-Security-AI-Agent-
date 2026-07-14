import json
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
random.seed(42)

def generate_synthetic_data():
    base_time = datetime(2026, 6, 20, 0, 0, 0)
    
    # 1. HR Logs
    hr_logs = [
        {"employee_id": "EMP001", "name": "Alex Chen", "role": "Principal Security Engineer", "department": "Infrastructure", "manager": "Sarah Jenkins", "start_date": "2022-03-11", "resignation_date": "2026-06-25", "status": "Resigned"},
        {"employee_id": "EMP002", "name": "Sarah Jenkins", "role": "VP of Infrastructure", "department": "Infrastructure", "manager": "CEO", "start_date": "2020-01-15", "resignation_date": None, "status": "Active"}
    ]
    for i in range(3, 25):
        hr_logs.append({
            "employee_id": f"EMP{i:03d}", "name": fake.name(), "role": fake.job(), "department": random.choice(["Engineering", "Sales", "HR", "Legal"]),
            "manager": "Sarah Jenkins", "start_date": "2024-05-01", "resignation_date": None, "status": "Active"
        })

    # 2. Auth Logs (Planting Alex's Anomaly at 2:13 AM)
    auth_logs = [
        {"timestamp": (base_time + timedelta(hours=2, minutes=13)).isoformat(), "employee_id": "EMP001", "username": "achen", "ip_address": "198.51.100.42", "location": "Unknown (VPN Out of State)", "device": "Personal-MacBook", "status": "Success", "failure_reason": None}
    ]
    
    # 3. File Logs (Massive Download)
    file_logs = []
    for m in range(15, 45):
        file_logs.append({
            "timestamp": (base_time + timedelta(hours=2, minutes=m)).isoformat(), "employee_id": "EMP001", "action": "DOWNLOAD",
            "filename": f"falcon_schematic_v{m-14}.dwg", "file_path": f"/shared/project_falcon/designs/falcon_schematic_v{m-14}.dwg",
            "project_tag": "Project Falcon", "size_mb": 26.5
        })

    # 4. Email Logs (Large attachment to personal account)
    email_logs = [
        {"timestamp": (base_time + timedelta(hours=2, minutes=47)).isoformat(), "sender": "alex.chen@corporate.com", "recipient": "alex.chen.99.personal@gmail.com", "subject": "Archived Personal Notes", "has_attachment": True, "attachment_name": "project_falcon_backup.zip", "size_mb": 847.0}
    ]

    # 5. USB Logs (External Mount)
    usb_logs = [
        {"timestamp": (base_time + timedelta(hours=3, minutes=47)).isoformat(), "employee_id": "EMP001", "device_id": "USB-SanDisk-AX882", "device_type": "External Mass Storage", "action": "CONNECTED", "files_transferred": 142}
    ]

    # 6. Slack Logs (The Smoking Gun text)
    slack_logs = [
        {"timestamp": (base_time + timedelta(hours=4, minutes=12)).isoformat(), "user": "Alex Chen", "channel": "project-falcon", "message": "Wrapping up my tasks here. I'll keep a copy for reference 😉", "reactions": ["thumbsup"]}
    ]

    # 7. Browser Logs (Exfiltration destination)
    browser_logs = [
        {"timestamp": (base_time + timedelta(hours=4, minutes=45)).isoformat(), "employee_id": "EMP001", "url": "https://www.dropbox.com/home/upload", "action": "POST_UPLOAD", "data_transferred_mb": 1200.0}
    ]

    # Add random background noise to all lists from other employees
    for i in range(50):
        emp = f"EMP{random.randint(2, 24):03d}"
        noise_time = (base_time + timedelta(minutes=random.randint(0, 1440))).isoformat()
        auth_logs.append({"timestamp": noise_time, "employee_id": emp, "username": f"user_{emp}", "ip_address": fake.ipv4(), "location": "Office Branch", "device": "Corp-Laptop", "status": "Success", "failure_reason": None})
        file_logs.append({"timestamp": noise_time, "employee_id": emp, "action": "READ", "filename": "weekly_report.xlsx", "file_path": "/shared/docs/weekly_report.xlsx", "project_tag": "General", "size_mb": 1.2})

    # Write files out securely
    sources = {
        "data/hr_logs.json": hr_logs, "data/auth_logs.json": auth_logs, "data/file_logs.json": file_logs,
        "data/usb_logs.json": usb_logs, "data/email_logs.json": email_logs, "data/slack_logs.json": slack_logs,
        "data/browser_logs.json": browser_logs
    }
    
    import os
    os.makedirs("data", exist_ok=True)
    for path, data in sources.items():
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    print("Successfully populated synthetic corporate ecosystem logs.")

if __name__ == "__main__":
    generate_synthetic_data()