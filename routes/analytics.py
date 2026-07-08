import os
from flask import Blueprint, send_file, jsonify
from database.models import Zone, Prediction, Alert, Sustainability, Recommendation
from ai.report_generator import generate_pdf_report

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/api/analytics/sustainability')
def get_sustainability_history():
    """
    Returns history of energy, water, waste, carbon footprint.
    """
    history = Sustainability.query.order_by(Sustainability.timestamp.desc()).limit(30).all()
    history.reverse() # chronologically ascending
    return jsonify([h.to_dict() for h in history])

@analytics_bp.route('/api/analytics/report/export')
def export_pdf_report():
    """
    Triggers generation of the PDF report and sends it to the user.
    """
    zones_data = Zone.query.all()
    predictions_data = Prediction.query.all()
    alerts_data = Alert.query.filter_by(resolved=False).all()
    sustainability_data = Sustainability.query.order_by(Sustainability.timestamp.desc()).first()
    
    # Format recommendations for the report
    recs = Recommendation.query.all()
    
    filename = "stadium_digital_twin_report.pdf"
    filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', filename)
    
    # Generate the file using report_generator module
    generate_pdf_report(
        filepath, 
        zones_data, 
        predictions_data, 
        alerts_data, 
        sustainability_data, 
        recs
    )
    
    # Check if a text file fallback was created instead of reportlab
    if not os.path.exists(filepath) and os.path.exists(filepath.replace('.pdf', '.txt')):
        return send_file(filepath.replace('.pdf', '.txt'), as_attachment=True, download_name="stadium_report.txt")
        
    return send_file(filepath, as_attachment=True, download_name="stadium_digital_twin_report.pdf")
