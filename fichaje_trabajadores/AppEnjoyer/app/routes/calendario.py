from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user
from app.models import EventoLaboral, HorarioLaboral, Treballador
from sqlalchemy.orm import joinedload
from app import db
from datetime import datetime, date
from calendar import monthrange
from zoneinfo import ZoneInfo

calendario_bp = Blueprint("calendario", __name__)

@calendario_bp.route("/calendario-laboral")
@login_required
def calendario_laboral():
    eventos = [
    {"title": "Trabajo", "start": "2025-09-03T09:00:00", "end": "2025-09-03T17:00:00", "color": "#1976d2"},
    {"title": "Festivo Nacional", "start": "2025-10-12", "allDay": True, "color": "#e53935"},
]
    treballador_id = request.args.get('treballador_id', type=int)

    # Si es admin y selecciona trabajador, muestra ese calendario
    if current_user.role == 'admin':
        # Si no se selecciona, muestra el primero
        if not treballador_id:
            treballador = Treballador.query.first()
        else:
            treballador = Treballador.query.get(treballador_id)
        # Para el desplegable de selección
        treballadors = Treballador.query.all()
    else:
        # Si es trabajador, solo el suyo
        treballador = current_user.treballador
        treballadors = None

    if treballador:
        eventos_db = EventoLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
        horarios_db = HorarioLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
    else:
        eventos_db = []
        horarios_db = []

    # Eventos puntuales (festivos y días especiales)
    for evento in eventos_db:
        color = "#1976d2"  # blau = treball
        if "festivo" in evento.tipo_evento:
            color = "#e53935"  # vermell = festiu
        elif evento.tipo_evento == "vacances":
            color = "#43a047"  # verd = vacances
        elif evento.tipo_evento == "baixa_medica":
            color = "#fb8c00"  # taronja = baixa
        elif evento.tipo_evento == "assumptes_propis":
            color = "#6d6d6d"  # gris = assumptes propis
        elif evento.tipo_evento == "teletreball":
            color = "#1e88e5"  # blau clar = teletreball

        # 🔹 Si no està aprovada, afegir marcador visual
        title = evento.tipo_evento.replace('_', ' ').capitalize()
        if not evento.aprovada:
            title += " (pendent)"

        eventos.append({
            "id": evento.id,  # 🔹 IMPORTANT: afegir l'ID per poder eliminar
            "title": title,
            "start": evento.fecha.isoformat(),
            "allDay": True if not evento.hora_inicio else False,
            "color": color,
            "extendedProps": {
                "aprovada": evento.aprovada
            }
        })


    # Horarios recurrentes (Lunes a Viernes, etc.)
    today = date.today()
    year = today.year
    month = today.month
    num_days = monthrange(year, month)[1]

    for horario in horarios_db:
        for day in range(1, num_days + 1):
            d = date(year, month, day)
            if d.weekday() == horario.dia_semana:
                eventos.append({
                    "title": "Trabajo",
                    "start": datetime.combine(d, horario.hora_inicio).isoformat(),
                    "end": datetime.combine(d, horario.hora_fin).isoformat(),
                    "color": "#1976d2"
                })



    if treballador:
        absencies = EventoLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
        tipus_abs = ['vacances', 'baixa_medica', 'assumptes_propis']

        stats = {t: 0 for t in tipus_abs}
        for a in absencies:
            if a.tipo_evento in stats:
                stats[a.tipo_evento] += 1

        # valors de referència
        lim = {'vacances': 30, 'baixa_medica': 90, 'assumptes_propis': 3}
        restants = {t: lim[t] - stats[t] for t in stats}
    else:
        stats = {}
        restants = {}

    return render_template(
        'calendari.html',
        eventos=eventos,
        treballadors=treballadors,
        treballador_seleccionat=treballador,
        stats=stats,
        restants=restants
    )

