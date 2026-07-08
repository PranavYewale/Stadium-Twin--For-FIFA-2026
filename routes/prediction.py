from flask import Blueprint, jsonify
from database.models import Prediction, Zone

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/api/predictions')
def get_all_predictions():
    """
    Returns predictions for all stadium zones grouped by offset.
    """
    predictions = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    results = {}
    
    for p in predictions:
        if p.zone_id not in results:
            results[p.zone_id] = []
        results[p.zone_id].append(p.to_dict())
        
    return jsonify(results)

@prediction_bp.route('/api/predictions/<zone_id>')
def get_zone_predictions(zone_id):
    """
    Returns predictions for a single zone.
    """
    zone = Zone.query.filter_by(id=zone_id).first()
    if not zone:
        return jsonify({'error': 'Zone not found'}), 404
        
    preds = Prediction.query.filter_by(zone_id=zone_id).order_by(Prediction.time_offset.asc()).all()
    return jsonify({
        'zone': zone.to_dict(),
        'predictions': [p.to_dict() for p in preds]
    })
