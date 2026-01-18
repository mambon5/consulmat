from flask import Blueprint, render_template
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@login_required
def admin_panel():
    if current_user.role != "admin":
        return "No autorizado", 403
    return render_template("create_admin.html")