# 🔹 PÀGINA D'ADMIN: Veure i gestionar totes les sol·licituds
@calendario_bp.route('/admin/solicitudes')
@login_required
def admin_solicitudes():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    
    try:
        # Obtenir totes les sol·licituds pendents
        pendentes = EventoLaboral.query.filter_by(aprovada=False).order_by(
            EventoLaboral.id_treballador,
            EventoLaboral.tipo_evento,
            EventoLaboral.fecha
        ).all()
        
        # 🔹 AGRUPACIÓ: Agrupar dies consecutius
        solicitudes_agrupadas = []
        
        # Dict per guardar grups: (treballador_id, tipo_evento) -> lista de eventos
        grupos = {}
        
        for evento in pendentes:
            key = (evento.id_treballador, evento.tipo_evento)
            if key not in grupos:
                grupos[key] = []
            grupos[key].append(evento)
        
        # 🔹 Processar cada grup per agrupar dies consecutius
        for (treballador_id, tipo_evento), eventos in grupos.items():
            # Ordenar per data
            eventos.sort(key=lambda e: e.fecha)
            
            # Agrupar dies consecutius
            grupos_consecutivos = []
            grupo_actual = [eventos[0]]
            
            for i in range(1, len(eventos)):
                evento_anterior = eventos[i-1]
                evento_actual = eventos[i]
                
                # Calcular diferència en dies
                diff = (evento_actual.fecha - evento_anterior.fecha).days
                
                if diff == 1:
                    # Consecutiu, afegir al grup actual
                    grupo_actual.append(evento_actual)
                else:
                    # No consecutiu, guardar grup i iniciar un de nou
                    grupos_consecutivos.append(grupo_actual)
                    grupo_actual = [evento_actual]
            
            # Afegir l'últim grup
            grupos_consecutivos.append(grupo_actual)
            
            # 🔹 Crear registres agrupats
            treballador = eventos[0].treballador
            treballador_nom = treballador.user.name if treballador.user else 'Unknown'
            
            for grupo in grupos_consecutivos:
                fecha_inicio = min(g.fecha for g in grupo)
                fecha_fin = max(g.fecha for g in grupo)
                event_ids = [g.id for g in grupo]
                
                solicitudes_agrupadas.append({
                    'ids': event_ids,  # Per a approvals múltiples
                    'id_treballador': treballador_id,
                    'treballador_nom': treballador_nom,
                    'tipo_evento': tipo_evento.replace('_', ' ').capitalize(),
                    'fecha_inicio': fecha_inicio.strftime('%d/%m/%Y'),
                    'fecha_fin': fecha_fin.strftime('%d/%m/%Y'),
                    'dias': len(grupo),
                    'fecha_solicitud': min(g.fecha_solicitud for g in grupo).strftime('%d/%m/%Y %H:%M') if grupo[0].fecha_solicitud else '-'
                })
        
        return render_template('admin_solicitudes.html', solicitudes=solicitudes_agrupadas)
    except Exception as e:
        print(f"❌ Error a /admin/solicitudes: {e}")
        return jsonify({"error": str(e)}), 500

# 🔹 RUTA PER ALS ADMINS: Veure sol·licituds pendents d'aprovació
@calendario_bp.route('/api/solicitudes-pendentes', methods=['GET'])
@login_required
def solicitudes_pendentes():
    if current_user.role != 'admin':
        return jsonify({"error": "Només els admins poden veure aquest contingut"}), 403
    
    try:
        # Obtenir sol·licituds pendents d'aprovació
        pendentes = EventoLaboral.query.filter_by(aprovada=False).all()
        
        data = []
        for evento in pendentes:
            data.append({
                'id': evento.id,
                'id_treballador': evento.id_treballador,
                'treballador_nom': evento.treballador.user.name if evento.treballador.user else 'Unknown',
                'tipo_evento': evento.tipo_evento,
                'fecha': evento.fecha.isoformat(),
                'fecha_solicitud': evento.fecha_solicitud.isoformat() if evento.fecha_solicitud else None
            })
        
        return jsonify({"solicitudes": data}), 200
    except Exception as e:
        print(f"❌ Error a /api/solicitudes-pendentes: {e}")
        return jsonify({"error": str(e)}), 500

# 🔹 RUTA PER ALS ADMINS: Aprovar una sol·licitud (única)
@calendario_bp.route('/api/absencia/<int:event_id>/aprobar', methods=['POST'])
@login_required
def aprobar_absencia(event_id):
    if current_user.role != 'admin':
        return jsonify({"error": "Només els admins poden aprovar sol·licituds"}), 403
    
    try:
        evento = EventoLaboral.query.get_or_404(event_id)
        
        # Marcar com aprovada
        # Llegir el nom del treballador abans de fer commit per evitar lazy-load després
        treballador_nom = evento.treballador.user.name if evento.treballador and evento.treballador.user else 'Unknown'
        evento.aprovada = True
        evento.fecha_aprobacion = datetime.now(ZoneInfo("Europe/Madrid"))
        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": f"{evento.tipo_evento.replace('_', ' ').capitalize()} aprovat per {treballador_nom}"
        })
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error a /api/absencia/aprobar: {e}")
        return jsonify({"error": str(e)}), 500

