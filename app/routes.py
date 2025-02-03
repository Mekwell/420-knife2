from flask import Blueprint, redirect, request, session, url_for, render_template
from app import db
from app.models import User
from app.utils import get_esi_data, esi_security, SCOPES

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/login')
def login():
    auth_url = esi_security.get_auth_uri(scopes=SCOPES)
    return redirect(auth_url)

@bp.route('/callback')
def callback():
    code = request.args.get('code')
    tokens = esi_security.auth(code)
    char_info = esi_security.verify()
    
    user = User.query.filter_by(character_id=char_info['sub'].split(':')[-1]).first()
    if not user:
        user = User(
            character_id=char_info['sub'].split(':')[-1],
            name=char_info['name'],
            access_token=tokens['access_token'],
            refresh_token=tokens['refresh_token']
        )
        db.session.add(user)
    else:
        user.access_token = tokens['access_token']
        user.refresh_token = tokens['refresh_token']
    
    db.session.commit()
    session['character_id'] = user.character_id
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard')
def dashboard():
    char_id = session.get('character_id')
    if not char_id:
        return redirect(url_for('main.index'))
    
    data = get_esi_data(char_id)
    return render_template('dashboard.html', data=data)

@bp.route('/recruiter')
def recruiter_view():
    users = User.query.all()
    return render_template('recruiter.html', users=users)

@bp.route('/user/<int:char_id>')
def user_profile(char_id):
    user = User.query.get_or_404(char_id)
    data = get_esi_data(char_id)
    return render_template('profile.html', user=user, data=data)
