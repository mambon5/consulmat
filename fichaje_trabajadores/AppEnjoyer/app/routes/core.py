from flask import Blueprint, session, redirect, request, url_for

core_bp = Blueprint('core', __name__)

@core_bp.route('/set_language/<lang>')
def set_language(lang):
    if lang in ['es', 'ca', 'en']:
        session['language'] = lang
    return redirect(request.referrer or url_for('fichajes.index'))