# 🔹 RUTA PER ALS ADMINS: Aprovar múltiples sol·licituds (grup de dies consecutius)
@calendario_bp.route('/api/absencias/aprobar', methods=['POST'])
@login_required
def aprobar_absencias_grupo():
    if current_user.role != 'admin':
        return jsonify({"error": "Només els admins poden aprovar sol·licituds"}), 403
    
    data = request.get_json(silent=True)
    event_ids = data.get('ids', []) if data else []
    
    if not event_ids:
        return jsonify({"error": "No event IDs provided"}), 400
    
    try:
        eventos = EventoLaboral.query.options(
            joinedload(EventoLaboral.treballador).joinedload(Treballador.user)
        ).filter(EventoLaboral.id.in_(event_ids)).all()
        
        if not eventos:
            return jsonify({"error": "No events found"}), 404
        
        # Llegir dades abans del commit (evita lazy-load després del commit)
        tipo_evento = eventos[0].tipo_evento.replace('_', ' ').capitalize()
        treballador_nom = eventos[0].treballador.user.name if eventos[0].treballador and eventos[0].treballador.user else 'Unknown'

        # Marcar tots com aprovats
        for evento in eventos:
            evento.aprovada = True
            evento.fecha_aprobacion = datetime.now(ZoneInfo("Europe/Madrid"))

        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": f"{tipo_evento} aprovat per {treballador_nom} ({len(eventos)} dies)"
        })
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error a /api/absencias/aprobar: {e}")
        return jsonify({"error": str(e)}), 500

# 🔹 RUTA PER ALS ADMINS: Denegar una sol·licitud (única)
@calendario_bp.route('/api/absencia/<int:event_id>/denegar', methods=['DELETE'])
@login_required
def denegar_absencia(event_id):
    if current_user.role != 'admin':
        return jsonify({"error": "Només els admins poden denegar sol·licituds"}), 403
    
    try:
        evento = EventoLaboral.query.get_or_404(event_id)
        
        # Eliminar la sol·licitud si no està aprovada
        if evento.aprovada:
            return jsonify({"error": "No pots denegar una sol·licitud que ja ha estat aprovada"}), 400
        
        # Llegir nom abans d'eliminar/commit per evitar lazy-load errors
        treballador_nom = evento.treballador.user.name if evento.treballador and evento.treballador.user else 'Unknown'
        db.session.delete(evento)
        db.session.commit()
        
        return jsonify({
            "status": "ok",
            "message": f"Sol·licitud denegada per {treballador_nom}"
        })
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error a /api/absencia/denegar: {e}")
        return jsonify({"error": str(e)}), 500

# 🔹 RUTA PER ALS ADMINS: Denegar múltiples sol·licituds (grup de dies consecutius)
@calendario_bp.route('/api/absencias/denegar', methods=['DELETE'])
@login_required
def denegar_absencias_grupo():
    if current_user.role != 'admin':
        return jsonify({"status": "error", "error": "Només els admins poden denegar sol·licituds"}), 403
    
    try:
        data = request.get_json(silent=True)
        event_ids = data.get('ids', []) if data else []
        
        print(f"📥 Denegar - Data rebuda: {data}, IDs: {event_ids}")
        
        if not event_ids or len(event_ids) == 0:
            return jsonify({"status": "error", "error": "No event IDs provided"}), 400
        
        eventos = EventoLaboral.query.filter(EventoLaboral.id.in_(event_ids)).all()
        
        print(f"🔍 Eventos encontrados: {len(eventos)}")
        
        if not eventos:
            return jsonify({"status": "error", "error": "No events found"}), 404
        
        # Verificar que no estén aprovades
        if any(e.aprovada for e in eventos):
            return jsonify({"status": "error", "error": "No pots denegar sol·licituds que ja han estat aprovades"}), 400

        # Extraure valors necessaris abans d'eliminar (evitar lazy-load després del commit)
        tipo_evento = eventos[0].tipo_evento.replace('_', ' ').capitalize()
        treballador_nom = 'Unknown'
        try:
            if eventos[0].treballador and eventos[0].treballador.user and eventos[0].treballador.user.name:
                treballador_nom = eventos[0].treballador.user.name
        except Exception:
            treballador_nom = 'Unknown'

        # Eliminar totes les sol·licituds
        for evento in eventos:
            db.session.delete(evento)

        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": f"{tipo_evento} denegat per {treballador_nom} ({len(eventos)} dies)"
        })
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error a /api/absencias/denegar: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500

