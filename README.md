# 🛡️ Corporate Security & Forensic Investigation Agent

A production-grade, state-managed **AI Forensic Investigation & Security Agent** built to replace rigid conversational pipelines with dynamic, multi-hop logical routing. The system safely validates corporate security guidelines, investigates login anomalies, maps chronological employee timelines, and calculates threat indices using deterministic fallback logic.

Live Demo Model is visualized through a high-performance **FastAPI backend** and an interactive, dark-themed **Streamlit operations dashboard** deployed in the cloud.

---

## 🎯 Architectural Highlights & Core Features

*   **🧠 LangGraph-Driven Intent Routing:** The agent acts as an intelligent routing system. General policy inquiries bypass forensic log databases entirely, routing directly to conversational pipelines to minimize token burn and processing latency.
*   **🔗 Multi-Hop Database Timeline Traversal:** When a target employee or threat profile is evaluated, the agent dynamically parses multiple independent logs—cross-referencing HR data directories, network authentication timelines, and system access patterns to stitch together a comprehensive chronological event list.
*   **🛡️ Active Input Security Guardrails:** An upstream defensive class inspects incoming prompts before database execution, immediately blocking malicious injection attempts, adversarial prompt overrides, or unauthorized clearance escalations.
*   **🎚️ Deterministic Threat Scoring Engine:** Implements a strict mathematical threat index (0-100) alongside localized heuristics. By locking model temperature at `0.0`, the system guarantees repeatable, objective threat evaluations.
*   **🔄 Fault-Tolerant Heuristic Fallback:** If cloud model rate limits ($429$) are hit, network requests spike, or API keys fail, the backend intercepts the crash instantly and routes execution to an offline math engine to maintain continuous system uptime.
*   **📊 Automatic PDF Report Generation:** Creates dynamic, production-quality forensic signature reports complete with executive summaries, threat indices, and log lists generated on-the-fly.

---

##  System Flowchart & State Architecture

          [ User Query ]
                   │
                   ▼
     [ Security Guardrails Intercept ]  ──(Adversarial Prompt)──► [ Access Denied ]
                   │
              (Safe Query)
                   │
                   ▼
      [ LangGraph Dynamic Router ]
         ├── (General Chat) ────────► [ Conversational Agent Node ]
         │                                        │
         └── (Investigation Profile Target)        ▼
                   │                    [ Return Direct Response ]
                   ▼
      [ Database Timeline Search ]
                   │
                   ▼
     [ Threat Scorer Model / Engine ]
         ├── (API Success) ──► [ AI Synthesis + Timeline Generation ]
         │                                   │
         └── (API Limit 429/Error)           ▼
                   └────────► [ Heuristic Fallback Pipeline ]
                                             │
                                             ▼
                                [ Dynamic PDF Generation ]
                                             │
                                             ▼
                                 [ Live Stream Download ]

## 🛠️ Tech Stack & Libraries Used

*   **Core Orchestration:** LangGraph, LangChain
*   **Language Model API:** Google Gemini Pro API (via `google-generativeai`)
*   **Backend REST Framework:** FastAPI, Uvicorn
*   **Frontend Dashboard UI:** Streamlit
*   **Database Interface:** SQLite / Python native database connectors
*   **PDF Compiler Asset Engine:** ReportLab
*   **Configuration & Security:** Python-dotenv, Pydantic (data-validation)

🚀 Setting Up Locally
1. Clone the repository:
Bash
git clone [https://github.com/yourusername/corporate-security-agent.git](https://github.com/yourusername/corporate-security-agent.git)
cd corporate-security-agent

2. Configure Environment Variables:
Create a .env file in the root directory:
Code snippet
GEMINI_API_KEY=your_actual_gemini_api_key_without_quotes
DATABASE_PATH=data/security_logs.db

3. Install Dependencies:
Bash
pip install -r requirements.txt

4. Run the FastAPI Backend:
Bash
uvicorn main:app --host 127.0.0.1 --port 8085 --reload

5. Start the Streamlit Client:
Bash
streamlit run frontend/app.py
