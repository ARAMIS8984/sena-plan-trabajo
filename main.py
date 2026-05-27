import streamlit as st
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
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9hZ3BjbHNpaW15eG5ma2Vlam9wIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk4NDcwMDAsImV4cCI6MjA5NTQyMzAwMH0.zy4WyMpB3EsBTAigTcPya1zat5myEFcOyLnsvqbP72A"

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

# ── CLIENTE SUPABASE ─────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    from supabase import create_client
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def verificar_usuario(cedula, pin):
    """Verifica credenciales y retorna datos del usuario o None"""
    try:
        sb = get_supabase()
        res = sb.table('usuarios').select('*').eq('cedula', cedula).execute()
        data = res.data
        if not data:
            return None, "Cédula no registrada."
        usuario = data[0]
        if not usuario['activo']:
            return None, "Tu acceso está desactivado. Contacta al administrador."
        vencimiento = datetime.strptime(usuario['fecha_vencimiento'], '%Y-%m-%d').date()
        if vencimiento < date.today():
            return None, f"Tu suscripción venció el {vencimiento.strftime('%d/%m/%Y')}. Renueva para continuar."
        if usuario['pin'] != pin and usuario['cedula'] != pin:
            return None, "PIN incorrecto."
        return usuario, None
    except Exception as e:
        return None, f"Error de conexión: {str(e)[:50]}"

def agregar_usuario(cedula, pin, nombre, paquete, dias):
    """Agrega un nuevo usuario"""
    from datetime import timedelta
    vencimiento = (date.today() + timedelta(days=dias)).isoformat()
    herramientas = ['todas'] if paquete == 'completo' else ['plan_concertado']
    try:
        sb = get_supabase()
        sb.table('usuarios').insert({
            "cedula": cedula, "pin": pin, "nombre": nombre.upper(),
            "paquete": paquete, "herramientas": herramientas,
            "fecha_vencimiento": vencimiento, "activo": True
        }).execute()
        return True
    except:
        return False

def listar_usuarios():
    """Lista todos los usuarios no admin"""
    try:
        sb = get_supabase()
        res = sb.table('usuarios').select('*').neq('paquete', 'admin').order('nombre').execute()
        return res.data
    except:
        return []

def toggle_usuario(cedula, activo):
    """Activa o desactiva un usuario"""
    try:
        sb = get_supabase()
        sb.table('usuarios').update({'activo': activo}).eq('cedula', cedula).execute()
        return True
    except:
        return False

def renovar_usuario(cedula, dias):
    """Renueva la suscripción de un usuario"""
    from datetime import timedelta
    nueva_fecha = (date.today() + timedelta(days=dias)).isoformat()
    try:
        sb = get_supabase()
        sb.table('usuarios').update({'fecha_vencimiento': nueva_fecha, 'activo': True}).eq('cedula', cedula).execute()
        return True
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
      <div class="login-sub">Centro Nacional Colombo Alemán<br/>Ingresa tu número de cédula para continuar</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        cedula = st.text_input("Número de cédula", placeholder="Ej. 1045678901", key="login_cedula")

        if st.button("🔐 Ingresar"):
            if not cedula:
                st.error("Ingresa tu número de cédula.")
            else:
                with st.spinner("Verificando..."):
                    usuario, error = verificar_usuario(cedula.strip(), cedula.strip())
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
            "nombre": "Plan Concertado",
            "desc": "Genera planes concertados para todos tus aprendices",
            "pagina": "plan_concertado",
            "url": None
        },
        {
            "id": "llamados",
            "nombre": "Llamados de Atención",
            "desc": "Registra y genera llamados de atención",
            "pagina": "llamados",
            "url": "https://aramis8984.github.io/llamado-atencion-sena"
        },
        {
            "id": "actas",
            "nombre": "Actas",
            "desc": "Genera actas de inicio, seguimiento, cierre y más",
            "pagina": "actas",
            "url": None
        },
    ]

    for h in HERRAMIENTAS:
        tiene_acceso = tiene_todo or h['id'] in herramientas
        if tiene_acceso:
            if h.get('url'):
                st.markdown(f"""
                <a href="{h['url']}" target="_blank" style="
                    display:block;
                    background:linear-gradient(135deg,#006633,#009944);
                    color:white;
                    text-decoration:none;
                    padding:0.65rem 1rem;
                    border-radius:10px;
                    font-weight:600;
                    font-size:0.9rem;
                    margin-bottom:0.5rem;
                    box-shadow:0 4px 20px rgba(0,100,50,0.4);
                    text-align:center;
                ">{h['nombre']} — {h['desc']} ↗</a>
                """, unsafe_allow_html=True)
            else:
                if st.button(f"{h['nombre']} — {h['desc']}", key=f"btn_{h['id']}",
                            use_container_width=True):
                    st.session_state.pagina = h['pagina']
                    st.rerun()
        else:
            st.markdown(f"""
            <div class="tool-locked">
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
            new_cedula  = c1.text_input("Cédula", key="new_cedula")
            new_nombre  = c2.text_input("Nombre completo", key="new_nombre")
            c3, c4 = st.columns(2)
            new_paquete = c3.selectbox("Paquete", ["basico", "completo"], key="new_paquete",
                                        format_func=lambda x: "📦 Básico" if x=="basico" else "⭐ Completo")
            new_dias = c4.number_input("Días de acceso", min_value=1, max_value=365, value=30, key="new_dias")
            if new_cedula:
                st.caption(f"🔑 El acceso será con la cédula: {new_cedula}")
            if st.button("➕ Agregar instructor", key="btn_agregar"):
                if not new_cedula or not new_nombre:
                    st.error("Completa todos los campos.")
                else:
                    ok = agregar_usuario(new_cedula, new_cedula, new_nombre, new_paquete, new_dias)
                    if ok:
                        st.success(f"✅ {new_nombre} agregado. Acceso con cédula: {new_cedula}")
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
    st.markdown("""
    <style>
    div[data-testid="stButton"]:first-of-type button {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(0,200,100,0.4) !important;
        color: #a5d6a7 !important;
        font-size: 0.85rem !important;
        padding: 0.4rem 1rem !important;
        width: auto !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← Volver al menú", key="back_plan"):
            st.session_state.pagina = 'menu'
            st.rerun()
    st.divider()
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
    col_back, _ = st.columns([1, 4])
    with col_back:
        if st.button("← Volver al menú", key=f"back_{st.session_state.pagina}"):
            st.session_state.pagina = 'menu'
            st.rerun()
    st.divider()
    st.markdown(f"""
    <div style="text-align:center;padding:3rem;background:rgba(255,255,255,0.03);
    border:1px solid rgba(0,200,100,0.15);border-radius:16px;margin-top:1rem;">
      <div style="font-size:3rem;">{icon}</div>
      <h2 style="color:white;">{nombre}</h2>
      <p style="color:#a5d6a7;">Esta herramienta está en desarrollo.<br>Próximamente disponible. 🚀</p>
    </div>
    """, unsafe_allow_html=True)
