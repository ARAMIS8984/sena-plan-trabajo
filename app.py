import streamlit as st
import openpyxl
import base64
from io import BytesIO
from datetime import date
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import os

st.set_page_config(page_title="Plan Concertado SENA", page_icon="🟢", layout="wide")

# ── LOGO EN BASE64 para web ───────────────────────────────────────
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
logo_html = (f'<img src="data:image/png;base64,{logo_b64}" '
             f'style="height:64px;background:white;border-radius:6px;padding:4px;">')  if logo_b64 else \
            '<span style="font-weight:900;font-size:1.4rem;background:white;color:#006633;padding:6px 10px;border-radius:6px;">SENA</span>'

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"]{{background-color:#0a1628;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'%3E%3Cdefs%3E%3CradialGradient id='g1' cx='25%25' cy='40%25' r='50%25'%3E%3Cstop offset='0%25' stop-color='%23006633' stop-opacity='0.35'/%3E%3Cstop offset='100%25' stop-color='transparent'/%3E%3C/radialGradient%3E%3CradialGradient id='g2' cx='75%25' cy='70%25' r='45%25'%3E%3Cstop offset='0%25' stop-color='%23003d1f' stop-opacity='0.4'/%3E%3Cstop offset='100%25' stop-color='transparent'/%3E%3C/radialGradient%3E%3C/defs%3E%3Crect width='1200' height='800' fill='%230a1628'/%3E%3Crect width='1200' height='800' fill='url(%23g1)'/%3E%3Crect width='1200' height='800' fill='url(%23g2)'/%3E%3Cg opacity='0.05' stroke='%2300ff88' stroke-width='0.5'%3E%3Cline x1='0' y1='200' x2='1200' y2='200'/%3E%3Cline x1='0' y1='400' x2='1200' y2='400'/%3E%3Cline x1='0' y1='600' x2='1200' y2='600'/%3E%3Cline x1='300' y1='0' x2='300' y2='800'/%3E%3Cline x1='600' y1='0' x2='600' y2='800'/%3E%3Cline x1='900' y1='0' x2='900' y2='800'/%3E%3C/g%3E%3C/svg%3E");background-size:cover;background-attachment:fixed;}}
[data-testid="stHeader"]{{background:rgba(10,22,40,0.95)!important;backdrop-filter:blur(10px);border-bottom:1px solid rgba(0,153,68,0.2);}}
[data-testid="block-container"]{{padding-top:1.5rem!important;}}
[data-testid="stMarkdown"] p,[data-testid="stMarkdown"] label,.stRadio label,.stCheckbox label,[data-testid="stWidgetLabel"],[data-testid="stCaptionContainer"] p{{color:#c8e6c9!important;}}
.main-header{{background:linear-gradient(135deg,rgba(0,77,38,0.95) 0%,rgba(0,120,60,0.95) 100%);padding:1.4rem 2rem;border-radius:16px;margin-bottom:1.5rem;display:flex;align-items:center;gap:1.5rem;border:1px solid rgba(0,200,100,0.3);box-shadow:0 8px 32px rgba(0,0,0,0.4);backdrop-filter:blur(12px);}}
.main-header-text h1{{color:white;margin:0;font-size:2rem;line-height:1.2;font-weight:700}}
.main-header-text p{{color:#a5d6a7;margin:6px 0 0;font-size:.9rem}}
.section-box{{background:rgba(255,255,255,0.05);border:1px solid rgba(0,200,100,0.2);border-radius:16px;padding:1.3rem 1.6rem;margin-bottom:1rem;box-shadow:0 8px 32px rgba(0,0,0,0.3);backdrop-filter:blur(12px);}}
.section-title{{color:#4caf50;font-weight:700;font-size:.82rem;margin-bottom:.8rem;text-transform:uppercase;letter-spacing:.08em;}}
.chip{{display:inline-block;background:rgba(0,153,68,0.25);color:#a5d6a7;padding:3px 10px;border-radius:20px;font-size:.78rem;margin:2px;border:1px solid rgba(0,200,100,0.3);}}
.stButton>button{{background:linear-gradient(135deg,#006633,#009944)!important;color:white!important;border:1px solid rgba(0,200,100,0.4)!important;border-radius:10px!important;font-size:1rem!important;font-weight:600!important;box-shadow:0 4px 20px rgba(0,100,50,0.4)!important;}}
.stButton>button:hover{{background:linear-gradient(135deg,#005522,#007733)!important;box-shadow:0 6px 24px rgba(0,150,70,0.5)!important;}}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(0,200,100,0.25)!important;border-radius:8px!important;color:white!important;}}
[data-baseweb="select"]>div{{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(0,200,100,0.25)!important;border-radius:8px!important;color:white!important;}}
hr{{border-color:rgba(0,200,100,0.15)!important;}}
</style>
<div class="main-header">
  <div>{logo_html}</div>
  <div class="main-header-text">
    <h1>Plan Concertado</h1>
    <p>Servicio Nacional de Aprendizaje SENA · Centro Nacional Colombo Alemán</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# CATÁLOGO DE PROGRAMAS — agrega aquí nuevos programas fácilmente
# ════════════════════════════════════════════════════════════════
CATALOGO = {

  # ── PROGRAMA 1 ─────────────────────────────────────────────────
  "821100 v1 — Producción de Componentes Mecánicos con Máquinas CNC": {
    "proyectos": {

      "2441890 - FABRICAR ELEMENTOS MECÁNICOS CON TECNOLOGÍA DE CONTROL NUMERICO COMPUTARIZADO": {
        "nombre_completo": "2441890 - FABRICAR ELEMENTOS MECÁNICOS CON TECNOLOGÍA DE CONTROL NUMERICO COMPUTARIZADO",
        "fases": {
          "INDUCCIÓN": {
            "Inducción": {"competencias": [{
              "nombre": "Resultado de aprendizaje de la inducción",
              "resultados": [
                {"ra": "Identificar la dinámica organizacional del SENA y el rol de la Formación Profesional Integral de acuerdo con su proyecto de vida y el desarrollo profesional",
                 "actividades": ["Asumir actitudes y valores en los diferentes ámbitos de formación, vida y trabajo.", "Reconocer la identidad institucional y los procedimientos administrativos.", "Incorporar a su proyecto de vida las oportunidades ofrecidas por el SENA."]}
              ], "hD": 36, "hI": 12
            }]}
          },
          "ANÁLISIS": {
            "CARACTERIZAR LA MATERIA PRIMA, HERRAMIENTAS Y EQUIPOS EN EL AJUSTE MANUAL DE LAS PIEZAS.": {"competencias": [{
              "nombre": "Pulir piezas industriales de acuerdo con técnicas manuales y mecánicas",
              "resultados": [
                {"ra": "01 Alistar materia prima e instrumentos de medición teniendo en cuenta normativa ocupacional, ambiental y procedimientos técnicos.", "actividades": ["Fundamentar conceptos y principios de metrología con instrumentos análogos.", "Seleccionar materiales de acuerdo con parámetros técnicos y normativa.", "Trazar y cortar material de acuerdo con planos y normativa ambiental."]},
                {"ra": "02 Poner a punto herramientas y equipos de banco para el ajuste manual y mecánico.", "actividades": ["Fundamentar conceptos y principios de trabajo con herramientas de banco.", "Rectificar muelas de afilar teniendo en cuenta procedimientos técnicos.", "Afilar brocas cumpliendo procedimientos técnicos y normas de seguridad."]},
                {"ra": "03 Ajustar manual y mecánicamente con herramientas y equipos de banco.", "actividades": ["Fundamentar conceptos y principios de ajustes y tolerancias.", "Aplicar técnicas de limado manual de acuerdo a parámetros establecidos.", "Ejecutar operaciones de roscado manual con macho y terraja."]}
              ], "hD": 36, "hI": 12
            }]},
            "REALIZAR EL DESPIECE CORRESPONDIENTE A LAS PIEZAS DEL PROYECTO SEGÚN EL DIEDRO APROPIADO.": {"competencias": [{
              "nombre": "Dibujar planos mecánicos de acuerdo con normas técnicas",
              "resultados": [
                {"ra": "01 Dibujar elementos mecánicos de acuerdo con especificaciones técnicas.", "actividades": ["Elaborar planos de acuerdo a las especificaciones técnicas del elemento.", "Dibujar a mano alzada y con instrumentos la geometría del elemento mecánico.", "Generar cortes, secciones y vistas ortogonales o isométricas."]},
                {"ra": "Modelar componentes mecánicos en software CAD según especificaciones técnicas.", "actividades": ["Desarrollar ejercicios de modelado de sólidos por medio de las tecnologías CAD.", "Generar modelos digitales de piezas y ensambles mecánicos.", "Parametrizar los modelos digitales según tipo y dimensiones del elemento."]},
                {"ra": "Documentar los planos según normas técnicas.", "actividades": ["Elaborar bitácora de los sólidos modelados por medio de las tecnologías CAD.", "Elaborar planos de fabricación y montaje de acuerdo con normas técnicas.", "Organizar archivos físicos y digitales de acuerdo a políticas de la empresa."]}
              ], "hD": 36, "hI": 12
            }]},
            "CARACTERIZAR EL TORNO Y SUS PROCESOS, PARA EL MECANIZADO DE PIEZAS MECÁNICAS": {"competencias": [{
              "nombre": "Mecanizar pieza industrial de acuerdo con técnicas manuales y semiautomáticas",
              "resultados": [
                {"ra": "Poner a punto materia prima, puesto de trabajo, máquina y herramientas de acuerdo al proceso de torneado convencional.", "actividades": ["Fundamentar conceptos y principios de metrología con instrumentos análogos.", "Seleccionar el material de acuerdo con especificaciones técnicas del plano.", "Patronar las herramientas de acuerdo con el orden operacional de mecanizado."]},
                {"ra": "Ejecutar operaciones de torneado convencional de acuerdo con procedimientos técnicos y normativa ambiental.", "actividades": ["Elaborar ruta operacional del proceso de mecanizado mediante torneado convencional.", "Ajustar parámetros de mecanizado de acuerdo con el acabado superficial.", "Mecanizar productos metalmecánicos con torno convencional según procedimientos."]},
                {"ra": "Mantener el torno convencional en condiciones óptimas de limpieza, ajuste y lubricación.", "actividades": ["Aplicar técnicas de lubricación en la máquina teniendo en cuenta la ruta entregada.", "Clasificar y disponer los residuos generados según procedimientos establecidos.", "Reportar fallas y necesidades de mantenimiento según lineamientos de la empresa."]}
              ], "hD": 36, "hI": 12
            }]},
            "CARACTERIZAR LA FRESADORA Y SUS PROCESOS, PARA EL MECANIZADO DE PIEZAS MECÁNICAS": {"competencias": [{
              "nombre": "Mecanizado de piezas en Tornos y Fresadoras Convencionales",
              "resultados": [
                {"ra": "Alistar materia prima, puesto de trabajo, máquina y herramientas de fresado convencional.", "actividades": ["Identificar los diferentes instrumentos de medición que intervienen en el proceso.", "Ajustar las características dimensionales del producto según especificaciones.", "Revisar la calidad del producto (acabados, tolerancias, dimensiones y geometría)."]},
                {"ra": "Mecanizar productos metalmecánicos con fresadora convencional cumpliendo especificaciones técnicas.", "actividades": ["Realizar orden operacional de las piezas a mecanizar con parámetros de corte.", "Fabricar pieza con operaciones básicas de fresado según especificaciones técnicas.", "Fabricar pieza con operaciones propias de cabezal divisor según especificaciones."]},
                {"ra": "Mantener la fresadora convencional en condiciones óptimas de limpieza, ajuste y lubricación.", "actividades": ["Aplicar técnicas de lubricación en la fresadora según ruta de mantenimiento.", "Almacenar el refrigerante usado de acuerdo con normas medioambientales.", "Informar fallas e inspección de la máquina según lineamientos de la empresa."]}
              ], "hD": 48, "hI": 0
            }]}
          },
          "PLANEACIÓN": {
            "PREPARAR LOS INSUMOS REQUERIDOS PARA LA ELABORACIÓN DE LOS PRODUCTOS METALMECÁNICOS.": {"competencias": [{
              "nombre": "Alistar máquina herramienta de control numérico de acuerdo con especificaciones técnicas",
              "resultados": [
                {"ra": "01 Alistar materia prima del producto según especificaciones técnicas.", "actividades": ["Seleccionar materiales para la fabricación de las piezas metalmecánicas.", "Utilizar técnicamente los instrumentos de medición de acuerdo a la pieza.", "Cortar el material de acuerdo al plano de fabricación y procedimientos técnicos."]}
              ], "hD": 36, "hI": 12
            }]},
            "PLANEAR EL PROCESO DE FABRICACIÓN, DE ACUERDO CON REQUERIMIENTOS TÉCNICOS.": {"competencias": [{
              "nombre": "Alistar máquina herramienta CNC de acuerdo con especificaciones técnicas",
              "resultados": [
                {"ra": "02 Alistar maquinaria de Control Numérico Computarizado y herramientas de acuerdo al proceso de mecanizado.", "actividades": ["Fundamentar conceptos y principios de los tratamientos térmicos y durezas.", "Verificar estado de la máquina CNC de acuerdo al proceso a realizar.", "Ajustar parámetros de mecanizado en la máquina herramienta CNC."]}
              ], "hD": 36, "hI": 12
            }]},
            "DESARROLLAR LOS PROTOTIPOS REQUERIDOS PARA EL PROCESO DE MECANIZADO.": {"competencias": [{
              "nombre": "Mecanizar pieza industrial de acuerdo con sistema de control numérico",
              "resultados": [
                {"ra": "Modelar prototipos teniendo en cuenta las especificaciones técnicas y requerimientos del cliente.", "actividades": ["Desarrollar prototipos del proyecto de Formación en software CAD.", "Generar plano técnico de las piezas según las especificaciones del producto.", "Verificar en el simulador el programa del torno y fresadora según geometría."]}
              ], "hD": 216, "hI": 72
            }]},
            "CREAR LAS RUTAS Y SECUENCIAS DE MECANIZADO PARA LAS MAQUINAS HERRAMIENTAS CNC.": {"competencias": [{
              "nombre": "Mecanizar pieza industrial de acuerdo con sistema de control numérico",
              "resultados": [
                {"ra": "Generar rutas de mecanizado para Tornos de Control Numérico Computarizado.", "actividades": ["Programar tornos CNC de acuerdo con procedimientos técnicos.", "Establecer coordenadas en el torno de acuerdo a geometría de la pieza.", "Documentar los programas del torno de acuerdo a procedimientos de mecanizado."]},
                {"ra": "Generar rutas de mecanizado para Fresadoras de Control Numérico Computarizado.", "actividades": ["Programar fresadoras CNC de acuerdo con procedimientos técnicos.", "Establecer coordenadas en la fresadora de acuerdo a geometría de la pieza.", "Optimizar en el simulador el programa de la fresadora según geometría."]},
                {"ra": "Generar rutas de mecanizado para Centros de Mecanizado CNC.", "actividades": ["Programar centros de mecanizado CNC con ayuda de software CAM.", "Simular el programa de la pieza a fabricar según el control de la máquina.", "Mecanizar la pieza en las máquinas CNC cumpliendo especificaciones técnicas."]}
              ], "hD": 36, "hI": 12
            }]}
          },
          "EJECUCIÓN Y EVALUACIÓN": {
            "PRODUCIR EL MECANIZADO DE LAS PIEZAS EN MAQUINAS HERRAMIENTAS CNC.": {"competencias": [{
              "nombre": "Mecanizar pieza industrial de acuerdo con sistema de control numérico",
              "resultados": [
                {"ra": "Fabricar piezas en Centros de Mecanizado de control numérico computarizado.", "actividades": ["Programar centros de mecanizado CNC con ayuda de software CAM.", "Establecer coordenadas en los centros de mecanizado según geometría.", "Verificar que el proceso y producto final cumplan requerimientos técnicos."]},
                {"ra": "Fabricar piezas en Torno de control numérico computarizado.", "actividades": ["Elaborar piezas requeridas en el Proyecto de Formación con torno CNC.", "Ajustar parámetros del torno de acuerdo con el acabado superficial.", "Revisar la calidad del producto torneado según planos entregados."]},
                {"ra": "Fabricar piezas en Fresadora de control numérico computarizado.", "actividades": ["Manejar software CAD-CAM para generar las rutas de mecanizado en fresadora.", "Fresar con diferentes técnicas teniendo en cuenta la geometría de la pieza.", "Determinar parámetros de corte según especificaciones de tolerancias y acabados."]}
              ], "hD": 180, "hI": 60
            }]},
            "GESTIONAR LA PRODUCCIÓN EN ATENCIÓN A LOS REQUERIMIENTOS TÉCNICOS.": {"competencias": [{
              "nombre": "Programar la producción según métodos y parámetros técnicos",
              "resultados": [
                {"ra": "Organizar proceso productivo de acuerdo a órdenes de fabricación, tiempos, mano de obra y materiales.", "actividades": ["Programar producción de acuerdo con estándares de fabricación.", "Diseñar cronogramas de fabricación dependiendo del proceso de mecanizado.", "Elaborar diagramas de Gantt y listas de chequeo según programa de producción."]},
                {"ra": "Diseñar programa de producción de piezas metalmecánicas según requerimientos y estándares.", "actividades": ["Elaborar el control estadístico y de calidad de las piezas fabricadas.", "Elaborar informe de producción de acuerdo con el tiempo estándar establecido.", "Calcular la capacidad de trabajo de las máquinas de mecanizado."]}
              ], "hD": 108, "hI": 36
            }]}
          }
        }
      },

      "3343700 - FABRICACIÓN DE COMPONENTES MECÁNICOS CON MÁQUINAS HERRAMIENTAS CNC PARA EL SECTOR INDUSTRIAL DEL ATLÁNTICO": {
        "nombre_completo": "3343700 - FABRICACIÓN DE COMPONENTES MECÁNICOS CON MÁQUINAS HERRAMIENTAS CNC PARA EL SECTOR INDUSTRIAL DEL ATLÁNTICO",
        "fases": {
          "IDENTIFICACIÓN": {
            "DETERMINAR LAS ESPECIFICACIONES TÉCNICAS DEL PROCESO DE FABRICACIÓN DE UN COMPONENTE MECÁNICO.": {"competencias": [
              {"nombre": "290201212 - ALISTAMIENTO DE MATERIA PRIMA, ACCESORIOS Y PLAN DE PRODUCCIÓN PARA MAQUINAS HERRAMIENTAS CNC",
               "resultados": [
                {"ra": "01. Alistar materia prima del producto según especificaciones técnicas.", "actividades": ["Identificar el tipo de material a mecanizar teniendo en cuenta sus propiedades y características.", "Seleccionar y cortar el material de acuerdo al plano de fabricación.", "Cumplir normas medioambientales, de seguridad y salud ocupacional en el alistamiento."]},
                {"ra": "02. Alistar maquinaria CNC y herramientas de acuerdo al proceso de mecanizado.", "actividades": ["Fundamentar conceptos y principios de metrología con instrumentos análogos.", "Verificar estado de la máquina de acuerdo al proceso a realizar.", "Ajustar herramienta de corte teniendo en cuenta el proceso de mecanizado."]}
               ], "hD": 36, "hI": 12},
              {"nombre": "290201190 - ELABORACIÓN DE PLANOS MECÁNICOS DE ACUERDO CON NORMAS TÉCNICAS",
               "resultados": [
                {"ra": "02. Documentar los planos según normas técnicas.", "actividades": ["Elaborar bitácora de los sólidos modelados por medio de las tecnologías CAD.", "Elaborar planos de fabricación y montaje según normas técnicas.", "Organizar técnicamente los archivos físicos y digitales."]},
                {"ra": "03. Dibujar elementos mecánicos de acuerdo con especificaciones técnicas.", "actividades": ["Elaborar planos de acuerdo a las especificaciones técnicas del elemento a fabricar.", "Dibujar a mano alzada y con instrumentos la geometría del elemento mecánico.", "Generar cortes, secciones y vistas ortogonales o isométricas."]}
               ], "hD": 36, "hI": 12},
              {"nombre": "290201210 - PULIR PIEZAS INDUSTRIALES DE ACUERDO CON TÉCNICAS MANUALES Y MECÁNICAS",
               "resultados": [
                {"ra": "01. Alistar materia prima e instrumentos de medición teniendo en cuenta normativa ocupacional, ambiental y procedimientos técnicos.", "actividades": ["Fundamentar conceptos y principios de metrología con instrumentos análogos.", "Identificar y clasificar instrumentos de medición dimensional.", "Convertir unidades entre sistemas de medición."]}
               ], "hD": 36, "hI": 12}
            ]}
          },
          "ALISTAMIENTO": {
            "DEFINIR LA SECUENCIA OPERACIONAL PARA LA FABRICACIÓN DE UN COMPONENTE MECÁNICO.": {"competencias": [
              {"nombre": "290201190 - ELABORACIÓN DE PLANOS MECÁNICOS DE ACUERDO CON NORMAS TÉCNICAS",
               "resultados": [
                {"ra": "01. Modelar componentes mecánicos en software CAD según especificaciones técnicas.", "actividades": ["Desarrollar ejercicios de modelado de sólidos por medio de las tecnologías CAD.", "Generar modelos digitales de piezas y ensambles mecánicos según especificaciones.", "Parametrizar los modelos digitales según tipo y dimensiones del elemento mecánico."]}
               ], "hD": 36, "hI": 12},
              {"nombre": "290201213 - MECANIZADO DE PIEZAS UTILIZANDO MÁQUINAS DE CONTROL NUMÉRICO COMPUTARIZADO",
               "resultados": [
                {"ra": "03. Modelar prototipos teniendo en cuenta las especificaciones técnicas y requerimientos del cliente.", "actividades": ["Desarrollar prototipos del proyecto de Formación en software CAD.", "Generar plano técnico de las piezas según las especificaciones del producto.", "Establecer coordenadas en el torno de acuerdo a geometría de la pieza."]}
               ], "hD": 216, "hI": 72},
              {"nombre": "220601048 - PROGRAMACIÓN DE LA PRODUCCIÓN PARA LA FABRICACIÓN DE PRODUCTOS MECANIZADOS",
               "resultados": [
                {"ra": "01. Organizar proceso productivo de acuerdo a órdenes de fabricación, tiempos, mano de obra y materiales requeridos.", "actividades": ["Programar producción de acuerdo con estándares de fabricación.", "Diseñar cronogramas de fabricación dependiendo del proceso de mecanizado.", "Elaborar histogramas, diagramas de Gantt y listas de chequeo."]},
                {"ra": "02. Diseñar programa de producción de piezas metalmecánicas según requerimientos y estándares.", "actividades": ["Elaborar el control estadístico y de calidad de las piezas fabricadas.", "Calcular la capacidad de trabajo de las máquinas de mecanizado.", "Identificar los puntos críticos de control del proceso productivo."]}
               ], "hD": 108, "hI": 36}
            ]},
            "PREPARAR EL ÁREA DE TRABAJO Y LOS INSUMOS PARA LA FABRICACIÓN DE COMPONENTES MECÁNICOS.": {"competencias": [
              {"nombre": "290201210 - PULIR PIEZAS INDUSTRIALES DE ACUERDO CON TÉCNICAS MANUALES Y MECÁNICAS",
               "resultados": [
                {"ra": "03. Poner a punto herramientas y equipos de banco para el ajuste manual y mecánico.", "actividades": ["Fundamentar conceptos y principios de trabajo con herramientas de banco.", "Afilar herramientas de corte teniendo en cuenta el tipo de trabajo.", "Lubricar herramientas y equipos de banco según procedimientos técnicos."]},
                {"ra": "02. Ajustar manual y mecánicamente con herramientas y equipos de banco.", "actividades": ["Fundamentar conceptos y principios de ajustes y tolerancias.", "Aplicar técnicas de limado manual de acuerdo a parámetros establecidos.", "Ejecutar operaciones de roscado manual con macho y terraja."]}
               ], "hD": 36, "hI": 12},
              {"nombre": "290201211 - MECANIZADO DE PIEZAS EN TORNOS Y FRESADORAS CONVENCIONALES",
               "resultados": [
                {"ra": "02. Alistar materia prima, puesto de trabajo, máquina y herramientas de fresado convencional.", "actividades": ["Identificar conceptos y principios de metrología con máquinas de medición por coordenadas.", "Establecer e interpretar secuencias de fabricación para el mecanizado en fresadora.", "Seleccionar herramientas de corte a utilizar en los procesos de fresado."]},
                {"ra": "04. Mantener la fresadora convencional en condiciones óptimas de limpieza, ajuste y lubricación.", "actividades": ["Mecanizar piezas en máquinas fresadora convencional.", "Aplicar técnicas de lubricación en la fresadora según ruta de mantenimiento.", "Informar fallas e inspección de la máquina según lineamientos de la empresa."]},
                {"ra": "05. Poner a punto materia prima, puesto de trabajo, máquina y herramientas de torneado convencional.", "actividades": ["Fundamentar conceptos y principios de metrología con instrumentos análogos, digitales y automáticos.", "Interpretar secuencias de fabricación o ruta de trabajo en tornos paralelos.", "Seleccionar materiales y herramientas de corte para el torneado."]},
                {"ra": "06. Mantener el torno convencional en condiciones óptimas de limpieza, ajuste y lubricación.", "actividades": ["Elaborar ruta operacional del proceso de mecanizado mediante torneado convencional.", "Aplicar técnicas de lubricación en la máquina teniendo en cuenta la ruta entregada.", "Clasificar y disponer los residuos generados según procedimientos establecidos."]}
               ], "hD": 36, "hI": 12}
            ]}
          },
          "FABRICACIÓN": {
            "PRODUCIR COMPONENTES MECÁNICOS CON MÁQUINAS HERRAMIENTAS CONVENCIONALES.": {"competencias": [
              {"nombre": "290201211 - MECANIZADO DE PIEZAS EN TORNOS Y FRESADORAS CONVENCIONALES",
               "resultados": [
                {"ra": "03. Ejecutar operaciones de torneado convencional de acuerdo con procedimientos técnicos y normativa ambiental.", "actividades": ["Elaborar ruta operacional del proceso de mecanizado mediante torneado convencional.", "Ajustar parámetros de mecanizado de acuerdo con el acabado superficial.", "Mecanizar productos metalmecánicos con torno convencional según procedimientos."]},
                {"ra": "01. Mecanizar productos metalmecánicos con fresadora convencional cumpliendo especificaciones técnicas.", "actividades": ["Mecanizar piezas en máquinas fresadora convencional.", "Ajustar los parámetros de mecanizado de acuerdo con el acabado superficial.", "Revisar la calidad del producto (acabados, tolerancias, dimensiones y geometría)."]}
               ], "hD": 72, "hI": 24}
            ]},
            "PRODUCIR COMPONENTES MECÁNICOS CON MÁQUINAS HERRAMIENTAS CNC": {"competencias": [
              {"nombre": "290201213 - MECANIZADO DE PIEZAS UTILIZANDO MÁQUINAS DE CONTROL NUMÉRICO COMPUTARIZADO",
               "resultados": [
                {"ra": "04. Generar rutas de mecanizado para Tornos CNC.", "actividades": ["Programar tornos, fresadoras y centros de mecanizado CNC.", "Establecer coordenadas en el torno de acuerdo a geometría de la pieza.", "Documentar los programas del torno de acuerdo a procedimientos de mecanizado."]},
                {"ra": "02. Generar rutas de mecanizado para Fresadoras CNC.", "actividades": ["Programar fresadoras CNC de acuerdo con procedimientos técnicos.", "Optimizar en el simulador el programa de la fresadora según geometría.", "Determinar parámetros de mecanizado para la fresadora CNC."]},
                {"ra": "07. Generar rutas de mecanizado para Centros de Mecanizado CNC.", "actividades": ["Programar centros de mecanizado CNC con ayuda de software CAM.", "Simular el programa de los centros de mecanizado CNC.", "Mecanizar la pieza en las máquinas CNC cumpliendo especificaciones técnicas."]},
                {"ra": "06. Fabricar piezas en Centros de Mecanizado CNC.", "actividades": ["Programar tornos, fresadoras y centros de mecanizado CNC con ayuda de software CAM.", "Verificar que el proceso y producto final cumplan requerimientos técnicos.", "Controlar las dimensiones del producto en el mecanizado CNC."]},
                {"ra": "01. Fabricar piezas en Torno CNC.", "actividades": ["Elaborar piezas requeridas en el Proyecto de Formación con torno CNC.", "Ajustar parámetros del torno de acuerdo con el acabado superficial.", "Revisar la calidad del producto torneado según planos entregados."]},
                {"ra": "05. Fabricar piezas en Fresadora CNC.", "actividades": ["Manejar software CAD-CAM para generar las rutas de mecanizado en fresadora.", "Fresar con diferentes técnicas teniendo en cuenta la geometría de la pieza.", "Determinar parámetros de corte según especificaciones de tolerancias y acabados."]}
               ], "hD": 180, "hI": 60}
            ]},
            "VERIFICAR LA PRODUCCIÓN DE LOS COMPONENTES MECÁNICOS CON ESTÁNDARES DE CALIDAD.": {"competencias": [
              {"nombre": "290201213 - MECANIZADO DE PIEZAS UTILIZANDO MÁQUINAS DE CONTROL NUMÉRICO COMPUTARIZADO",
               "resultados": [
                {"ra": "06. Fabricar piezas en Centros de Mecanizado CNC (verificación de calidad).", "actividades": ["Verificar que el proceso y producto final cumplan requerimientos técnicos.", "Controlar las dimensiones durante el proceso, cumpliendo requerimientos del plano.", "Elaborar informe de producción de acuerdo con el tiempo estándar establecido."]}
               ], "hD": 180, "hI": 60}
            ]}
          },
          "MEJORAMIENTO": {
            "Ensamblar los componentes mecánicos fabricados aplicando estrategias de solución": {"competencias": [{
              "nombre": "RESULTADOS DE APRENDIZAJE ETAPA PRÁCTICA",
              "resultados": [
                {"ra": "Aplicar en la resolución de problemas reales del sector productivo los conocimientos, habilidades y destrezas pertinentes a las competencias del programa de formación.", "actividades": ["Aplicar estrategias y metodologías de autogestión en el sector productivo.", "Resolver problemas reales integrando las competencias adquiridas durante la formación.", "Presentar informe de actividades realizadas en la etapa productiva."]}
              ], "hD": 0, "hI": 0
            }]}
          }
        }
      }
    }
  }

  # ── AGREGA AQUÍ NUEVOS PROGRAMAS ──────────────────────────────
  # "CÓDIGO — Nombre del Programa": {
  #   "proyectos": {
  #     "CÓDIGO — Nombre Proyecto": {
  #       "nombre_completo": "NOMBRE COMPLETO",
  #       "fases": { ... }
  #     }
  #   }
  # }

}

# ── PDF ───────────────────────────────────────────────────────────
SENA_GREEN  = colors.HexColor('#006633')
LIGHT_GREEN = colors.HexColor('#E8F5E9')
GRAY_BORDER = colors.HexColor('#AAAAAA')
BLACK       = colors.black

def get_styles():
    return {
        'label':  ParagraphStyle('label',  fontName='Helvetica-Bold', fontSize=8,   alignment=TA_LEFT,   leading=10),
        'value':  ParagraphStyle('value',  fontName='Helvetica',      fontSize=8,   alignment=TA_LEFT,   leading=10),
        'cell':   ParagraphStyle('cell',   fontName='Helvetica',      fontSize=7.5, alignment=TA_LEFT,   leading=10),
        'cell_c': ParagraphStyle('cell_c', fontName='Helvetica',      fontSize=7.5, alignment=TA_CENTER, leading=10),
        'header': ParagraphStyle('header', fontName='Helvetica-Bold', fontSize=7.5, alignment=TA_CENTER, leading=10),
    }

def get_logo_image():
    """Devuelve un objeto Image de reportlab con el logo SENA, o None si no existe."""
    for path in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_sena.png"),
        "logo_sena.png",
    ]:
        if os.path.exists(path):
            return Image(path, width=1.8*cm, height=1.8*cm)
    return None

def build_page(aprendiz, resultados_sel, datos, styles):
    # Cada RA numerado y separado con salto de línea entre ellos
    ra_partes = []
    for i, r in enumerate(resultados_sel):
        ra_partes.append(f"<b>{i+1}.</b> {r["ra"]}")
    ra_texto = "<br/><br/>".join(ra_partes)

    actividades_todas = []
    for r in resultados_sel:
        actividades_todas.extend(r["actividades"])

    fecha_plan = datos.get('fecha_plan', date.today().strftime("%d/%m/%Y"))

    # ── ANCHO ÚNICO para TODAS las tablas ────────────────────────
    # letter=21.59cm, márgenes 2x1.2cm → útil=19.19cm
    # Usamos 19.1cm y borde uniforme 0.5pt en todas las tablas
    W  = 19.1*cm
    BX = 0.5          # grosor de borde unificado

    estilo_base = [
        ('BOX',   (0,0),(-1,-1), BX, BLACK),
        ('GRID',  (0,0),(-1,-1), BX, GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0,0),(-1,-1), 4),
        ('BOTTOMPADDING',(0,0),(-1,-1), 4),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
    ]

    # ── ENCABEZADO: logo + título + versión  (suman W) ───────────
    # 2.3 + 15.3 + 1.5 = 19.1
    logo_img  = get_logo_image()
    logo_cell = logo_img if logo_img else Paragraph(
        "<b>SENA</b>",
        ParagraphStyle('lg', fontName='Helvetica-Bold', fontSize=16,
                       alignment=TA_CENTER, textColor=SENA_GREEN))

    header = Table([[
        logo_cell,
        Paragraph("<b>SERVICIO NACIONAL DE APRENDIZAJE SENA</b><br/>"
                  "<b>CENTRO NACIONAL COLOMBO ALEMAN</b><br/>PLAN CONCERTADO",
                  ParagraphStyle('hd', fontName='Helvetica', fontSize=9,
                                  alignment=TA_CENTER, leading=13)),
        Paragraph("V2.0", ParagraphStyle('v', fontName='Helvetica', fontSize=7,
                                          alignment=TA_LEFT, textColor=colors.gray)),
    ]], colWidths=[2.3*cm, 15.3*cm, 1.5*cm])
    header.setStyle(TableStyle(estilo_base + [
        ('TOPPADDING',   (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
    ]))

    # ── FILA 1: Programa / Instructor  (suman W) ─────────────────
    # 2.8 + 9.5 + 2.3 + 4.5 = 19.1
    sv = ParagraphStyle('sv', fontName='Helvetica', fontSize=7.5,
                        alignment=TA_LEFT, leading=10)
    sl = ParagraphStyle('sl', fontName='Helvetica-Bold', fontSize=7.5,
                        alignment=TA_LEFT, leading=10)

    f1 = Table([[
        Paragraph("<b>Programa de\nFormación:</b>", sl),
        Paragraph(datos['programa'], sv),
        Paragraph("<b>Instructor:</b>", sl),
        Paragraph(datos['instructor'], sv),
    ]], colWidths=[2.8*cm, 9.5*cm, 2.3*cm, 4.5*cm])
    f1.setStyle(TableStyle(estilo_base + [
        ('BACKGROUND',(0,0),(0,0), LIGHT_GREEN),
        ('BACKGROUND',(2,0),(2,0), LIGHT_GREEN),
    ]))

    # ── FILA 2: Ficha / Proyecto / Fase  (suman W) ───────────────
    # 2.0 + 2.3 + 2.3 + 7.5 + 2.0 + 3.0 = 19.1
    f2 = Table([[
        Paragraph("<b>Número de\nFicha:</b>", sl),
        Paragraph(datos['ficha'], sv),
        Paragraph("<b>Proyecto\nFormativo:</b>", sl),
        Paragraph(datos['proyecto'], sv),
        Paragraph("<b>Fase del\nProyecto:</b>", sl),
        Paragraph(datos['fase'], sv),
    ]], colWidths=[2.0*cm, 2.3*cm, 2.3*cm, 7.5*cm, 2.0*cm, 3.0*cm])
    f2.setStyle(TableStyle(estilo_base + [
        ('BACKGROUND',(0,0),(0,0), LIGHT_GREEN),
        ('BACKGROUND',(2,0),(2,0), LIGHT_GREEN),
        ('BACKGROUND',(4,0),(4,0), LIGHT_GREEN),
    ]))

    # ── FILA 3: Aprendiz / Doc / Observaciones  (suman W) ────────
    # 2.8 + 6.8 + 2.8 + 6.7 = 19.1
    f3 = Table([
        [Paragraph("<b>Nombre del\nAprendiz:</b>", sl),
         Paragraph(aprendiz['nombre'], sv),
         Paragraph("<b>Observaciones:</b>", sl),
         Paragraph(datos.get('observaciones',''), sv)],
        [Paragraph("<b>Documento\nde Identidad:</b>", sl),
         Paragraph(aprendiz['doc'], sv), '', ''],
    ], colWidths=[2.8*cm, 6.8*cm, 2.8*cm, 6.7*cm])
    f3.setStyle(TableStyle(estilo_base + [
        ('BACKGROUND',(0,0),(0,1), LIGHT_GREEN),
        ('BACKGROUND',(2,0),(2,0), LIGHT_GREEN),
        ('SPAN',(2,0),(3,1)),
    ]))

    # ── TABLA DESCRIPTORES: columnas suman W = 19.1 cm ───────────
    # RA(4.4) | N°(1.1) | Act(4.8) | Física(1.4) | Digital(1.4) | Concertada(1.9) | Final(1.9) | SI(1.1) | NO(1.1)
    # 4.4 + 1.1 + 4.8 + 1.4 + 1.4 + 1.9 + 1.9 + 1.1 + 1.1 = 19.1
    col_w = [4.4*cm, 1.1*cm, 4.8*cm, 1.4*cm, 1.4*cm, 1.9*cm, 1.9*cm, 1.1*cm, 1.1*cm]
    # Verificación: sum = 19.1 ✓
    NCOLS = len(col_w)
    h = styles['header']
    num_rows = len(actividades_todas)  # exactamente las que hay, sin filas vacías

    # Fila 0: título "DESCRIPTORES..." en SPAN de todas las columnas
    title_style = ParagraphStyle('dt', fontName='Helvetica-Bold', fontSize=9, alignment=TA_CENTER)
    fila_titulo  = [Paragraph("<b>DESCRIPTORES PARA EL DESARROLLO DE LA RUTA DE APRENDIZAJE</b>", title_style)] + ['']*(NCOLS-1)
    # Fila 1: encabezados superiores
    fila_hdr1 = [
        Paragraph("<b>Resultados de\nAprendizaje</b>",h),
        Paragraph("<b>N°\nActiv.</b>",h),
        Paragraph("<b>Actividades a desarrollar</b>",h),
        Paragraph("<b>Forma de\nEntrega</b>",h), '',
        Paragraph("<b>Fecha de entrega</b>",h), '',
        Paragraph("<b>¿Entregó?</b>",h), '',
    ]
    # Fila 2: subencabezados
    fila_hdr2 = ['','','',
        Paragraph("<b>Física</b>",h), Paragraph("<b>Digital</b>",h),
        Paragraph("<b>Concertada</b>",h), Paragraph("<b>Final</b>",h),
        Paragraph("<b>SI</b>",h), Paragraph("<b>NO</b>",h),
    ]

    table_data = [fila_titulo, fila_hdr1, fila_hdr2]

    for i in range(num_rows):
        act = actividades_todas[i] if i < len(actividades_todas) else ""
        # Determinar SI / NO según entrega_map
        entrega = datos.get('entrega_map', {}).get(aprendiz['nombre'], None)
        if entrega is True:
            cel_si = Paragraph("X", styles['cell_c'])
            cel_no = Paragraph("", styles['cell_c'])
        elif entrega is False:
            cel_si = Paragraph("", styles['cell_c'])
            cel_no = Paragraph("X", styles['cell_c'])
        else:
            cel_si = Paragraph("", styles['cell_c'])
            cel_no = Paragraph("", styles['cell_c'])
        table_data.append([
            Paragraph(ra_texto, styles['cell']) if i == 0 else '',
            Paragraph(str(i+1), styles['cell_c']),
            Paragraph(act, styles['cell']),
            Paragraph("X", styles['cell_c']),
            '',
            Paragraph(fecha_plan, styles['cell_c']),
            '',
            cel_si,
            cel_no,
        ])

    DATA_START = 3
    desc_table = Table(table_data, colWidths=col_w,
                       rowHeights=[None, None, None] + [1.5*cm]*num_rows)
    desc_table.setStyle(TableStyle([
        ('BOX',  (0,0),(-1,-1), BX, BLACK),
        ('GRID', (0,0),(-1,-1), BX, GRAY_BORDER),
        ('VALIGN',(0,0),(-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0),(-1,-1), 'CENTER'),
        ('ALIGN', (0,DATA_START),(0,-1), 'LEFT'),
        ('ALIGN', (2,DATA_START),(2,-1), 'LEFT'),
        ('VALIGN',(0,DATA_START),(0,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0),(-1,-1), 3),
        ('TOPPADDING',  (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('SPAN',(0,0),(-1,0)),
        ('SPAN',(3,1),(4,1)),('SPAN',(5,1),(6,1)),('SPAN',(7,1),(8,1)),
        ('SPAN',(0,DATA_START),(0,DATA_START+num_rows-1)),
        ('BACKGROUND',(0,0),(-1,0), LIGHT_GREEN),
        ('BACKGROUND',(0,1),(-1,2), LIGHT_GREEN),
        ('FONTNAME',(0,0),(-1,2),'Helvetica-Bold'),
        ('TEXTCOLOR',(3,DATA_START),(3,-1), SENA_GREEN),
        ('FONTNAME', (3,DATA_START),(3,-1),'Helvetica-Bold'),
        ('FONTSIZE', (3,DATA_START),(3,-1), 10),
        # Fecha en fuente pequeña para que quepe en 1 línea
        ('FONTSIZE', (5,DATA_START),(5,-1), 6.5),
        # SI en verde
        ('TEXTCOLOR',(7,DATA_START),(7,-1), SENA_GREEN),
        ('FONTNAME', (7,DATA_START),(7,-1),'Helvetica-Bold'),
        ('FONTSIZE', (7,DATA_START),(7,-1), 10),
        # NO en rojo
        ('TEXTCOLOR',(8,DATA_START),(8,-1), colors.HexColor('#CC0000')),
        ('FONTNAME', (8,DATA_START),(8,-1),'Helvetica-Bold'),
        ('FONTSIZE', (8,DATA_START),(8,-1), 10),
    ]))

    return [header, Spacer(1,3), f1, f2, f3, Spacer(1,4), desc_table]


def generar_pdf_bytes(aprendices, resultados_sel, datos):
    """PDF único con todos los aprendices (una página por aprendiz)."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf,pagesize=letter,rightMargin=1.2*cm,leftMargin=1.2*cm,topMargin=1.2*cm,bottomMargin=1.2*cm)
    styles = get_styles()
    story = []
    for i, ap in enumerate(aprendices):
        story.extend(build_page(ap, resultados_sel, datos, styles))
        if i < len(aprendices)-1:
            story.append(PageBreak())
    doc.build(story)
    buf.seek(0)
    return buf.getvalue()

def generar_zip_bytes(aprendices, resultados_sel, datos):
    """ZIP con un PDF individual por cada aprendiz."""
    import zipfile, re
    zip_buf = BytesIO()
    styles = get_styles()
    with zipfile.ZipFile(zip_buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for ap in aprendices:
            # PDF individual
            buf = BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter,
                                    rightMargin=1.2*cm, leftMargin=1.2*cm,
                                    topMargin=1.2*cm,  bottomMargin=1.2*cm)
            doc.build(build_page(ap, resultados_sel, datos, styles))
            # Nombre de archivo limpio (sin caracteres especiales)
            nombre_limpio = re.sub(r'[^\w\s-]', '', ap['nombre']).strip().replace(' ', '_')
            filename = f"Plan_Concertado_{nombre_limpio}.pdf"
            zf.writestr(filename, buf.getvalue())
    zip_buf.seek(0)
    return zip_buf.getvalue()

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
col1, col2 = st.columns([1,1], gap="large")

with col1:
    # 1. Lista aprendices
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 1. Lista de aprendices</div>', unsafe_allow_html=True)
    archivo = st.file_uploader("Excel (.xlsx)", type=["xlsx","xls"], label_visibility="collapsed")
    aprendices = []
    if archivo:
        aprendices = leer_aprendices(archivo)
        st.success(f"✅ {len(aprendices)} aprendices cargados")
        chips = "".join([f'<span class="chip">{a["nombre"].split()[0]} {a["nombre"].split()[-1]}</span>' for a in aprendices[:8]])
        if len(aprendices) > 8: chips += f'<span class="chip">+{len(aprendices)-8} más</span>'
        st.markdown(chips, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Instructor y grupo
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 2. Instructor y grupo</div>', unsafe_allow_html=True)
    instructor    = st.text_input("Nombre del instructor", placeholder="Nombres y apellidos completos")
    ficha         = st.text_input("Número de ficha", placeholder="Ej. 2441890")
    fecha_plan    = st.date_input("Fecha del Plan Concertado", value=date.today())
    observaciones = st.text_area("Observaciones (opcional)", height=68)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # 3. Selección en cascada: Programa → Proyecto → Fase → Actividad → Competencia
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📚 3. Programa, proyecto y fase</div>', unsafe_allow_html=True)

    programa_sel = st.selectbox("Programa de formación", ["— Selecciona —"] + list(CATALOGO.keys()),
                                format_func=lambda x: x[:80]+"..." if len(x)>80 else x)
    proyectos_disponibles = []
    proyecto_data = None
    fases_data = {}

    if programa_sel != "— Selecciona —":
        proyectos_disponibles = list(CATALOGO[programa_sel]["proyectos"].keys())
        proyecto_sel = st.selectbox("Proyecto formativo", ["— Selecciona —"] + proyectos_disponibles,
                                    format_func=lambda x: x[:80]+"..." if len(x)>80 else x)
        if proyecto_sel != "— Selecciona —":
            proyecto_data = CATALOGO[programa_sel]["proyectos"][proyecto_sel]
            fases_data    = proyecto_data["fases"]
            fase_sel = st.selectbox("Fase del proyecto", ["— Selecciona —"] + list(fases_data.keys()))
        else:
            fase_sel = "— Selecciona —"
    else:
        proyecto_sel = "— Selecciona —"
        fase_sel     = "— Selecciona —"

    actividad_sel   = "— Selecciona —"
    competencia_sel = None

    if fase_sel != "— Selecciona —" and fase_sel in fases_data:
        acts = list(fases_data[fase_sel].keys())
        actividad_sel = st.selectbox("Actividad de proyecto", ["— Selecciona —"] + acts,
                                     format_func=lambda x: (x[:70]+"...") if len(x)>70 else x)

    if actividad_sel != "— Selecciona —":
        comps = fases_data[fase_sel][actividad_sel]["competencias"]
        nombres_comp = [c["nombre"] for c in comps]
        comp_nombre  = st.selectbox("Competencia", nombres_comp,
                                    format_func=lambda x: (x[:75]+"...") if len(x)>75 else x)
        competencia_sel = next(c for c in comps if c["nombre"] == comp_nombre)

    st.markdown('</div>', unsafe_allow_html=True)

    # 4. Resultados de aprendizaje
    resultados_sel = []
    if competencia_sel:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">✅ 4. Resultados de aprendizaje</div>', unsafe_allow_html=True)
        st.caption("Selecciona uno o más. Sus actividades se combinarán en el PDF.")
        for i, r in enumerate(competencia_sel["resultados"]):
            key = f"ra_{programa_sel[:10]}_{fase_sel[:10]}_{i}"
            if st.checkbox(r["ra"], key=key):
                resultados_sel.append(r)
                with st.expander(f"📝 Actividades del resultado {i+1}", expanded=True):
                    for j, act in enumerate(r["actividades"]):
                        st.markdown(f"**{j+1}.** {act}")
        if resultados_sel:
            total_acts = sum(len(r["actividades"]) for r in resultados_sel)
            st.info(f"✅ {len(resultados_sel)} resultado(s) → {total_acts} actividades en el PDF")
        st.markdown('</div>', unsafe_allow_html=True)

# ── SECCIÓN OPCIONAL: ¿Entregó? ───────────────────────────────────
entrega_map = {}  # nombre → True(SI) / False(NO) / None(en blanco)
if aprendices:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📬 ¿Entregó la actividad? <span style="font-weight:400;color:#888;font-size:.8rem">(opcional)</span></div>', unsafe_allow_html=True)
    st.caption("Si no lo completas, SI y NO quedan en blanco en el PDF.")

    usar_entrega = st.toggle("Registrar entrega de actividades", value=False)
    if usar_entrega:
        marcar_todos = st.toggle("✅ Marcar todos como SI", value=True, key="todos_si")
        st.markdown("---")
        cols_hdr = st.columns([4, 1, 1])
        cols_hdr[0].markdown("**Aprendiz**")
        cols_hdr[1].markdown("**SI**")
        cols_hdr[2].markdown("**NO**")
        for ap in aprendices:
            default_si = marcar_todos
            cols = st.columns([4, 1, 1])
            cols[0].markdown(f"{ap['nombre']}")
            si  = cols[1].checkbox("", value=default_si,  key=f"si_{ap['nombre']}", label_visibility="collapsed")
            no  = cols[2].checkbox("", value=not default_si if marcar_todos else False, key=f"no_{ap['nombre']}", label_visibility="collapsed")
            if si and not no:
                entrega_map[ap['nombre']] = True
            elif no and not si:
                entrega_map[ap['nombre']] = False
            else:
                entrega_map[ap['nombre']] = True  # si ambos o ninguno, SI por defecto
    st.markdown('</div>', unsafe_allow_html=True)

# ── GENERAR ───────────────────────────────────────────────────────
st.divider()
col_btn, col_info = st.columns([2,3])
with col_info:
    if not archivo: st.info("⬆️ Carga la lista de aprendices para continuar.")
    elif not instructor or not ficha: st.warning("Completa el nombre del instructor y número de ficha.")
    elif programa_sel == "— Selecciona —" or proyecto_sel == "— Selecciona —": st.warning("Selecciona el programa y proyecto formativo.")
    elif fase_sel == "— Selecciona —" or actividad_sel == "— Selecciona —": st.warning("Selecciona la fase y actividad del proyecto.")
    elif not resultados_sel: st.warning("Selecciona al menos un resultado de aprendizaje.")
    else:
        total_acts = sum(len(r["actividades"]) for r in resultados_sel)
        st.success(f"✅ Listo — {len(aprendices)} aprendices · {len(resultados_sel)} resultado(s) · {total_acts} actividades")

with col_btn:
    generar = st.button("🖨️ Generar Plan Concertado")

if generar:
    errores = []
    if not archivo: errores.append("Carga la lista de aprendices.")
    if not instructor: errores.append("Escribe el nombre del instructor.")
    if not ficha: errores.append("Escribe el número de ficha.")
    if programa_sel == "— Selecciona —": errores.append("Selecciona el programa de formación.")
    if proyecto_sel == "— Selecciona —": errores.append("Selecciona el proyecto formativo.")
    if fase_sel == "— Selecciona —" or actividad_sel == "— Selecciona —": errores.append("Selecciona fase y actividad.")
    if not resultados_sel: errores.append("Selecciona al menos un resultado de aprendizaje.")
    if errores:
        for e in errores: st.error(e)
    else:
        with st.spinner(f"Generando {len(aprendices)} documentos..."):
            datos = {
                'programa':      "PRODUCCIÓN DE COMPONENTES MECÁNICOS CON MÁQUINAS DE CONTROL NUMÉRICO COMPUTARIZADO",
                'instructor':    instructor.upper(),
                'ficha':         ficha,
                'proyecto':      proyecto_data["nombre_completo"],
                'fase':          fase_sel,
                'observaciones': observaciones,
                'fecha_plan':    fecha_plan.strftime("%d/%m/%Y"),
                'entrega_map':   entrega_map,
            }
            zip_bytes = generar_zip_bytes(aprendices, resultados_sel, datos)
            pdf_bytes = generar_pdf_bytes(aprendices, resultados_sel, datos)

        st.success(f"✅ {len(aprendices)} documentos generados — elige cómo descargar:")

        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                label=f"📦 Descargar ZIP ({len(aprendices)} PDFs individuales)",
                data=zip_bytes,
                file_name=f"PlanConcertado_Ficha_{ficha}.zip",
                mime="application/zip",
                use_container_width=True,
            )
        with c2:
            st.download_button(
                label=f"📄 Descargar PDF único ({len(aprendices)} páginas)",
                data=pdf_bytes,
                file_name=f"PlanConcertado_Ficha_{ficha}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
