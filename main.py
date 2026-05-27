import streamlit as st
import requests
from datetime import date, datetime
import base64, os

st.set_page_config(
    page_title="Herramientas SENA",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CONFIGURACIÓN SUPABASE ────────────────────────────────────────
SUPABASE_URL = "https://oagpclsiimyxnfkeejop.supabase.co"
SUPABASE_KEY = "sb_publishable_hdV4ZfWNr13bNN8WDdHLYg_5qCQpAK1"
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# ── LOGO ──────────────────────────────────────────────────────────
def get_logo_b64():
    for path in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_sena.png"),
        "logo_sena.png",
    ]:
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return ""

logo_b64 = get_logo_b64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="height:70px;background:white;border-radius:8px;padding:5px;">' if logo_b64 else ""

# ── CSS ───────────────────────────────────────────────────────────
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"]{{
    background-color:#0a1628;
    background-image:
        radial-gradient(ellipse at 25% 40%, rgba(0,102,51,0.35) 0%, transparent 60%),
        radial-gradient(ellipse at 75% 70%, rgba(0,61,31,0.4) 0%, transparent 55%);
    background-size:cover;
    background-attachment:fixed;
}}
[data-testid="stHeader"]{{background:rgba(10,22,40,0.95)!important;backdrop-filter:blur(10px);border-bottom:1px solid rgba(0,153,68,0.2);}}
[data-testid="block-container"]{{padding-top:2rem!important;}}
.login-card{{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(0,200,100,0.2);
    border-radius:20px;
    padding:2.5rem;
    box-shadow:0 8px 32px rgba(0,0,0,0.4);
    backdrop-filter:blur(12px);
    max-width:420px;
    margin:0 auto;
}}
.logo-area{{text-align:center;margin-bottom:1.5rem;}}
.login-title{{color:white;font-size:1.6rem;font-weight:700;text-align:center;margin:0.5rem 0;}}
.login-sub{{color:#a5d6a7;font-size:.85rem;text-align:center;margin-bottom:1.5rem;}}
.tool-card{{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(0,200,100,0.2);
    border-radius:14px;
    padding:1.2rem 1.5rem;
    margin-bottom:0.8rem;
    cursor:pointer;
    transition:all 0.2s;
    display:flex;
    align-items:center;
    gap:1rem;
}}
.tool-card:hover{{border-color:#009944;background:rgba(0,153,68,0.1);}}
.tool-locked{{
    background:rgba(255,255,255,0.02);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:14px;
    padding:1.2rem 1.5rem;
    margin-bottom:0.8rem;
    opacity:0.4;
    display:flex;
    align-items:center;
    gap:1rem;
}}
.tool-icon{{font-size:1.8rem;}}
.tool-name{{color:white;font-weight:600;font-size:1rem;}}
.tool-desc{{color:#a5d6a7;font-size:.8rem;}}
.tool-lock{{color:#666;font-size:1rem;margin-left:auto;}}
.welcome-header{{
    background:linear-gradient(135deg,rgba(0,77,38,0.95),rgba(0,120,60,0.95));
    border:1px solid rgba(0,200,100,0.3);
    border-radius:16px;
    padding:1.2rem 1.5rem;
    margin-bottom:1.5rem;
    display:flex;
    align-items:center;
    gap:1rem;
    box-shadow:0 4px 20px rgba(0,0,0,0.3);
}}
.welcome-text h2{{color:white;margin:0;font-size:1.2rem;}}
.welcome-text p{{color:#a5d6a7;margin:0;font-size:.85rem;}}
.badge-basico{{background:rgba(0,153,68,0.3);color:#4caf50;padding:3px 10px;border-radius:20px;font-size:.75rem;border:1px solid rgba(0,200,100,0.3);}}
.badge-completo{{background:rgba(255,180,0,0.2);color:#ffd54f;padding:3px 10px;border-radius:20px;font-size:.75rem;border:1px solid rgba(255,180,0,0.3);}}
.badge-admin{{background:rgba(255,100,100,0.2);color:#ef9a9a;padding:3px 10px;border-radius:20px;font-size:.75rem;border:1px solid rgba(255,100,100,0.3);}}
[data-testid="stTextInput"] input{{
    background:rgba(255,255,255,0.07)!important;
    border:1px solid rgba(0,200,100,0.25)!important;
    border-radius:8px!important;
    color:#10941a!important;
}}
.stButton>button{{
    background:linear-gradient(135deg,#006633,#009944)!important;
    color:white!important;
    border:none!important;
    border-radius:10px!important;
    font-weight:600!important;
    box-shadow:0 4px 20px rgba(0,100,50,0.4)!important;
    width:100%!important;
}}
.admin-card{{
    background:rgba(255,100,100,0.05);
    border:1px solid rgba(255,100,100,0.2);
    border-radius:14px;
    padding:1.2rem 1.5rem;
    margin-bottom:1rem;
}}
.admin-title{{color:#ef9a9a;font-weight:700;font-size:.85rem;text-transform:uppercase;letter-spacing:.06em;margin-bottom:.8rem;}}
</style>
""", unsafe_allow_html=True)

# ── FUNCIONES SUPABASE ────────────────────────────────────────────
def verificar_usuario(cedula, pin):
    """Verifica credenciales y retorna datos del usuario o None"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/usuarios?cedula=eq.{cedula}&select=*"
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        if not data:
            return None, "Cédula no registrada."
        usuario = data[0]
        if not usuario['activo']:
            return None, "Tu acceso está desactivado. Contacta al administrador."
        vencimiento = datetime.strptime(usuario['fecha_vencimiento'], '%Y-%m-%d').date()
        if vencimiento < date.today():
            return None, f"Tu suscripción venció el {vencimiento.strftime('%d/%m/%Y')}. Renueva para continuar."
        if usuario['pin'] != pin:
            return None, "PIN incorrecto."
        return usuario, None
    except Exception as e:
        return None, f"Error de conexión. Intenta de nuevo."

def agregar_usuario(cedula, pin, nombre, paquete, dias):
    """Agrega un nuevo usuario"""
    from datetime import timedelta
    vencimiento = (date.today() + timedelta(days=dias)).isoformat()
    herramientas = '{"todas"}' if paquete == 'completo' else '{"plan_concertado"}'
    payload = {
        "cedula": cedula,
        "pin": pin,
        "nombre": nombre.upper(),
        "paquete": paquete,
        "herramientas": herramientas,
        "fecha_vencimiento": vencimiento,
        "activo": True
    }
    try:
        url = f"{SUPABASE_URL}/rest/v1/usuarios"
        r = requests.post(url, headers={**HEADERS, "Prefer": "return=minimal"}, json=payload, timeout=10)
        return r.status_code in (200, 201)
    except:
        return False

def listar_usuarios():
    """Lista todos los usuarios no admin"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/usuarios?paquete=neq.admin&select=*&order=nombre.asc"
        r = requests.get(url, headers=HEADERS, timeout=10)
        return r.json()
    except:
        return []

def toggle_usuario(cedula, activo):
    """Activa o desactiva un usuario"""
    try:
        url = f"{SUPABASE_URL}/rest/v1/usuarios?cedula=eq.{cedula}"
        r = requests.patch(url, headers={**HEADERS, "Prefer": "return=minimal"},
                          json={"activo": activo}, timeout=10)
        return r.status_code in (200, 204)
    except:
        return False

def renovar_usuario(cedula, dias):
    """Renueva la suscripción de un usuario"""
    from datetime import timedelta
    nueva_fecha = (date.today() + timedelta(days=dias)).isoformat()
    try:
        url = f"{SUPABASE_URL}/rest/v1/usuarios?cedula=eq.{cedula}"
        r = requests.patch(url, headers={**HEADERS, "Prefer": "return=minimal"},
                          json={"fecha_vencimiento": nueva_fecha, "activo": True}, timeout=10)
        return r.status_code in (200, 204)
    except:
        return False

# ── ESTADO DE SESIÓN ──────────────────────────────────────────────
if 'usuario' not in st.session_state:
    st.session_state.usuario = None
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'

# ════════════════════════════════════════════════════════════════
# PANTALLA DE LOGIN
# ════════════════════════════════════════════════════════════════
if st.session_state.pagina == 'login':
    st.markdown(f"""
    <div class="login-card">
      <div class="logo-area">{logo_html}</div>
      <div class="login-title">Herramientas SENA</div>
      <div class="login-sub">Centro Nacional Colombo Alemán<br/>Ingresa tus credenciales para continuar</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cedula = st.text_input("Número de cédula", placeholder="Ej. 1045678901", key="login_cedula")
        pin    = st.text_input("PIN de 4 dígitos", placeholder="••••", type="password", max_chars=4, key="login_pin")

        if st.button("🔐 Ingresar"):
            if not cedula or not pin:
                st.error("Ingresa tu cédula y PIN.")
            else:
                with st.spinner("Verificando..."):
                    usuario, error = verificar_usuario(cedula.strip(), pin.strip())
                if error:
                    st.error(f"❌ {error}")
                else:
                    st.session_state.usuario = usuario
                    st.session_state.pagina = 'menu'
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("¿No tienes acceso? Contacta al administrador del sistema.")

# ════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ════════════════════════════════════════════════════════════════
elif st.session_state.pagina == 'menu':
    u = st.session_state.usuario
    paquete = u['paquete']
    herramientas = u['herramientas']
    tiene_todo = paquete in ('admin', 'completo') or 'todas' in herramientas
    vencimiento = datetime.strptime(u['fecha_vencimiento'], '%Y-%m-%d').date()
    dias_restantes = (vencimiento - date.today()).days

    # Badge de paquete
    if paquete == 'admin':
        badge = '<span class="badge-admin">👑 Administrador</span>'
    elif paquete == 'completo':
        badge = '<span class="badge-completo">⭐ Paquete Completo</span>'
    else:
        badge = '<span class="badge-basico">📦 Paquete Básico</span>'

    st.markdown(f"""
    <div class="welcome-header">
      <div>{logo_html}</div>
      <div class="welcome-text">
        <h2>Bienvenido, {u['nombre'].split()[0].title()}</h2>
        <p>{badge} &nbsp;·&nbsp; Vence: {vencimiento.strftime('%d/%m/%Y')} ({dias_restantes} días)</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🛠️ Mis Herramientas")

    # ── HERRAMIENTAS DISPONIBLES ──────────────────────────────────
    HERRAMIENTAS = [
        {
            "id": "plan_concertado",
            "icon": "📋",
            "nombre": "Plan Concertado",
            "desc": "Genera planes concertados para todos tus aprendices",
            "pagina": "plan_concertado"
        },
        {
            "id": "guias",
            "icon": "📚",
            "nombre": "Guías de Aprendizaje",
            "desc": "Crea guías de aprendizaje personalizadas",
            "pagina": "guias"
        },
        {
            "id": "informe",
            "icon": "📊",
            "nombre": "Informe Contractual",
            "desc": "Genera informes contractuales de seguimiento",
            "pagina": "informe"
        },
        {
            "id": "llamados",
            "icon": "⚠️",
            "nombre": "Llamados de Atención",
            "desc": "Registra y genera llamados de atención",
            "pagina": "llamados"
        },
        {
            "id": "actas",
            "icon": "📄",
            "nombre": "Actas",
            "desc": "Genera actas de inicio, seguimiento, cierre y más",
            "pagina": "actas"
        },
    ]

    for h in HERRAMIENTAS:
        tiene_acceso = tiene_todo or h['id'] in herramientas
        if tiene_acceso:
            if st.button(f"{h['icon']}  {h['nombre']} — {h['desc']}", key=f"btn_{h['id']}",
                        use_container_width=True):
                st.session_state.pagina = h['pagina']
                st.rerun()
        else:
            st.markdown(f"""
            <div class="tool-locked">
              <span class="tool-icon">{h['icon']}</span>
              <div>
                <div class="tool-name">{h['nombre']}</div>
                <div class="tool-desc">{h['desc']}</div>
              </div>
              <span class="tool-lock">🔒 No incluido en tu plan</span>
            </div>
            """, unsafe_allow_html=True)

    # ── PANEL ADMIN ───────────────────────────────────────────────
    if paquete == 'admin':
        st.markdown("---")
        st.markdown("### 👑 Panel de Administración")

        tab1, tab2, tab3 = st.tabs(["➕ Agregar instructor", "👥 Ver instructores", "🔄 Renovar / Desactivar"])

        with tab1:
            st.markdown('<div class="admin-card"><div class="admin-title">Nuevo instructor</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            new_cedula = c1.text_input("Cédula", key="new_cedula")
            new_pin    = c2.text_input("PIN (4 dígitos)", key="new_pin", max_chars=4)
            new_nombre = st.text_input("Nombre completo", key="new_nombre")
            c3, c4 = st.columns(2)
            new_paquete = c3.selectbox("Paquete", ["basico", "completo"], key="new_paquete",
                                        format_func=lambda x: "📦 Básico" if x=="basico" else "⭐ Completo")
            new_dias = c4.number_input("Días de acceso", min_value=1, max_value=365, value=30, key="new_dias")
            if st.button("➕ Agregar instructor", key="btn_agregar"):
                if not new_cedula or not new_pin or not new_nombre:
                    st.error("Completa todos los campos.")
                elif len(new_pin) != 4 or not new_pin.isdigit():
                    st.error("El PIN debe ser exactamente 4 dígitos.")
                else:
                    ok = agregar_usuario(new_cedula, new_pin, new_nombre, new_paquete, new_dias)
                    if ok:
                        st.success(f"✅ {new_nombre} agregado con acceso por {new_dias} días.")
                    else:
                        st.error("Error al agregar. La cédula puede estar ya registrada.")
            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            usuarios = listar_usuarios()
            if not usuarios:
                st.info("No hay instructores registrados.")
            else:
                st.caption(f"{len(usuarios)} instructor(es) registrado(s)")
                for usr in usuarios:
                    venc = datetime.strptime(usr['fecha_vencimiento'], '%Y-%m-%d').date()
                    dias = (venc - date.today()).days
                    estado = "✅ Activo" if usr['activo'] and dias > 0 else "❌ Inactivo/Vencido"
                    paq_icon = "⭐" if usr['paquete'] == 'completo' else "📦"
                    st.markdown(f"""
                    **{usr['nombre']}** · CC {usr['cedula']} · {paq_icon} {usr['paquete'].title()}
                    {estado} · Vence: {venc.strftime('%d/%m/%Y')} ({dias} días)
                    """)
                    st.divider()

        with tab3:
            usuarios = listar_usuarios()
            if usuarios:
                cedulas = {f"{u['nombre']} (CC {u['cedula']})": u['cedula'] for u in usuarios}
                sel = st.selectbox("Selecciona instructor", list(cedulas.keys()), key="sel_usr")
                cedula_sel = cedulas[sel]
                usr_sel = next(u for u in usuarios if u['cedula'] == cedula_sel)

                c1, c2 = st.columns(2)
                dias_renovar = c1.number_input("Días a renovar", min_value=1, max_value=365, value=30, key="dias_ren")
                if c1.button("🔄 Renovar", key="btn_renovar"):
                    if renovar_usuario(cedula_sel, dias_renovar):
                        st.success(f"✅ Acceso renovado por {dias_renovar} días.")
                        st.rerun()

                estado_actual = usr_sel['activo']
                label = "🔴 Desactivar" if estado_actual else "🟢 Activar"
                if c2.button(label, key="btn_toggle"):
                    if toggle_usuario(cedula_sel, not estado_actual):
                        st.success("✅ Estado actualizado.")
                        st.rerun()

    # ── CERRAR SESIÓN ─────────────────────────────────────────────
    st.markdown("---")
    if st.button("🚪 Cerrar sesión", key="logout"):
        st.session_state.usuario = None
        st.session_state.pagina  = 'login'
        st.rerun()

# ════════════════════════════════════════════════════════════════
# HERRAMIENTA: PLAN CONCERTADO
# ════════════════════════════════════════════════════════════════
elif st.session_state.pagina == 'plan_concertado':
    if st.button("← Volver al menú"):
        st.session_state.pagina = 'menu'
        st.rerun()
    # Importar y ejecutar el Plan Concertado
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py')).read())

# ════════════════════════════════════════════════════════════════
# HERRAMIENTAS EN DESARROLLO
# ════════════════════════════════════════════════════════════════
elif st.session_state.pagina in ('guias', 'informe', 'llamados', 'actas'):
    nombres = {
        'guias':    ('📚', 'Guías de Aprendizaje'),
        'informe':  ('📊', 'Informe Contractual'),
        'llamados': ('⚠️', 'Llamados de Atención'),
        'actas':    ('📄', 'Actas'),
    }
    icon, nombre = nombres[st.session_state.pagina]
    if st.button("← Volver al menú"):
        st.session_state.pagina = 'menu'
        st.rerun()
    st.markdown(f"""
    <div style="text-align:center;padding:3rem;background:rgba(255,255,255,0.03);
    border:1px solid rgba(0,200,100,0.15);border-radius:16px;margin-top:1rem;">
      <div style="font-size:3rem;">{icon}</div>
      <h2 style="color:white;">{nombre}</h2>
      <p style="color:#a5d6a7;">Esta herramienta está en desarrollo.<br>Próximamente disponible. 🚀</p>
    </div>
    """, unsafe_allow_html=True)