@calendario_bp.route('/api/absencia', methods=['POST'])
@login_required
def crear_absencia():
    if not current_user.treballador:
        return jsonify({"error": "No tens un perfil de treballador associat. Contacta amb l'administrador."}), 400
    
    data = request.get_json(silent=True)
    if not data or 'fecha' not in data or 'tipo_evento' not in data:
        return jsonify({"error": "Falten dades (fecha o tipo_evento)"}), 400

    try:
        fecha = datetime.strptime(data['fecha'][:10], '%Y-%m-%d').date()
        tipo_evento = data['tipo_evento']

        # 🔹 VALIDACIÓ: Verificar que hi ha dies disponibles
        # Els límits de dies per tipus d'absència
        lim = {'vacances': 30, 'baixa_medica': 90, 'assumptes_propis': 3}
        
        if tipo_evento in lim:
            # Contar els dies ja sol·licitats (tant pendents com aprovats compten pel límit)
            absencies = EventoLaboral.query.filter_by(
                id_treballador=current_user.treballador.id_treballador,
                tipo_evento=tipo_evento
            ).all()
            dias_utilizados = len(absencies)
            dias_disponibles = lim[tipo_evento] - dias_utilizados
            
            if dias_disponibles <= 0:
                return jsonify({
                    "error": f"No tens dies disponibles de {tipo_evento.replace('_', ' ')}. S'ha exhaurit el límit de {lim[tipo_evento]} dies."
                }), 400

        # ⚙️ teleworking és compatible amb altres absències
        if tipo_evento != 'teletreball':
            existent = EventoLaboral.query.filter_by(
                id_treballador=current_user.treballador.id_treballador,
                fecha=fecha
            ).filter(EventoLaboral.tipo_evento != 'teletreball').first()
            if existent:
                return jsonify({"error": "Ja existeix una absència per aquest dia"}), 400
        
        if tipo_evento == 'teletreball':
            existent = EventoLaboral.query.filter_by(
                id_treballador=current_user.treballador.id_treballador,
                fecha=fecha
            ).filter(EventoLaboral.tipo_evento == 'teletreball').first()
            if existent:
                return jsonify({"error": "Ja existeix un teletreball per aquest dia"}), 400

        # 🔹 NOVA LÓGICA: crear absències com a pendents d'aprovació
        # Necessites aprovació per: absències i teletreball
        # NO necessites aprovació: festius (son automàtics)
        require_approval = tipo_evento in ['vacances', 'baixa_medica', 'assumptes_propis', 'teletreball']
        
        dia = EventoLaboral(
            id_treballador=current_user.treballador.id_treballador,
            id_comunitat=data.get('id_comunitat', 1),
            fecha=fecha,
            tipo_evento=tipo_evento,
            aprovada=not require_approval  # False per absències, True per festius
        )
        db.session.add(dia)
        db.session.commit()
        
        status_msg = "pendient d'aprovació" if require_approval else "afegit"
        return jsonify({"status": "ok", "message": f"{tipo_evento.capitalize()} {status_msg} per {fecha}"})
    except Exception as e:
        db.session.rollback()
        print("❌ Error a /api/absencia:", e)
        return jsonify({"error": str(e)}), 500

