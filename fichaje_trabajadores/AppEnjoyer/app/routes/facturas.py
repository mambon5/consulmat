from flask_babel import _
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_file
from flask_login import login_required, current_user
from app.models import Factura, Comunidad
from app import db
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

facturas_bp = Blueprint("facturas", __name__)

@facturas_bp.route("/factures")
@login_required
def llistar_factures():
    if current_user.role != 'admin':
        flash(_('No tens permisos per accedir a aquesta pàgina.'), 'danger')
        return redirect(url_for('fichajes.index'))

    factures = Factura.query.order_by(Factura.id_factura.desc()).all()
    return render_template('llistat_factures.html', factures=factures)

@facturas_bp.route('/factura/<int:factura_id>/download')
@login_required
def download_factura(factura_id):
    if current_user.role != 'admin':
        flash(_('No tens permisos per descarregar factures.'), 'danger')
        return redirect(url_for('facturas.llistar_factures'))

    factura = Factura.query.get_or_404(factura_id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    y = 800
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, y, f"Factura ID: {factura.id_factura}")

    p.setFont("Helvetica", 12)
    y -= 30
    p.drawString(100, y, f"Comunitat: {factura.comunitat.nombre}")
    y -= 20
    p.drawString(100, y, f"Tipus de feina: {factura.tipus_feina}")
    y -= 20
    p.drawString(100, y, f"Document de pagament: {factura.document_de_pago}")
    y -= 20
    p.drawString(100, y, f"Règim d’impostos: {factura.regimen_impuestos or '-'}")
    # Afegeix més camps si cal

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'factura_{factura.id_factura}.pdf',
        mimetype='application/pdf'
    )

@facturas_bp.route('/create_factura', methods=['GET', 'POST'])
@login_required
def create_factura():
    if not current_user.role == 'admin':
        flash(_('No tienes permisos para crear facturas.'), 'danger')
        return redirect(url_for('fichajes.index'))

    if request.method == 'POST':
        id_comunitat = request.form.get('id_comunitat')
        tipus_feina = request.form.get('tipus_feina')
        document_de_pago = request.form.get('document_de_pago')
        regimen_impuestos = request.form.get('regimen_impostos') or None

        nova_factura = Factura(
            id_comunitat=id_comunitat,
            tipus_feina=tipus_feina,
            document_de_pago=document_de_pago,
            regimen_impostos=regimen_impuestos
        )

        db.session.add(nova_factura)
        try:
            db.session.commit()
            flash(_('Factura creada exitosamente.'), 'success')
            return redirect(url_for('facturas.llistar_factures'))
        except Exception as e:
            db.session.rollback()
            flash(_('Error al crear la factura.'), 'danger')
            return redirect(url_for('facturas.create_factura'))

    comunitats = Comunidad.query.order_by(Comunidad.nombre.asc()).all()
    return render_template('create_factura.html', comunitats=comunitats)
