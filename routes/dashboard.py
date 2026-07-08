from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from database.models import User, Zone, Alert, Recommendation, db
from werkzeug.security import generate_password_hash

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('dashboard.login'))
    
    # Fetch current state to initialize the page before websockets kick in
    zones = Zone.query.all()
    alerts = Alert.query.filter_by(resolved=False).all()
    recs = Recommendation.query.all()
    
    # Calculate attendance
    attendance = sum(z.current_crowd for z in zones if z.zone_type == 'stand')
    
    return render_template(
        'index.html',
        username=session['username'],
        role=session['role'],
        zones=zones,
        alerts=alerts,
        recs=recs,
        attendance=attendance
    )

@dashboard_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard.index'))
            
        flash('Invalid username or password', 'error')
        
    return render_template('login.html')

@dashboard_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dashboard.login'))

@dashboard_bp.route('/seed-user')
def seed_user():
    """
    Convenience endpoint to seed initial roles for hackathon testing.
    """
    if User.query.first() is not None:
        return "Users already seeded."
        
    roles = ['Admin', 'Operator', 'Security', 'Volunteer', 'Medical']
    for role in roles:
        u = User(username=role.lower(), role=role)
        u.set_password('worldcup2026')
        db.session.add(u)
    db.session.commit()
    return "Demo users seeded. Credentials: admin/worldcup2026, operator/worldcup2026, etc."
