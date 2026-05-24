# 🎓 Generador de Plan de Trabajo SENA

Aplicación web para generar automáticamente el **Plan de Trabajo SENA** (formato V2.0) para todos los aprendices de un grupo, a partir de la planeación pedagógica del programa **Producción de Componentes Mecánicos con Máquinas CNC (Cód. 821100 v1)**.

---

## ✅ Cómo usar

1. Sube el Excel con la lista de aprendices (columnas: N°, Tipo Doc, N° Documento, Nombre, Apellidos)
2. Ingresa los datos del instructor y ficha
3. Selecciona: Fase → Actividad → Competencia
4. Marca los resultados de aprendizaje
5. Haz clic en **Generar PDFs**
6. Descarga el PDF con una página por aprendiz

---

## 🚀 Despliegue en Streamlit Cloud (gratis)

1. Haz fork o sube esta carpeta a un repositorio de GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Conecta tu cuenta de GitHub
4. Selecciona el repositorio y el archivo `app.py`
5. Haz clic en **Deploy** — en 2 minutos tienes tu link

---

## 📁 Estructura

```
sena_app/
├── app.py            ← Aplicación principal
├── requirements.txt  ← Dependencias
└── README.md         ← Este archivo
```

---

## 📋 Formato del Excel de aprendices

| N° | Tipo de Doc. | N° Documento | Nombre | Apellidos |
|----|-------------|-------------|--------|-----------|
| 1  | CC          | 1001918128  | OLARIS MERCEDES | MADRID CAMARGO |
| 2  | CC          | 1001918852  | DAYANA INES | BARRIOS AHUMADA |
