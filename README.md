# ☁️ Jhojen Cloud DevOps Roadmap v2.0

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-green?style=for-the-badge)

Esta es mi aplicación personalizada de seguimiento de Roadmap para convertirme en **Arquitecto Cloud DevOps**. Originalmente diseñada en HTML/Tailwind, ha sido migrada a **Python (Streamlit)** para integrar capacidades de automatización y persistencia de datos.

## 🚀 Características
- **Visualización de Progreso:** Dashboard interactivo con métricas en tiempo real.
- **Filtros Dinámicos:** Organización por Mes de estudio y Categoría (Estudio, Proyecto, Negocio).
- **Persistencia Local:** Los datos se guardan automáticamente en archivos JSON.
- **Enfoque SRE:** Incluye secciones de gestión de energía y hábitos de alto rendimiento.

## 🛠️ Stack Tecnológico
- **Lenguaje:** Python
- **Framework UI:** Streamlit
- **Datos:** JSON (Estructura de tareas y progreso)
- **Despliegue:** Streamlit Cloud

## 📂 Estructura del Proyecto
```bash
├── app.py              # Aplicación principal de Streamlit
├── data/
│   ├── roadmap.json    # Base de datos de tareas extraídas
│   └── progress.json   # Registro de progreso del usuario
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

## 🔧 Instalación Local
Si deseas ejecutarlo en tu propia máquina:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/TU_USUARIO/jhojen-roadmap.git
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicia la aplicación:
   ```bash
   streamlit run app.py
   ```

---
*Diseñado por Jhojen - Estudiante de Telemática 5to Año*
