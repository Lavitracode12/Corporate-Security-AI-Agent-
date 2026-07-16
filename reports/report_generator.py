import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(state: dict) -> str:
    # Use a fixed standard filename in the root workspace directory
    report_path = "report.pdf"
    
    doc = SimpleDocTemplate(report_path, pagesize=letter)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ReportTitle', parent=styles['Heading1'],
        textColor=colors.HexColor("#8B0000"), spaceAfter=12
    )
    
    story.append(Paragraph("INCIDENT FORENSIC AUDIT THREAT REPORT", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph(f"<b>Target Investigation Query:</b> {state.get('query')}", styles['Normal']))
    story.append(Paragraph(f"<b>Risk Assessment Severity:</b> {state.get('threat_level')} ({state.get('threat_score')}/100)", styles['Normal']))
    story.append(Paragraph(f"<b>Verbatim Executive Verdict:</b> {state.get('summary_verdict')}", styles['Normal']))
    story.append(Spacer(1, 18))
    
    # Chronological Table Construction Setup
    table_data = [["Timestamp", "Source Matrix Channel", "Activity Log Slice Snapshot"]]
    for event in state.get("timeline", []):
        # Added string typecast fallback safety boundary bounds to avoid None runtime slicing exceptions
        raw_ts = str(event.get("timestamp", ""))
        ts_display = raw_ts[:16] if len(raw_ts) >= 16 else raw_ts
        
        table_data.append([
            ts_display,
            str(event.get("source", "N/A")),
            str(event.get("details", "N/A"))[:65] + "..."
        ])
        
    t = Table(table_data, colWidths=[110, 100, 310])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A252C")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.lightgrey, colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    
    story.append(t)
    doc.build(story)
    return report_path