@calendario_bp.route('/api/absencia/<int:event_id>', methods=['DELETE'])
@login_required
def eliminar_absencia(event_id):
    if not current_user.treballador:
        return jsonify({"error": "No tens un perfil de treballador associat."}), 400
    
    evento = EventoLaboral.query.get_or_404(event_id)
    
    # 🔹 Verificar que és el treballador propietari de l'absència
    if evento.id_treballador != current_user.treballador.id_treballador:
        return jsonify({"status": "error", "message": "No autoritzat"}), 403
    
    # 🔹 Si l'absència ja està aprovada, el treballador no la pot eliminar (només admins)
    if evento.aprovada and current_user.role != 'admin':
        return jsonify({"status": "error", "message": "No pots eliminar una sol·licitud que ja ha estat aprovada"}), 400
    
    # 🔹 Permetre eliminar qualsevol tipus d'absència (vacances, baixa, assumptes, teletreball)
    if evento.tipo_evento not in ['vacances', 'baixa_medica', 'assumptes_propis', 'teletreball']:
        return jsonify({"status": "error", "message": "No pots eliminar aquest tipus d'event"}), 400
    
    try:
        tipo = evento.tipo_evento.replace('_', ' ')
        db.session.delete(evento)
        db.session.commit()
        return jsonify({"status": "ok", "message": f"{tipo.capitalize()} eliminada correctament"})
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error a /api/absencia DELETE: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔹 Mantenir ruta antiga per compatibilitat
@calendario_bp.route('/api/vacances/<int:event_id>', methods=['DELETE'])
@login_required
def eliminar_vacances(event_id):
    return eliminar_absencia(event_id)

@calendario_bp.route("/calendari")
@login_required
def calendari():
    treballador_id = request.args.get('treballador_id', type=int)

    # Si es admin y selecciona trabajador, muestra ese calendario
    if current_user.role == 'admin':
        # Si no se selecciona, muestra el primero
        if not treballador_id:
            treballador = Treballador.query.first()
        else:
            treballador = Treballador.query.get(treballador_id)
        # Para el desplegable de selección
        treballadors = Treballador.query.all()
    else:
        # Si es trabajador, solo el suyo
        treballador = current_user.treballador
        treballadors = None

    eventos = []

    if treballador:
        eventos_db = EventoLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
        horarios_db = HorarioLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
    else:
        eventos_db = []
        horarios_db = []

    # Eventos puntuales (festivos y días especiales)
    for evento in eventos_db:
        color = "#1976d2"  # blau = treball
        if "festivo" in evento.tipo_evento:
            color = "#e53935"  # vermell = festiu
        elif evento.tipo_evento == "vacances":
            color = "#43a047"  # verd = vacances
        elif evento.tipo_evento == "baixa_medica":
            color = "#fb8c00"  # taronja = baixa
        elif evento.tipo_evento == "assumptes_propis":
            color = "#6d6d6d"  # gris = assumptes propis
        elif evento.tipo_evento == "teletreball":
            color = "#1e88e5"  # blau clar = teletreball

        # 🔹 Si no està aprovada, afegir marcador visual
        title = evento.tipo_evento.replace('_', ' ').capitalize()
        if not evento.aprovada:
            title += " (pendent)"

        eventos.append({
            "id": evento.id,  # 🔹 IMPORTANT: afegir l'ID per poder eliminar
            "title": title,
            "start": evento.fecha.isoformat(),
            "allDay": True if not evento.hora_inicio else False,
            "color": color,
            "extendedProps": {
                "aprovada": evento.aprovada
            }
        })

    # Horarios recurrentes (Lunes a Viernes, etc.)
    today = date.today()
    year = today.year
    month = today.month
    num_days = monthrange(year, month)[1]

    for horario in horarios_db:
        for day in range(1, num_days + 1):
            d = date(year, month, day)
            if d.weekday() == horario.dia_semana:
                eventos.append({
                    "title": "Trabajo",
                    "start": datetime.combine(d, horario.hora_inicio).isoformat(),
                    "end": datetime.combine(d, horario.hora_fin).isoformat(),
                    "color": "#1976d2"
                })

    if treballador:
        absencies = EventoLaboral.query.filter_by(id_treballador=treballador.id_treballador).all()
        tipus_abs = ['vacances', 'baixa_medica', 'assumptes_propis']

        stats = {t: 0 for t in tipus_abs}
        for a in absencies:
            if a.tipo_evento in stats:
                stats[a.tipo_evento] += 1

        # valors de referència
        lim = {'vacances': 30, 'baixa_medica': 90, 'assumptes_propis': 3}
        restants = {t: lim[t] - stats[t] for t in stats}
    else:
        stats = {}
        restants = {}

    return render_template(
        'calendari.html',
        eventos=eventos,
        treballadors=treballadors,
        treballador_seleccionat=treballador,
        stats=stats,
        restants=restants
    )
