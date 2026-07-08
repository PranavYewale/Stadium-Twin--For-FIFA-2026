import os
from datetime import datetime

# Import reportlab parts with fallbacks
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

def generate_pdf_report(filename, zones_data, predictions_data, alerts_data, sustainability_data, ai_recommendations):
    """
    Generates a beautifully formatted PDF report summarizing the stadium state.
    Falls back to a detailed text report if reportlab is not installed.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not HAS_REPORTLAB:
        # Create a text file report fallback
        txt_filename = filename.replace('.pdf', '.txt')
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write(f"FIFA WORLD CUP 2026 - DIGITAL TWIN REPORT\n")
            f.write(f"Generated at: {now_str}\n")
            f.write("="*60 + "\n\n")
            
            f.write("1. ZONE & SECTOR CAPACITIES\n")
            f.write("-"*30 + "\n")
            for z in zones_data:
                f.write(f"{z.name} ({z.zone_type.upper()}): {z.current_crowd}/{z.capacity} - Risk: {z.risk_score} [{z.status}]\n")
            f.write("\n")
            
            f.write("2. SUSTAINABILITY METRICS\n")
            f.write("-"*30 + "\n")
            if sustainability_data:
                f.write(f"Energy: {sustainability_data.energy_kwh:.2f} kWh\n")
                f.write(f"Water: {sustainability_data.water_liters:.2f} Liters\n")
                f.write(f"Carbon Footprint: {sustainability_data.carbon_footprint_kg:.2f} kg CO2\n")
                f.write(f"Sustainability Score: {sustainability_data.sustainability_score:.2f}%\n")
            else:
                f.write("No sustainability data available.\n")
            f.write("\n")
            
            f.write("3. RECENT ACTIVE ALERTS\n")
            f.write("-"*30 + "\n")
            if alerts_data:
                for a in alerts_data:
                    f.write(f"[{a.level.upper()}] {a.message} ({a.timestamp})\n")
            else:
                f.write("No active incidents.\n")
            f.write("\n")
            
            f.write("4. AI OPERATOR RECOMMENDATIONS\n")
            f.write("-"*30 + "\n")
            if ai_recommendations:
                # Can be a list or dict depending on context
                if isinstance(ai_recommendations, dict):
                    f.write(f"Analysis: {ai_recommendations.get('analysis', '')}\n\n")
                    for action in ai_recommendations.get('priority_actions', []):
                        f.write(f"- {action.get('title')} ({action.get('location')}): {action.get('description')} (Volunteers: {action.get('volunteers_needed')}) -> Outcome: {action.get('expected_outcome')}\n")
                else:
                    for r in ai_recommendations:
                        f.write(f"- [{r.priority}] {r.issue}: {r.recommendation} -> {r.expected_outcome}\n")
            else:
                f.write("No recommendations generated yet.\n")
                
        # Copy the text file contents to a fake pdf for route handling compatibility
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"%PDF-1.4 mock pdf content wrapper. Check original txt file at {txt_filename}")
        return filename

    # ReportLab Generation
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SectionStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )
    
    # Title
    story.append(Paragraph(f"FIFA World Cup 2026 - Stadium Digital Twin AI Report", title_style))
    story.append(Paragraph(f"Report generated: {now_str}", body_style))
    story.append(Spacer(1, 10))
    
    # 1. Zone Telemetry Table
    story.append(Paragraph("1. Sector and Zone Telemetry", section_style))
    table_data = [["Zone ID", "Name", "Type", "Crowd", "Capacity", "Risk", "Status"]]
    for z in zones_data:
        table_data.append([z.id, z.name, z.zone_type.capitalize(), str(z.current_crowd), str(z.capacity), f"{z.risk_score}%", z.status])
        
    t = Table(table_data, colWidths=[80, 100, 70, 60, 60, 50, 60])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    # 2. Sustainability Section
    story.append(Paragraph("2. Sustainability Metrics", section_style))
    if sustainability_data:
        sus_data = [
            ["Metric", "Value", "Unit"],
            ["Energy Consumption", f"{sustainability_data.energy_kwh:.2f}", "kWh"],
            ["Water Consumption", f"{sustainability_data.water_liters:.2f}", "Liters"],
            ["Waste Collected", f"{sustainability_data.waste_kg:.2f}", "kg"],
            ["Estimated Carbon Footprint", f"{sustainability_data.carbon_footprint_kg:.2f}", "kg CO2"],
            ["Overall Sustainability Score", f"{sustainability_data.sustainability_score:.1f}%", ""]
        ]
        t_sus = Table(sus_data, colWidths=[180, 120, 80])
        t_sus.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#0f766e")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(t_sus)
    else:
        story.append(Paragraph("No sustainability metrics tracked.", body_style))
    story.append(Spacer(1, 15))
    
    # 3. Active Incidents
    story.append(Paragraph("3. Active Incidents & Security Alerts", section_style))
    if alerts_data:
        alert_table_data = [["Level", "Message", "Location", "Timestamp"]]
        for a in alerts_data:
            alert_table_data.append([a.level.upper(), a.message, a.zone_id or "Global", a.timestamp.strftime("%H:%M:%S")])
        t_alert = Table(alert_table_data, colWidths=[60, 240, 80, 80])
        t_alert.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#991b1b")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ]))
        story.append(t_alert)
    else:
        story.append(Paragraph("Stadium is clean. No active incidents recorded.", body_style))
    story.append(Spacer(1, 15))
    
    # 4. AI Gemini Recommendations
    story.append(Paragraph("4. AI Gemini Core Action Plan", section_style))
    if ai_recommendations:
        if isinstance(ai_recommendations, dict):
            story.append(Paragraph(f"<b>Core Analysis:</b> {ai_recommendations.get('analysis', '')}", body_style))
            story.append(Spacer(1, 5))
            rec_table = [["Action Title", "Zone", "Priority", "Description", "Outcome"]]
            for action in ai_recommendations.get('priority_actions', []):
                rec_table.append([
                    action.get('title'),
                    action.get('location'),
                    action.get('priority'),
                    action.get('description'),
                    action.get('expected_outcome')
                ])
            t_rec = Table(rec_table, colWidths=[100, 60, 60, 200, 100])
            t_rec.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563eb")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            story.append(t_rec)
        else:
            for r in ai_recommendations:
                story.append(Paragraph(f"<b>[{r.priority}] {r.issue}:</b> {r.recommendation} <i>(Expected outcome: {r.expected_outcome})</i>", body_style))
    else:
        story.append(Paragraph("No operator recommendations found.", body_style))
        
    doc.build(story)
    return filename
