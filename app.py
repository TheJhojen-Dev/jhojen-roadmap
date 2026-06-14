import streamlit as st
import json
import os
from datetime import datetime

# Configuración de página
st.set_page_config(
    page_title="Jhojen Cloud DevOps Dashboard",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- THEME MANAGEMENT ---
if 'theme' not in st.session_state:
    st.session_state.theme = "Oscuro"

with st.sidebar:
    st.title("Configuración")
    theme_choice = st.radio("Modo de Visualización", ["Oscuro", "Claro"], 
                           index=0 if st.session_state.theme == "Oscuro" else 1)
    st.session_state.theme = theme_choice

# Colores dinámicos según el tema
if st.session_state.theme == "Oscuro":
    bg_color = "#030712"
    text_color = "#f1f5f9"
    card_bg = "#0f172a"
    card_border = "#1e293b"
    secondary_text = "#94a3b8"
    divider_color = "#1e293b"
else:
    bg_color = "#f8fafc"
    text_color = "#0f172a"
    card_bg = "#ffffff"
    card_border = "#e2e8f0"
    secondary_text = "#64748b"
    divider_color = "#e2e8f0"

# Estilo personalizado dinámico
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Geist', sans-serif;
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}
    .mono {{
        font-family: 'Geist Mono', monospace;
    }}
    .task-card {{
        background-color: {card_bg};
        border: 1px solid {card_border};
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s;
    }}
    .task-card:hover {{
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }}
    .badge {{
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-transform: uppercase;
    }}
    .badge-estudio {{ background-color: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }}
    .badge-proyecto {{ background-color: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }}
    .badge-negocio {{ background-color: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }}
    .badge-descanso {{ background-color: rgba(100, 116, 139, 0.1); color: #94a3b8; border: 1px solid rgba(100, 116, 139, 0.2); }}
    
    /* Adaptación de textos específicos */
    h1, h2, h3, h4, .stMarkdown p {{
        color: {text_color} !important;
    }}
    .secondary-text {{
        color: {secondary_text} !important;
    }}
    
    /* Progress Bar */
    .stProgress > div > div > div > div {{
        background-color: #3b82f6;
    }}
    
    /* Divider */
    hr {{
        border-color: {divider_color} !important;
    }}
</style>
""", unsafe_allow_html=True)

# Rutas de archivos
ROADMAP_PATH = "data/roadmap.json"
PROGRESS_PATH = "data/progress.json"

# Cargar datos
@st.cache_data
def load_roadmap():
    if os.path.exists(ROADMAP_PATH):
        with open(ROADMAP_PATH, "r") as f:
            return json.load(f)
    return []

def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, "r") as f:
            data = json.load(f)
            # Soporte para formato antiguo (solo lista de IDs)
            if isinstance(data, list):
                return {day_id: {"note": "", "date": ""} for day_id in data}
            return data
    return {}

def save_progress(progress_dict):
    with open(PROGRESS_PATH, "w") as f:
        json.dump(progress_dict, f, indent=4)

# Inicializar estado
roadmap = load_roadmap()
if 'completed_days_v2' not in st.session_state:
    st.session_state.completed_days_v2 = load_progress()

# --- BITÁCORA EN SIDEBAR ---
with st.sidebar:
    st.divider()
    st.subheader("💾 Gestión de Datos")
    
    # Botón para descargar progreso
    progress_json = json.dumps(st.session_state.completed_days_v2, indent=4)
    st.download_button(
        label="📥 Descargar Respaldo",
        data=progress_json,
        file_name=f"roadmap_backup_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        help="Guarda tu progreso en un archivo en tu PC."
    )
    
    # Botón para cargar progreso
    uploaded_file = st.file_uploader("📤 Cargar Respaldo", type="json", help="Sube tu archivo de respaldo para recuperar tu progreso.")
    if uploaded_file is not None:
        try:
            restored_data = json.load(uploaded_file)
            if st.button("Confirmar Restauración"):
                st.session_state.completed_days_v2 = restored_data
                save_progress(restored_data)
                st.success("¡Progreso restaurado con éxito!")
                st.rerun()
        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")

    st.divider()
    st.subheader("📝 Bitácora de Notas")
    notes_count = sum(1 for d in st.session_state.completed_days_v2.values() if d.get("note"))
    if notes_count > 0:
        if st.checkbox("Ver mis notas"):
            for day_id, info in st.session_state.completed_days_v2.items():
                if info.get("note"):
                    st.markdown(f"""
                    <div style="background: {card_bg}; padding: 10px; border-radius: 8px; border-left: 3px solid #3b82f6; margin-bottom: 10px;">
                        <p style="font-size: 0.7rem; font-weight: bold; margin: 0;">ID: {day_id}</p>
                        <p style="font-size: 0.8rem; margin: 5px 0;">{info['note']}</p>
                        <p style="font-size: 0.6rem; color: {secondary_text}; margin: 0;">{info.get('date', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("No hay notas registradas aún.")

    # --- BOTÓN DE REINICIO CON CONFIRMACIÓN ---
    st.divider()
    if 'confirm_reset' not in st.session_state:
        st.session_state.confirm_reset = False

    if not st.session_state.confirm_reset:
        if st.button("🗑️ Reiniciar Todo el Progreso", help="Borra todas las tareas marcadas y tus notas."):
            st.session_state.confirm_reset = True
            st.rerun()
    else:
        st.warning("⚠️ ¿Estás seguro? Se borrarán todas tus notas y progreso.")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            if st.button("✅ SÍ, BORRAR", use_container_width=True):
                st.session_state.completed_days_v2 = {}
                save_progress({})
                st.session_state.confirm_reset = False
                st.success("¡Progreso borrado!")
                st.rerun()
        with col_res2:
            if st.button("❌ CANCELAR", use_container_width=True):
                st.session_state.confirm_reset = False
                st.rerun()

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; height: 100px; width: 100px; background: linear-gradient(to top right, #2563eb, #06b6d4); border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);">
        <span style="font-weight: 900; color: white; font-size: 2rem; letter-spacing: 0.05em;">JH</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <h1 style="margin: 0; padding: 0; font-weight: 900; letter-spacing: -0.025em; color: {text_color};">Jhojen Cloud DevOps</h1>
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="padding: 2px 8px; font-size: 10px; background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 6px; font-weight: bold; text-transform: uppercase;">TELEMÁTICA 5TO</span>
        <span class="secondary-text" style="font-size: 0.8rem;">Roadmap Planificador Diario Vacacional 2026</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- DASHBOARD STATS ---
total_days = sum(len(w['days']) for m in roadmap for w in m['weeks'])
completed_count = len(st.session_state.completed_days_v2)
progress_percent = int((completed_count / total_days) * 100) if total_days > 0 else 0

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown(f"""
    <div class="task-card">
        <h3 class="secondary-text" style="font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;">Progreso de Vacaciones</h3>
        <div style="display: flex; align-items: baseline; gap: 10px;">
            <span style="font-size: 2.5rem; font-weight: 900; color: {text_color};">{progress_percent}%</span>
            <span class="secondary-text" style="font-size: 0.9rem; font-weight: bold;">{completed_count} / {total_days} Días</span>
        </div>
        <div style="margin-top: 15px;">
            <div style="width: 100%; background-color: {card_border}; border-radius: 9999px; height: 8px;">
                <div style="width: {progress_percent}%; background-color: #3b82f6; height: 8px; border-radius: 9999px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown(f"""
    <div class="task-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h3 class="secondary-text" style="font-size: 0.7rem; font-weight: bold; text-transform: uppercase; letter-spacing: 0.1em;">Gestión de Energía</h3>
            <span style="color: #fbbf24;">⚡</span>
        </div>
        <ul class="secondary-text" style="font-size: 0.75rem; list-style-type: none; padding: 0; margin: 0;">
            <li style="margin-bottom: 5px;">• Calistenia diaria para canalizar estrés.</li>
            <li style="margin-bottom: 5px;">• Higiene de pantalla 30 min antes de dormir.</li>
            <li>• Dormir 7.5 horas innegociables.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown(f"""
    <div class="task-card">
        <h3 style="font-size: 0.7rem; font-weight: bold; color: #818cf8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;">Espejo de Superación</h3>
        <p class="secondary-text" style="font-size: 0.75rem; font-style: italic; line-height: 1.4;">
            "El único del grupo que hizo más de lo que hablaba y cumplió su promesa de superarse. De antisocial a líder con autoconfianza."
        </p>
        <div style="margin-top: 10px; display: flex; align-items: center; gap: 8px;">
            <div style="width: 6px; height: 6px; background-color: #6366f1; border-radius: 50%; box-shadow: 0 0 10px #6366f1;"></div>
            <span class="secondary-text" style="font-size: 9px; font-weight: bold;">ETHAN - Inspiración Mutua</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FILTERS ---
month_filter = st.sidebar.selectbox("Mes", ["Todos"] + [str(m['monthNum']) for m in roadmap])
type_filter = st.sidebar.selectbox("Tipo de Tarea", ["Todas", "Estudio", "Proyecto", "Negocio", "Descanso"])

# --- TIMELINE ---
for month in roadmap:
    if month_filter != "Todos" and str(month['monthNum']) != month_filter:
        continue
        
    st.markdown(f"""
    <div style="margin-top: 2rem; border-bottom: 1px solid {divider_color}; padding-bottom: 0.5rem;">
        <h2 style="font-weight: 900; font-size: 1.5rem; color: {text_color};">
            <span style="color: #3b82f6; font-family: 'Geist Mono';">0{month['monthNum']}.</span> {month['monthName']}
        </h2>
        <p class="secondary-text" style="font-size: 0.8rem; font-style: italic;">{month['monthMeta']}</p>
    </div>
    """, unsafe_allow_html=True)

    for week in month['weeks']:
        filtered_days = [d for d in week['days'] if type_filter == "Todas" or d['type'] == type_filter]
        
        if not filtered_days:
            continue
            
        st.markdown(f"<h3 style='font-size: 0.8rem; font-weight: bold; color: {text_color}; text-transform: uppercase; margin: 1.5rem 0 1rem 0; background: {card_bg}; border: 1px solid {card_border}; display: inline-block; padding: 4px 12px; border-radius: 8px;'>{week['weekTitle']}</h3>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, day in enumerate(filtered_days):
            with cols[i % 3]:
                day_id = day['id']
                is_completed = day_id in st.session_state.completed_days_v2
                badge_class = f"badge-{day['type'].lower()}"
                
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid {'#10b981' if is_completed else card_border}; background-color: {'rgba(16, 185, 129, 0.05)' if is_completed else card_bg}; padding: 1rem; border-radius: 1rem; height: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span class="secondary-text" style="font-size: 0.7rem; font-weight: bold;">{day['dayName']} - <span class="mono">{day['date']}</span></span>
                            <span class="badge {badge_class}">{day['type']}</span>
                        </div>
                        <h4 style="font-size: 0.9rem; font-weight: 800; color: {text_color}; margin-bottom: 0.5rem;">{day['title']}</h4>
                        <p class="secondary-text" style="font-size: 0.75rem; margin-bottom: 1rem; line-height: 1.4;">{day['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Logica de completado con Nota
                    if st.checkbox("Completado", value=is_completed, key=f"check_{day_id}"):
                        if not is_completed:
                            # Pop-over de nota
                            with st.expander("📝 Añadir nota de aprendizaje (opcional)", expanded=True):
                                note = st.text_area("¿Qué aprendiste hoy?", key=f"note_{day_id}")
                                if st.button("Guardar Tarea", key=f"btn_{day_id}"):
                                    st.session_state.completed_days_v2[day_id] = {
                                        "note": note,
                                        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                                    }
                                    save_progress(st.session_state.completed_days_v2)
                                    st.rerun()
                    else:
                        if is_completed:
                            del st.session_state.completed_days_v2[day_id]
                            save_progress(st.session_state.completed_days_v2)
                            st.rerun()

st.markdown(f"""
<div style="margin-top: 4rem; border-top: 1px solid {divider_color}; padding-top: 2rem; text-align: center; color: {secondary_text}; font-size: 0.7rem;">
    <p>Jhojen DevOps Cloud Planner v2.0 (Streamlit Edition)</p>
    <p>"El contador de sexto año ha iniciado. Prepárate hoy para liderar mañana."</p>
</div>
""", unsafe_allow_html=True)
