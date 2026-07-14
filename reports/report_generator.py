import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_pdf_report(state: dict) -> str:
    os.makedirs("output_reports", exist_ok=True)
    report_path = f"output_reports/incident_report_{int(state.get('threat_score',0))}.pdf"
    
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
        table_data.append([
            event.get("timestamp")[:16],
            event.get("source"),
            str(event.get("details"))[:65] + "..."
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