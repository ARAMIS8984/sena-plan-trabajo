import streamlit as st
import pandas as pd
import openpyxl
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── CONFIGURACIÓN ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Plan de Trabajo SENA",
    page_icon="🎓",
    layout="wide"
)

# ── ESTILOS CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #006633 0%, #009944 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.6rem; }
    .main-header p  { color: #ccffcc; margin: 4px 0 0; font-size: 0.9rem; }
    .section-box {
        background: #f8fffe;
        border: 1px solid #c8e6c9;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .section-title {
        color: #006633;
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .ra-selected {
        background: #e8f5e9;
        border-left: 4px solid #006633;
        padding: 6px 10px;
        border-radius: 4px;
        margin: 4px 0;
        font-size: 0.85rem;
    }
    .aprendiz-chip {
        display: inline-block;
        background: #e8f5e9;
        color: #006633;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        margin: 2px;
        border: 1px solid #a5d6a7;
    }
    .stButton > button {
        background: #006633;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton > button:hover { background: #005522; }
    .success-box {
        background: #e8f5e9;
        border: 1px solid #66bb6a;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ── PLANEACIÓN PEDAGÓGICA ─────────────────────────────────────────
PLANEACION = {
    "INDUCCIÓN": {
        "Inducción": {
            "competencias": [{
                "nombre": "Resultado de aprendizaje de la inducción",
                "resultados": [
                    "Identificar la dinámica organizacional del SENA y el rol de la Formación Profesional Integral de acuerdo con su proyecto de vida y el desarrollo profesional"
                ],
                "actividades": [
                    "Asumir actitudes y valores en los diferentes ámbitos de formación, vida y trabajo",
                    "Reconocer la identidad institucional y los procedimientos administrativos",
                    "Incorporar a su proyecto de vida las oportunidades ofrecidas por el SENA"
                ],
                "hD": 36, "hI": 12
            }]
        }
    },
    "ANÁLISIS": {
        "CARACTERIZAR LA MATERIA PRIMA, HERRAMIENTAS Y EQUIPOS EN EL AJUSTE MANUAL DE LAS PIEZAS.": {
            "competencias": [{
                "nombre": "Pulir piezas industriales de acuerdo con técnicas manuales y mecánicas",
                "resultados": [
                    "01 Alistar materia prima e instrumentos de medición teniendo en cuenta normativa ocupacional, ambiental y procedimientos técnicos.",
                    "02 Poner a punto herramientas y equipos de banco para el ajuste manual y mecánico teniendo en cuenta procedimientos técnicos y normativa.",
                    "03 Ajustar manual y mecánicamente con herramientas y equipos de banco teniendo en cuenta procedimientos técnicos y normativas."
                ],
                "actividades": [
                    "Fundamentar conceptos y principios de metrología con instrumentos análogos.",
                    "Fundamentar conceptos y principios de trabajo con herramientas de banco.",
                    "Fundamentar conceptos y principios de ajustes y tolerancias utilizando herramientas e instrumentos de banco."
                ],
                "hD": 36, "hI": 12
            }]
        },
        "REALIZAR EL DESPIECE CORRESPONDIENTE A LAS PIEZAS DEL PROYECTO SEGÚN EL DIEDRO APROPIADO.": {
            "competencias": [{
                "nombre": "Dibujar planos mecánicos de acuerdo con normas técnicas",
                "resultados": [
                    "01 Dibujar elementos mecánicos de acuerdo con especificaciones técnicas.",
                    "Modelar componentes mecánicos en software CAD según especificaciones técnicas.",
                    "Documentar los planos según normas técnicas."
                ],
                "actividades": [
                    "Elaborar planos de acuerdo a las especificaciones técnicas del elemento a fabricar.",
                    "Desarrollar ejercicios de modelado de sólidos por medio de las tecnologías CAD.",
                    "Elaborar bitácora de los sólidos modelados por medio de las tecnologías CAD."
                ],
                "hD": 36, "hI": 12
            }]
        },
        "CARACTERIZAR EL TORNO Y SUS PROCESOS, PARA EL MECANIZADO DE PIEZAS MECÁNICAS": {
            "competencias": [{
                "nombre": "Mecanizar pieza industrial de acuerdo con técnicas manuales y semiautomáticas",
                "resultados": [
                    "Poner a punto materia prima, puesto de trabajo, máquina y herramientas de acuerdo al proceso de torneado convencional.",
                    "Ejecutar operaciones de torneado convencional de acuerdo con procedimientos técnicos y normativa ambiental.",
                    "Mantener el torno convencional en condiciones óptimas de limpieza, ajuste y lubricación."
                ],
                "actividades": [
                    "Fundamentar conceptos y principios de metrología con instrumentos análogos, digitales y automáticos.",
                    "Elaborar ruta operacional del proceso de mecanizado mediante torneado convencional.",
                    "Aplicar técnicas de lubricación y mantenimiento de primer nivel del torno."
                ],
                "hD": 36, "hI": 12
            }]
        },
        "CARACTERIZAR LA FRESADORA Y SUS PROCESOS, PARA EL MECANIZADO DE PIEZAS MECÁNICAS": {
            "competencias": [{
                "nombre": "Mecanizado de piezas en Tornos y Fresadoras Convencionales",
                "resultados": [
                    "Alistar materia prima, puesto de trabajo, máquina y herramientas de fresado convencional.",
                    "Mecanizar productos metalmecánicos con fresadora convencional cumpliendo especificaciones técnicas.",
                    "Mantener la fresadora convencional en condiciones óptimas de limpieza, ajuste y lubricación."
                ],
                "actividades": [
                    "Identificar los diferentes instrumentos de medición que intervienen en el proceso.",
                    "Realizar orden operacional de las piezas a mecanizar con herramientas y parámetros de corte.",
                    "Fabricar pieza con operaciones básicas de fresado según especificaciones técnicas."
                ],
                "hD": 48, "hI": 0
            }]
        }
    },
    "PLANEACIÓN": {
        "PREPARAR LOS INSUMOS REQUERIDOS PARA LA ELABORACIÓN DE LOS PRODUCTOS METALMECÁNICOS.": {
            "competencias": [{
                "nombre": "Alistar máquina herramienta de control numérico de acuerdo con especificaciones técnicas",
                "resultados": [
                    "01 Alistar materia prima del producto según especificaciones técnicas."
                ],
                "actividades": [
                    "Seleccionar materiales para la fabricación de las piezas metalmecánicas.",
                    "Utilizar técnicamente los instrumentos de medición de acuerdo a la pieza a medir.",
                    "Cumplir normas medioambientales, de seguridad y salud ocupacional en el alistamiento."
                ],
                "hD": 36, "hI": 12
            }]
        },
        "PLANEAR EL PROCESO DE FABRICACIÓN, DE ACUERDO CON REQUERIMIENTOS TÉCNICOS.": {
            "competencias": [{
                "nombre": "Alistar máquina herramienta CNC de acuerdo con especificaciones técnicas",
                "resultados": [
                    "02 Alistar maquinaria de Control Numérico Computarizado y herramientas de acuerdo al proceso de mecanizado."
                ],
                "actividades": [
                    "Fundamentar conceptos y principios de los tratamientos térmicos, durezas e instrumentos de medición.",
                    "Verificar estado de la máquina de acuerdo al proceso a realizar.",
                    "Ajustar parámetros de mecanizado en la máquina herramienta CNC."
                ],
                "hD": 36, "hI": 12
            }]
        },
        "DESARROLLAR LOS PROTOTIPOS REQUERIDOS PARA EL PROCESO DE MECANIZADO.": {
            "competencias": [{
                "nombre": "Mecanizar pieza industrial de acuerdo con sistema de control numérico",
                "resultados": [
                    "Modelar prototipos teniendo en cuenta las especificaciones técnicas y requerimientos del cliente."
                ],
                "actividades": [
                    "Desarrollar prototipos del proyecto de Formación en software CAD.",
                    "Generar plano técnico de las piezas según las especificaciones del producto.",
                    "Establecer coordenadas en el torno y fresadora de acuerdo a geometría de la pieza."
                ],
                "hD": 216, "hI": 72
            }]
        },
        "CREAR LAS RUTAS Y SECUENCIAS DE MECANIZADO PARA LAS MAQUINAS HERRAMIENTAS DE CONTROL NUMÉRICO.": {
            "competencias": [{
                "nombre": "Mecanizar pieza industrial de acuerdo con sistema de control numérico",
                "resultados": [
                    "Generar rutas de mecanizado para Tornos de Control Numérico Computarizado.",
                    "Generar rutas de mecanizado para Fresadoras de Control Numérico Computarizado.",
                    "Generar rutas de mecanizado para Centros de Mecanizado CNC."
                ],
                "actividades": [
                    "Programar tornos CNC de acuerdo con procedimientos técnicos.",
                    "Programar fresadoras CNC de acuerdo con procedimientos técnicos.",
                    "Programar centros de mecanizado CNC con ayuda de software CAM."
                ],
                "hD": 36, "hI": 12
            }]
        }
    },
    "EJECUCIÓN Y EVALUACIÓN": {
        "PRODUCIR EL MECANIZADO DE LAS PIEZAS EN MAQUINAS HERRAMIENTAS CNC.": {
            "competencias": [{
                "nombre": "Mecanizar pieza industrial de acuerdo con sistema de control numérico",
                "resultados": [
                    "Fabricar piezas en Centros de Mecanizado de control numérico computarizado.",
                    "Fabricar piezas en Torno de control numérico computarizado.",
                    "Fabricar piezas en Fresadora de control numérico computarizado."
                ],
                "actividades": [
                    "Programar tornos, fresadoras y centros de mecanizado CNC con ayuda de software CAM.",
                    "Elaborar piezas requeridas en el Proyecto de Formación.",
                    "Revisar la calidad del producto mecanizado según planos entregados."
                ],
                "hD": 180, "hI": 60
            }]
        },
        "GESTIONAR LA PRODUCCIÓN EN ATENCIÓN A LOS REQUERIMIENTOS TÉCNICOS DE LAS PIEZAS A FABRICAR": {
            "competencias": [{
                "nombre": "Programar la producción según métodos y parámetros técnicos",
                "resultados": [
                    "Organizar proceso productivo de acuerdo a órdenes de fabricación, tiempos, mano de obra y materiales.",
                    "Diseñar programa de producción de piezas metalmecánicas según requerimientos y estándares."
                ],
                "actividades": [
                    "Programar producción de acuerdo con estándares de fabricación.",
                    "Diseñar cronogramas de fabricación dependiendo del proceso de mecanizado.",
                    "Elaborar histogramas, diagramas de Gantt y listas de chequeo según programa de producción."
                ],
                "hD": 108, "hI": 36
            }]
        },
        "EVALUAR SI LA PRODUCCIÓN DE LAS PIEZAS METALMECÁNICAS CUMPLE CON LOS ESTÁNDARES DE CALIDAD.": {
            "competencias": [{
                "nombre": "Programar la producción según métodos y parámetros técnicos",
                "resultados": [
                    "Diseñar programa de producción de piezas metalmecánicas según requerimientos y estándares de producción."
                ],
                "actividades": [
                    "Elaborar el control estadístico y de calidad de las piezas fabricadas.",
                    "Elaborar informe de producción de acuerdo con el tiempo estándar establecido.",
                    "Calcular la capacidad de trabajo de las máquinas de mecanizado."
                ],
                "hD": 72, "hI": 24
            }]
        }
    }
}

# ── FUNCIONES PDF ─────────────────────────────────────────────────
SENA_GREEN  = colors.HexColor('#006633')
LIGHT_GREEN = colors.HexColor('#E8F5E9')
GRAY_BORDER = colors.HexColor('#AAAAAA')

def get_styles():
    return {
        'label':      ParagraphStyle('label',      fontName='Helvetica-Bold', fontSize=8,   alignment=TA_LEFT,   leading=10),
        'value':      ParagraphStyle('value',      fontName='Helvetica',      fontSize=8,   alignment=TA_LEFT,   leading=10),
        'cell':       ParagraphStyle('cell',       fontName='Helvetica',      fontSize=7.5, alignment=TA_LEFT,   leading=10),
        'cell_c':     ParagraphStyle('cell_c',     fontName='Helvetica',      fontSize=7.5, alignment=TA_CENTER, leading=10),
        'header':     ParagraphStyle('header',     fontName='Helvetica-Bold', fontSize=7.5, alignment=TA_CENTER, leading=10),
    }

def build_page(aprendiz, resultados, actividades, datos, styles):
    BLACK = colors.black

    # Encabezado
    logo = Paragraph("<b>SENA</b>", ParagraphStyle('lg', fontName='Helvetica-Bold', fontSize=16, alignment=TA_CENTER, textColor=SENA_GREEN))
    header = Table([[
        logo,
        Paragraph("<b>SERVICIO NACIONAL DE APRENDIZAJE SENA</b><br/><b>CENTRO NACIONAL COLOMBO ALEMAN</b><br/>PLAN DE TRABAJO",
                  ParagraphStyle('hd', fontName='Helvetica', fontSize=9, alignment=TA_CENTER, leading=13)),
        Paragraph("V2.0", ParagraphStyle('v', fontName='Helvetica', fontSize=7, alignment=TA_LEFT, textColor=colors.gray))
    ]], colWidths=[2.5*cm, 13.5*cm, 1.5*cm])
    header.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),1,BLACK),('GRID',(0,0),(-1,-1),.5,GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))

    # Fila 1
    f1 = Table([[
        Paragraph("<b>Programa de\nFormación:</b>", styles['label']),
        Paragraph(datos['programa'], styles['value']),
        Paragraph("<b>Instructor:</b>", styles['label']),
        Paragraph(datos['instructor'], styles['value']),
    ]], colWidths=[2.2*cm, 8.3*cm, 2*cm, 5*cm])
    f1.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),.5,BLACK),('GRID',(0,0),(-1,-1),.5,GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(0,0),LIGHT_GREEN),('BACKGROUND',(2,0),(2,0),LIGHT_GREEN),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),
    ]))

    # Fila 2
    f2 = Table([[
        Paragraph("<b>Número de\nFicha:</b>", styles['label']),
        Paragraph(datos['ficha'], styles['value']),
        Paragraph("<b>Proyecto\nFormativo:</b>", styles['label']),
        Paragraph(datos['proyecto'], styles['value']),
        Paragraph("<b>Fase del\nProyecto:</b>", styles['label']),
        Paragraph(datos['fase'], styles['value']),
    ]], colWidths=[1.8*cm, 1.8*cm, 2*cm, 7*cm, 1.8*cm, 3.1*cm])
    f2.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),.5,BLACK),('GRID',(0,0),(-1,-1),.5,GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(0,0),LIGHT_GREEN),('BACKGROUND',(2,0),(2,0),LIGHT_GREEN),('BACKGROUND',(4,0),(4,0),LIGHT_GREEN),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),
    ]))

    # Fila 3
    f3 = Table([
        [Paragraph("<b>Nombre del\nAprendiz:</b>", styles['label']),
         Paragraph(aprendiz['nombre'], styles['value']),
         Paragraph("<b>Observaciones:</b>", styles['label']),
         Paragraph(datos.get('observaciones',''), styles['value'])],
        [Paragraph("<b>Documento\nde Identidad:</b>", styles['label']),
         Paragraph(aprendiz['doc'], styles['value']), '', ''],
    ], colWidths=[2.2*cm, 6.3*cm, 2.5*cm, 6.5*cm])
    f3.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),.5,BLACK),('GRID',(0,0),(-1,-1),.5,GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('BACKGROUND',(0,0),(0,1),LIGHT_GREEN),('BACKGROUND',(2,0),(2,0),LIGHT_GREEN),
        ('SPAN',(2,0),(3,1)),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),('LEFTPADDING',(0,0),(-1,-1),4),
    ]))

    # Título descriptores
    desc_title = Table([[
        Paragraph("<b>DESCRIPTORES PARA EL DESARROLLO DE LA RUTA DE APRENDIZAJE</b>",
                  ParagraphStyle('dt', fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER))
    ]], colWidths=[17.5*cm])
    desc_title.setStyle(TableStyle([
        ('BOX',(0,0),(-1,-1),.5,BLACK),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))

    # Tabla descriptores
    h = styles['header']
    num_rows = max(len(actividades), 5)
    col_w = [5*cm, 1.2*cm, 5.5*cm, 1.1*cm, 1.1*cm, 1.5*cm, 1.5*cm, 1.3*cm, 1.3*cm]

    table_data = [
        [Paragraph("<b>Resultados de Aprendizaje</b>",h), Paragraph("<b>N°\nActividad</b>",h),
         Paragraph("<b>Actividades a desarrollar</b>",h), Paragraph("<b>Forma de\nEntrega de\nactividad</b>",h),
         '', Paragraph("<b>Fecha de entrega</b>",h), '', Paragraph("<b>¿Entrego la\nActividad?</b>",h), ''],
        ['','','', Paragraph("<b>Física</b>",h), Paragraph("<b>Digital</b>",h),
         Paragraph("<b>Concertada</b>",h), Paragraph("<b>Final</b>",h), Paragraph("<b>SI</b>",h), Paragraph("<b>NO</b>",h)],
    ]

    ra_text = "\n\n".join(resultados) if resultados else ""
    for i in range(num_rows):
        act = actividades[i] if i < len(actividades) else ""
        row = [
            Paragraph(ra_text, styles['cell']) if i == 0 else '',
            Paragraph(str(i+1), styles['cell_c']),
            Paragraph(act, styles['cell']),
            '','','','','',''
        ]
        table_data.append(row)

    desc_table = Table(table_data, colWidths=col_w,
                       rowHeights=[None, None]+[1.5*cm]*num_rows)
    ts = [
        ('BOX',(0,0),(-1,-1),.5,BLACK),('GRID',(0,0),(-1,-1),.5,GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('ALIGN',(0,2),(0,-1),'LEFT'),('ALIGN',(2,2),(2,-1),'LEFT'),
        ('LEFTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('SPAN',(3,0),(4,0)),('SPAN',(5,0),(6,0)),('SPAN',(7,0),(8,0)),
        ('SPAN',(0,2),(0,1+num_rows)),
        ('BACKGROUND',(0,0),(-1,1),LIGHT_GREEN),
        ('FONTNAME',(0,0),(-1,1),'Helvetica-Bold'),
    ]
    desc_table.setStyle(TableStyle(ts))

    return [header, Spacer(1,3), f1, f2, f3, Spacer(1,4), desc_title, desc_table]


def generar_pdf_bytes(aprendices, resultados, actividades, datos):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                            rightMargin=1.2*cm, leftMargin=1.2*cm,
                            topMargin=1.2*cm, bottomMargin=1.2*cm)
    styles = get_styles()
    story = []
    for i, ap in enumerate(aprendices):
        story.extend(build_page(ap, resultados, actividades, datos, styles))
        if i < len(aprendices)-1:
            story.append(PageBreak())
    doc.build(story)
    buf.seek(0)
    return buf.getvalue()


def leer_aprendices(file):
    wb = openpyxl.load_workbook(file, data_only=True)
    ws = wb.active
    aprendices = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]: continue
        tipo = str(row[1] or 'CC').strip()
        num  = str(row[2] or '').strip()
        nom  = str(row[3] or '').strip()
        ape  = str(row[4] or '').strip()
        nombre = f"{nom} {ape}".strip()
        if nombre:
            aprendices.append({'nombre': nombre, 'doc': f"{tipo} {num}".strip()})
    return aprendices


# ── INTERFAZ ──────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>🎓 Generador de Plan de Trabajo SENA</h1>
  <p>Producción de Componentes Mecánicos con Máquinas CNC · Cód. 821100 v1 · Centro Colombo Alemán</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    # ── PASO 1: Aprendices ────────────────────────────────────────
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 1. Lista de aprendices</div>', unsafe_allow_html=True)
    archivo = st.file_uploader("Cargar archivo Excel (.xlsx)", type=["xlsx","xls"], label_visibility="collapsed")
    aprendices = []
    if archivo:
        aprendices = leer_aprendices(archivo)
        st.success(f"✅ {len(aprendices)} aprendices cargados")
        chips_html = "".join([f'<span class="aprendiz-chip">{a["nombre"].split()[0]} {a["nombre"].split()[-1]}</span>' for a in aprendices[:8]])
        if len(aprendices) > 8:
            chips_html += f'<span class="aprendiz-chip">+{len(aprendices)-8} más</span>'
        st.markdown(chips_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── PASO 2: Instructor y grupo ────────────────────────────────
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 2. Instructor y grupo</div>', unsafe_allow_html=True)
    instructor = st.text_input("Nombre del instructor", placeholder="Nombres y apellidos completos")
    c1, c2 = st.columns(2)
    ficha    = c1.text_input("Número de ficha", placeholder="Ej. 2441890")
    proyecto = st.text_input("Proyecto formativo", value="FABRICAR ELEMENTOS MECÁNICOS CON TECNOLOGÍA DE CONTROL NUMÉRICO COMPUTARIZADO")
    observaciones = st.text_area("Observaciones (opcional)", placeholder="Observaciones para todos los aprendices...", height=70)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # ── PASO 3: Fase → Actividad → Competencia ────────────────────
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 3. Fase, actividad y competencia</div>', unsafe_allow_html=True)

    fase = st.selectbox("Fase del proyecto", [""] + list(PLANEACION.keys()))

    actividad_sel = ""
    competencia_sel = None

    if fase:
        acts = list(PLANEACION[fase].keys())
        actividad_sel = st.selectbox("Actividad de proyecto", [""] + acts,
                                     format_func=lambda x: x[:70]+"..." if len(x)>70 else x)

    if fase and actividad_sel:
        comps = PLANEACION[fase][actividad_sel]["competencias"]
        nombres_comp = [c["nombre"] for c in comps]
        comp_nombre = st.selectbox("Competencia", nombres_comp,
                                   format_func=lambda x: x[:75]+"..." if len(x)>75 else x)
        competencia_sel = next(c for c in comps if c["nombre"] == comp_nombre)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── PASO 4: Resultados de aprendizaje ─────────────────────────
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✅ 4. Resultados de aprendizaje</div>', unsafe_allow_html=True)

    resultados_sel = []
    if competencia_sel:
        for ra in competencia_sel["resultados"]:
            if st.checkbox(ra, key=ra):
                resultados_sel.append(ra)
        if resultados_sel:
            st.caption(f"{len(resultados_sel)} resultado(s) seleccionado(s)")
    else:
        st.caption("Selecciona una competencia para ver los resultados.")

    st.markdown('</div>', unsafe_allow_html=True)

    # ── PASO 5: Actividades ───────────────────────────────────────
    if competencia_sel:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📝 5. Actividades a desarrollar</div>', unsafe_allow_html=True)
        for i, act in enumerate(competencia_sel["actividades"]):
            st.markdown(f"**{i+1}.** {act}")
        c1, c2 = st.columns(2)
        c1.metric("Horas trabajo directo", competencia_sel["hD"])
        c2.metric("Horas trabajo independiente", competencia_sel["hI"])
        st.markdown('</div>', unsafe_allow_html=True)

# ── BOTÓN GENERAR ─────────────────────────────────────────────────
st.divider()
col_btn, col_info = st.columns([2, 3])

with col_btn:
    generar = st.button("🖨️ Generar PDFs para todos los aprendices")

with col_info:
    if not archivo:
        st.info("⬆️ Carga la lista de aprendices para continuar.")
    elif not instructor or not ficha:
        st.warning("Completa el nombre del instructor y número de ficha.")
    elif not fase or not actividad_sel:
        st.warning("Selecciona la fase y actividad del proyecto.")
    elif not resultados_sel:
        st.warning("Selecciona al menos un resultado de aprendizaje.")
    else:
        st.success(f"✅ Listo para generar {len(aprendices)} documentos PDF.")

if generar:
    if not archivo:
        st.error("Carga la lista de aprendices.")
    elif not instructor or not ficha:
        st.error("Completa el nombre del instructor y número de ficha.")
    elif not fase or not actividad_sel:
        st.error("Selecciona la fase y actividad del proyecto.")
    elif not resultados_sel:
        st.error("Selecciona al menos un resultado de aprendizaje.")
    else:
        with st.spinner(f"Generando {len(aprendices)} documentos..."):
            datos = {
                'programa': "PRODUCCIÓN DE COMPONENTES MECÁNICOS CON MÁQUINAS DE CONTROL NUMÉRICO COMPUTARIZADO",
                'instructor': instructor.upper(),
                'ficha': ficha,
                'proyecto': proyecto.upper(),
                'fase': fase,
                'observaciones': observaciones,
            }
            pdf_bytes = generar_pdf_bytes(
                aprendices,
                resultados_sel,
                competencia_sel["actividades"],
                datos
            )

        st.markdown('<div class="success-box">', unsafe_allow_html=True)
        st.success(f"✅ PDF generado con {len(aprendices)} páginas")
        st.download_button(
            label=f"⬇️ Descargar Plan_Trabajo_SENA.pdf ({len(aprendices)} páginas)",
            data=pdf_bytes,
            file_name=f"Plan_Trabajo_Ficha_{ficha}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
