import streamlit as st
import requests
import os

st.set_page_config(page_title="Corporate Security Memory Agent UI", layout="wide", page_icon="🛡️")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20,400,0,0&display=swap');

:root{
  --bg:            #0A0E13;
  --bg-panel:      #10151C;
  --bg-panel-alt:  #151B23;
  --border:        #212934;
  --border-soft:   #1A2129;
  --text:          #E7EAEE;
  --text-muted:    #8B96A3;
  --text-faint:    #5C6672;
  --amber:         #D9A441;
  --amber-dim:     #4A3B22;
  --cyan:          #4FB8C4;
  --cyan-dim:      #1E3438;
  --red:           #C1554A;
  --red-dim:       #3A2320;
  --green:         #6FA287;
  --green-dim:     #223129;
}

.material-symbols-outlined{
  font-variation-settings: 'FILL' 0, 'wght' 450, 'GRAD' 0, 'opsz' 22;
  vertical-align: middle;
  line-height: 1;
}

html, body, [class*="css"]{ font-family: 'IBM Plex Sans', sans-serif; }

.stApp{
  background:
    radial-gradient(1200px 500px at 15% -10%, #12181F 0%, transparent 60%),
    var(--bg);
  color: var(--text);
}

/* Kill default top padding so the case-header sits high on the page */
.block-container{ padding-top: 2.2rem; padding-bottom: 3rem; max-width: 1180px; }

/* ── Sidebar ─────────────────────────────────────────────────────────── */
section[data-testid="stSidebar"]{
  background: var(--bg-panel);
  border-right: 1px solid var(--border-soft);
}
section[data-testid="stSidebar"] .block-container{ padding-top: 1.6rem; }

.console-brand{
  display:flex; align-items:center; gap:10px;
  margin-bottom: 4px;
}
.console-brand .material-symbols-outlined{
  font-size: 30px; color: var(--amber);
}
.console-brand-text .eyebrow{
  font-family:'IBM Plex Mono'; font-size:10px; letter-spacing:.14em;
  color: var(--text-faint); text-transform:uppercase;
}
.console-brand-text h1{
  font-family:'Space Grotesk'; font-size:19px; font-weight:600; margin:0;
  color: var(--text); letter-spacing:.01em;
}
.console-divider{ height:1px; background:var(--border-soft); margin:16px 0; border:none; }

.fabric-heading{
  display:flex; align-items:center; gap:7px;
  font-family:'IBM Plex Mono'; font-size:11px; letter-spacing:.1em;
  color: var(--text-muted); text-transform:uppercase; margin-bottom:12px;
}
.fabric-heading .material-symbols-outlined{ font-size:16px; color:var(--cyan); }

.fabric-card{
  background: var(--bg-panel-alt);
  border: 1px solid var(--border-soft);
  border-left: 3px solid var(--green);
  border-radius: 6px;
  padding: 10px 12px;
  margin-bottom: 9px;
}
.fabric-name{
  font-family:'IBM Plex Sans'; font-weight:500; font-size:13.5px; color:var(--text);
}
.fabric-status{
  display:flex; align-items:center; gap:6px; margin-top:3px;
}
.fabric-dot{
  width:6px; height:6px; border-radius:50%; background:var(--green);
  box-shadow: 0 0 6px var(--green);
}
.fabric-status span.label{
  font-family:'IBM Plex Mono'; font-size:10.5px; color: var(--green); letter-spacing:.04em;
}

/* ── Header ──────────────────────────────────────────────────────────── */
.case-header{ display:flex; align-items:flex-start; gap:16px; margin-bottom:4px; }
.case-header .material-symbols-outlined{
  font-size:40px; color:var(--amber);
  background: var(--amber-dim);
  border: 1px solid #5c4a26;
  border-radius: 10px;
  padding: 8px;
}
.case-header h1{
  font-family:'Space Grotesk'; font-weight:700; font-size:32px;
  color:var(--text); margin:0 0 4px 0; letter-spacing:.005em;
}
.case-header .subtitle{
  font-family:'IBM Plex Mono'; font-size:13px; color:var(--text-muted);
  letter-spacing:.03em;
}
.section-rule{ height:1px; background:var(--border-soft); margin:26px 0 22px 0; border:none; }

.field-label{
  font-family:'IBM Plex Mono'; font-size:11.5px; letter-spacing:.08em;
  color:var(--text-muted); text-transform:uppercase; margin-bottom:6px;
}

/* ── Inputs ──────────────────────────────────────────────────────────── */
div[data-testid="stTextInput"] input{
  background: var(--bg-panel-alt) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  font-family:'IBM Plex Mono';
  font-size: 14px;
  border-radius: 8px !important;
  padding: 12px 14px !important;
}
div[data-testid="stTextInput"] input:focus{
  border-color: var(--amber) !important;
  box-shadow: 0 0 0 1px var(--amber) !important;
}

div[data-testid="stButton"] button{
  background: var(--amber) !important;
  color: #14100A !important;
  border: none !important;
  font-family:'Space Grotesk';
  font-weight: 600 !important;
  letter-spacing: .01em;
  border-radius: 8px !important;
  padding: 0.6rem 1.3rem !important;
  transition: filter .15s ease;
}
div[data-testid="stButton"] button:hover{ filter: brightness(1.12); }
div[data-testid="stButton"] button p{ font-family:'Space Grotesk' !important; font-weight:600 !important; }

label[data-testid="stWidgetLabel"] p{
  font-family:'IBM Plex Mono' !important; font-size:12px !important;
  letter-spacing:.06em; color: var(--text-muted) !important;
  text-transform:uppercase;
}

/* toggle */
div[data-testid="stToggle"] label div[data-baseweb="checkbox"] div{
  background-color: var(--border) !important;
}

/* expander */
div[data-testid="stExpander"]{
  background: var(--bg-panel);
  border: 1px solid var(--border-soft) !important;
  border-radius: 10px !important;
}
div[data-testid="stExpander"] summary{
  font-family:'Space Grotesk'; font-weight:600; color: var(--text) !important;
}

/* json viewer blend */
div[data-testid="stJson"]{
  background: var(--bg-panel-alt) !important;
  border: 1px solid var(--border-soft) !important;
  border-radius: 8px !important;
}

/* ── Reusable cards ──────────────────────────────────────────────────── */
.metric-card{
  background: var(--bg-panel-alt);
  border: 1px solid var(--border-soft);
  border-radius: 10px;
  padding: 16px 20px;
}
.metric-label{
  font-family:'IBM Plex Mono'; font-size:11px; letter-spacing:.08em;
  color: var(--text-muted); text-transform:uppercase; margin-bottom:8px;
}
.metric-value{
  font-family:'Space Grotesk'; font-size:30px; font-weight:700; color:var(--text);
}
.level-chip{
  display:inline-block; font-family:'IBM Plex Mono'; font-size:13px;
  font-weight:600; letter-spacing:.06em; padding: 5px 12px; border-radius:6px;
}
.level-LOW{ background: var(--green-dim); color: var(--green); border:1px solid #2f4a3d; }
.level-MEDIUM{ background: var(--amber-dim); color: var(--amber); border:1px solid #5c4a26; }
.level-MED{ background: var(--amber-dim); color: var(--amber); border:1px solid #5c4a26; }
.level-HIGH{ background: var(--red-dim); color: var(--red); border:1px solid #5a332e; }
.level-CRITICAL{ background: var(--red-dim); color: var(--red); border:1px solid #5a332e; }
.level-DEFAULT{ background: var(--bg-panel); color: var(--text-muted); border:1px solid var(--border); }

.alert-card{
  border-radius: 10px; padding: 16px 18px; margin: 6px 0 18px 0;
  display:flex; gap:12px; align-items:flex-start;
  font-family:'IBM Plex Sans'; font-size:14.5px; line-height:1.5;
}
.alert-card .material-symbols-outlined{ font-size:22px; margin-top:1px; flex-shrink:0; }
.alert-title{ font-family:'Space Grotesk'; font-weight:600; font-size:15px; margin-bottom:3px; display:block; }
.alert-error{ background: var(--red-dim); border:1px solid #5a332e; color:#F0C9C3; }
.alert-error .material-symbols-outlined, .alert-error .alert-title{ color: var(--red); }
.alert-warning{ background: var(--amber-dim); border:1px solid #5c4a26; color:#F0DDB8; }
.alert-warning .material-symbols-outlined, .alert-warning .alert-title{ color: var(--amber); }
.alert-success{ background: var(--green-dim); border:1px solid #2f4a3d; color:#CFE6D9; }
.alert-success .material-symbols-outlined, .alert-success .alert-title{ color: var(--green); }
.alert-info{ background: var(--cyan-dim); border:1px solid #2c4d52; color:#C7E7EA; }
.alert-info .material-symbols-outlined, .alert-info .alert-title{ color: var(--cyan); }

.section-heading{
  display:flex; align-items:center; gap:9px; margin: 6px 0 16px 0;
}
.section-heading .material-symbols-outlined{ font-size:20px; color:var(--cyan); }
.section-heading h3{
  font-family:'Space Grotesk'; font-weight:600; font-size:18px; color:var(--text); margin:0;
}

.trace-step{
  display:flex; gap:14px; align-items:flex-start; margin-bottom: 4px; padding-left: 4px;
  border-left: 2px solid var(--border); padding-bottom: 16px; margin-left: 13px;
}
.trace-step:last-child{ border-left: 2px solid transparent; padding-bottom:0; }
.trace-index{
  font-family:'IBM Plex Mono'; font-size:11px; font-weight:600; color:#14100A;
  background: var(--cyan); width:24px; height:24px; border-radius:50%;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
  margin-left:-25px; margin-top:-1px;
}
.trace-text{ font-family:'IBM Plex Mono'; font-size:13.5px; color: var(--text); padding-top:2px; }
.trace-text .trace-label{ color: var(--text-muted); font-family:'IBM Plex Sans'; font-size:12.5px; display:block; margin-bottom:2px; }

.timeline-entry{
  background: var(--bg-panel-alt);
  border: 1px solid var(--border-soft);
  border-left: 3px solid var(--cyan);
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 12px;
}
.timeline-top{ display:flex; align-items:center; gap:10px; margin-bottom:8px; flex-wrap:wrap; }
.timeline-ts{
  font-family:'IBM Plex Mono'; font-size:12.5px; color:var(--cyan);
  background: var(--cyan-dim); padding:3px 9px; border-radius:5px;
}
.timeline-src{
  font-family:'IBM Plex Mono'; font-size:11px; letter-spacing:.05em; color:var(--amber);
  background: var(--amber-dim); padding:3px 9px; border-radius:5px; text-transform:uppercase;
}

.report-link{
  display:inline-flex; align-items:center; gap:8px;
  background: var(--bg-panel-alt); border:1px solid var(--border);
  border-radius:8px; padding:10px 16px; text-decoration:none !important;
  font-family:'Space Grotesk'; font-weight:600; font-size:14px; color: var(--amber) !important;
  transition: border-color .15s ease;
}
.report-link:hover{ border-color: var(--amber); }
.report-link .material-symbols-outlined{ font-size:18px; }
</style>
""", unsafe_allow_html=True)

def alert(kind: str, icon: str, title: str, message: str):
    st.markdown(f"""
    <div class="alert-card alert-{kind}">
        <span class="material-symbols-outlined">{icon}</span>
        <div><span class="alert-title">{title}</span>{message}</div>
    </div>
    """, unsafe_allow_html=True)

def level_class(level: str) -> str:
    key = str(level).strip().upper()
    return f"level-{key}" if f"level-{key}" in {
        "level-LOW", "level-MEDIUM", "level-MED", "level-HIGH", "level-CRITICAL"
    } else "level-DEFAULT"

# SIDEBAR: Connected Corporate Data Fabrics Overview
with st.sidebar:
    st.markdown("""
    <div class="console-brand">
        <span class="material-symbols-outlined">shield_lock</span>
        <div class="console-brand-text">
            <div class="eyebrow">Access Level: Analyst</div>
            <h1>Control Console</h1>
        </div>
    </div>
    <hr class="console-divider" />
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="fabric-heading">
        <span class="material-symbols-outlined">database</span>
        Enterprise Knowledge Fabrics
    </div>
    """, unsafe_allow_html=True)

    fabrics = [
        "Forensics Log Ledger (SQLite online)",
        "HR Performance Database (SQLite online)",
        "Compliance Policy Matrix (SQLite online)",
    ]
    for f in fabrics:
        name, status = f.rsplit("(", 1)
        st.markdown(f"""
        <div class="fabric-card">
            <div class="fabric-name">{name.strip()}</div>
            <div class="fabric-status">
                <span class="fabric-dot"></span>
                <span class="label">{status.replace(")", "").strip().upper()}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="case-header">
    <span class="material-symbols-outlined">shield_lock</span>
    <div>
        <h1>Corporate Security Memory Agent</h1>
        <div class="subtitle">Persistent Hybrid Graph-Vector Cross-Source Forensic Investigation Engine</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="section-rule" />', unsafe_allow_html=True)
st.markdown('<div class="field-label">Enter Investigative Security Directive</div>', unsafe_allow_html=True)
query_input = st.text_input(
    "Enter Investigative Security Directive:",
    value="Did employee Alex leak confidential Project Falcon documents before resigning?",
    label_visibility="collapsed",
)

# Demo Mode Toggle
demo_mode = st.toggle(
    "Demo Mode (Offline / Mock LLM)",
    value=False,
    help="Bypasses upstream Gemini API calls to use robust local deterministic logic and avoid rate limits."
)

execute = st.button("Execute Multi-Hop Forensics Routing Sequence", icon=":material/play_arrow:")

if execute:
    with st.spinner("Traversing across the documents..."):
        try:
            res = requests.post(
                "http://127.0.0.1:8080/query",
                json={"query": query_input, "demo_mode": demo_mode}
            ).json()

            threat_level = res.get("threat_level")

            if res.get("status") == "blocked" or "SECURITY CLEARANCE DENIED" in str(res.get("summary_verdict")):
                alert(
                    "error", "gpp_maybe",
                    "Active Security Intercept: Adversarial Threat Neutralized",
                    res.get("summary_verdict", "This directive violates established corporate safety guardrails."),
                )
                st.stop()

            elif res.get("threat_level") == "N/A":
                # INTERACTIVE CHAT MODE VIEW
                st.markdown("""
                <div class="section-heading">
                    <span class="material-symbols-outlined">chat</span>
                    <h3>Interactive Security Chat Mode Active</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="field-label">Assistant Response</div>', unsafe_allow_html=True)
                st.write(res.get("summary_verdict"))

            else:
                # FULL FORENSIC INVESTIGATION VIEW
                # 1. Metric Callout Banners
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Calculated Threat Score Indicator</div>
                        <div class="metric-value">{res.get('threat_score')}/100</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-label">Threat Classification Level Status</div>
                        <span class="level-chip {level_class(threat_level)}">{threat_level}</span>
                    </div>
                    """, unsafe_allow_html=True)

                st.write("")
                alert("info", "gavel", "Executive Forensic Verdict Summary:", res.get("summary_verdict"))

                # 2. Sequential Multihop Subquery Planner Processing Blocks Trace
                st.markdown("""
                <div class="section-heading">
                    <span class="material-symbols-outlined">account_tree</span>
                    <h3>Decomposed Investigative Search Steps Tracker (Multi-Hop Trace)</h3>
                </div>
                """, unsafe_allow_html=True)
                for i, step in enumerate(res.get("sub_queries", [])):
                    st.markdown(f"""
                    <div class="trace-step">
                        <div class="trace-index">{i+1}</div>
                        <div class="trace-text">
                            <span class="trace-label">Step {i+1} Vector Node Traversal Path Flag</span>
                            {step}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                # 3. Dynamic Chronological Log Timeline Data Grid Representation Matrix
                st.markdown("""
                <div class="section-heading" style="margin-top:28px;">
                    <span class="material-symbols-outlined">timeline</span>
                    <h3>Generated Unified Forensic Incident Chronological Timeline View</h3>
                </div>
                """, unsafe_allow_html=True)
                timeline_data = res.get("timeline", [])

                if not timeline_data:
                    alert("warning", "search_off", "No records found", "No context records located in timeline payload matrix.")
                else:
                    for event in timeline_data:
                        source_doc = event.get('source_document', event.get('source', 'LOG'))
                        st.markdown(f"""
                        <div class="timeline-entry">
                            <div class="timeline-top">
                                <span class="timeline-ts">{event.get('timestamp', 'N/A')}</span>
                                <span class="timeline-src">{source_doc.upper()}</span>
                            </div>
                        """, unsafe_allow_html=True)

                        details = event.get('details', event.get('action', event))
                        if isinstance(details, (dict, list)):
                            st.json(details)
                        else:
                            alert("info", "description", "", str(details))

                        st.markdown("</div>", unsafe_allow_html=True)

                # 4. Built Report Lab Document File Assets Endpoint Sync Stream Action
                report_path = res.get("report_path")
                if report_path:
                    report_url = f"http://127.0.0.1:8080/report?path={report_path}"
                    alert("success", "task_alt", "", "Professional Incident Audit Log PDF Compiled Successfully.")
                    st.markdown(f"""
                    <a class="report-link" href="{report_url}" target="_blank">
                        <span class="material-symbols-outlined">download</span>
                        Download Official Incident Signature Report PDF
                    </a>
                    """, unsafe_allow_html=True)

        except Exception as e:
            alert("error", "wifi_off", "Connection Failed",
                  f"Failed connection transaction stream intercept validation sequence checklist exception: {str(e)}")

# BOTTOM SECTION: Interactive System Architecture Flowchart
st.markdown('<hr class="section-rule" />', unsafe_allow_html=True)
with st.expander("View System Graph Agent Architecture Diagram", icon=":material/hub:"):
    try:
        from Graph.workflow import app_graph
        # Fetch the Mermaid PNG byte stream dynamically from your compiled graph object
        graph_image_bytes = app_graph.get_graph().draw_mermaid_png()
        st.image(graph_image_bytes, caption="Persistent Hybrid Forensic Engine State Machine Workflow Layout")
    except Exception as e:
        alert("info", "hub", "", "Architecture diagram rendering active. For full visualization, ensure graphviz is configured.")


























