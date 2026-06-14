import streamlit as st
import json
import os

# Configuración de página
st.set_page_config(
    page_title="Jhojen Cloud DevOps Dashboard",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilo personalizado para emular Tailwind / Geist Mono
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist+Mono:wght@300;400;500;600;700&family=Geist:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Geist', sans-serif;
    }
    .mono {
        font-family: 'Geist Mono', monospace;
    }
    .stApp {
        background-color: #030712;
        color: #f1f5f9;
    }
    .task-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 1rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: border-color 0.3s;
    }
    .task-card:hover {
        border-color: #3b82f6;
    }
    .badge {
        font-size: 0.7rem;
        padding: 0.2rem 0.5rem;
        border-radius: 0.5rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    .badge-estudio { background-color: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }
    .badge-proyecto { background-color: rgba(245, 158, 11, 0.1); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.2); }
    .badge-negocio { background-color: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); }
    .badge-descanso { background-color: rgba(100, 116, 139, 0.1); color: #94a3b8; border: 1px solid rgba(100, 116, 139, 0.2); }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }
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
            return json.load(f)
    return []

def save_progress(completed_ids):
    with open(PROGRESS_PATH, "w") as f:
        json.dump(completed_ids, f)

# Inicializar estado
roadmap = load_roadmap()
if 'completed_days' not in st.session_state:
    st.session_state.completed_days = load_progress()

# --- HEADER ---
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; height: 100px; width: 100px; background: linear-gradient(to top right, #2563eb, #06b6d4); border-radius: 1rem; box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.2);">
        <span style="font-weight: 900; color: white; font-size: 2rem; letter-spacing: 0.05em;">JH</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <h1 style="margin: 0; padding: 0; font-weight: 900; letter-spacing: -0.025em; color: white;">Jhojen Cloud DevOps</h1>
    <div style="display: flex; align-items: center; gap: 10px;">
        <span style="padding: 2px 8px; font-size: 10px; background: rgba(16, 185, 129, 0.1); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 6px; font-weight: bold; text-transform: uppercase;">TELEMÁTICA 5TO</span>
        <span style="color: #94a3b8; font-size: 0.8rem;">Roadmap Planificador Diario Vacacional 2026</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- DASHBOARD STATS ---
total_days = sum(len(w['days']) for m in roadmap for w in m['weeks'])
completed_count = len(st.session_state.completed_days)
progress_percent = int((completed_count / total_days) * 100) if total_days > 0 else 0

stat_col1, stat_col2, stat_col3 = st.columns(3)

with stat_col1:
    st.markdown(f"""
    <div class="task-card">
        <h3 style="font-size: 0.7rem; font-weight: bold; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;">Progreso de Vacaciones</h3>
        <div style="display: flex; align-items: baseline; gap: 10px;">
            <span style="font-size: 2.5rem; font-weight: 900; color: white;">{progress_percent}%</span>
            <span style="font-size: 0.9rem; font-weight: bold; color: #64748b;">{completed_count} / {total_days} Días</span>
        </div>
        <div style="margin-top: 15px;">
            <div style="width: 100%; background-color: #1e293b; border-radius: 9999px; height: 8px;">
                <div style="width: {progress_percent}%; background-color: #3b82f6; height: 8px; border-radius: 9999px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with stat_col2:
    st.markdown("""
    <div class="task-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h3 style="font-size: 0.7rem; font-weight: bold; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em;">Gestión de Energía</h3>
            <span style="color: #fbbf24;">⚡</span>
        </div>
        <ul style="font-size: 0.75rem; color: #cbd5e1; list-style-type: none; padding: 0; margin: 0;">
            <li style="margin-bottom: 5px;">• Calistenia diaria para canalizar estrés.</li>
            <li style="margin-bottom: 5px;">• Higiene de pantalla 30 min antes de dormir.</li>
            <li>• Dormir 7.5 horas innegociables.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with stat_col3:
    st.markdown("""
    <div class="task-card">
        <h3 style="font-size: 0.7rem; font-weight: bold; color: #818cf8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 10px;">Espejo de Superación</h3>
        <p style="font-size: 0.75rem; color: #cbd5e1; font-style: italic; line-height: 1.4;">
            "El único del grupo que hizo más de lo que hablaba y cumplió su promesa de superarse. De antisocial a líder con autoconfianza."
        </p>
        <div style="margin-top: 10px; display: flex; align-items: center; gap: 8px;">
            <div style="width: 6px; height: 6px; background-color: #6366f1; border-radius: 50%; box-shadow: 0 0 10px #6366f1;"></div>
            <span style="font-size: 9px; color: #94a3b8; font-weight: bold;">ETHAN - Inspiración Mutua</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FILTERS ---
st.sidebar.title("Configuración")
month_filter = st.sidebar.selectbox("Mes", ["Todos"] + [str(m['monthNum']) for m in roadmap])
type_filter = st.sidebar.selectbox("Tipo de Tarea", ["Todas", "Estudio", "Proyecto", "Negocio", "Descanso"])

if st.sidebar.button("Reiniciar Progreso"):
    if st.sidebar.checkbox("Confirmar reinicio"):
        st.session_state.completed_days = []
        save_progress([])
        st.rerun()

# --- TIMELINE ---
for month in roadmap:
    # Filtro de mes
    if month_filter != "Todos" and str(month['monthNum']) != month_filter:
        continue
        
    st.markdown(f"""
    <div style="margin-top: 2rem; border-bottom: 1px solid #1e293b; padding-bottom: 0.5rem;">
        <h2 style="font-weight: 900; font-size: 1.5rem; color: white;">
            <span style="color: #3b82f6; font-family: 'Geist Mono';">0{month['monthNum']}.</span> {month['monthName']}
        </h2>
        <p style="color: #94a3b8; font-size: 0.8rem; font-style: italic;">{month['monthMeta']}</p>
    </div>
    """, unsafe_allow_html=True)

    for week in month['weeks']:
        # Filtrar días por tipo
        filtered_days = [d for d in week['days'] if type_filter == "Todas" or d['type'] == type_filter]
        
        if not filtered_days:
            continue
            
        st.markdown(f"<h3 style='font-size: 0.8rem; font-weight: bold; color: #cbd5e1; text-transform: uppercase; margin: 1.5rem 0 1rem 0; background: #0f172a; display: inline-block; padding: 4px 12px; border-radius: 8px;'>{week['weekTitle']}</h3>", unsafe_allow_html=True)
        
        # Grid de días
        cols = st.columns(3)
        for i, day in enumerate(filtered_days):
            with cols[i % 3]:
                is_completed = day['id'] in st.session_state.completed_days
                
                # Clase de badge
                badge_class = f"badge-{day['type'].lower()}"
                
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid {'#10b981' if is_completed else '#1e293b'}; background-color: {'rgba(16, 185, 129, 0.05)' if is_completed else 'rgba(15, 23, 42, 0.6)'}; padding: 1rem; border-radius: 1rem; height: 100%;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="font-size: 0.7rem; font-weight: bold; color: #94a3b8;">{day['dayName']} - <span class="mono">{day['date']}</span></span>
                            <span class="badge {badge_class}">{day['type']}</span>
                        </div>
                        <h4 style="font-size: 0.9rem; font-weight: 800; color: white; margin-bottom: 0.5rem;">{day['title']}</h4>
                        <p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 1rem; line-height: 1.4;">{day['desc']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # El checkbox de Streamlit para controlar el estado
                    if st.checkbox("Completado", value=is_completed, key=day['id']):
                        if day['id'] not in st.session_state.completed_days:
                            st.session_state.completed_days.append(day['id'])
                            save_progress(st.session_state.completed_days)
                            st.rerun()
                    else:
                        if day['id'] in st.session_state.completed_days:
                            st.session_state.completed_days.remove(day['id'])
                            save_progress(st.session_state.completed_days)
                            st.rerun()

st.markdown(f"""
<div style="margin-top: 4rem; border-top: 1px solid {divider_color}; padding-top: 2rem; text-align: center; color: {secondary_text}; font-size: 0.7rem;">
    <p>Jhojen DevOps Cloud Planner v2.0 (Streamlit Edition)</p>
    <p>"El contador de sexto año ha iniciado. Prepárate hoy para liderar mañana."</p>
</div>
""", unsafe_allow_html=True)
 mañana."</p>
</div>
""", unsafe_allow_html=True)
ml=True)
                    
                    # El checkbox de Streamlit para controlar el estado
                    if st.checkbox("Completado", value=is_completed, key=day['id']):
                        if day['id'] not in st.session_state.completed_days:
                            st.session_state.completed_days.append(day['id'])
                            save_progress(st.session_state.completed_days)
                            st.rerun()
                    else:
                        if day['id'] in st.session_state.completed_days:
                            st.session_state.completed_days.remove(day['id'])
                            save_progress(st.session_state.completed_days)
                            st.rerun()

st.markdown("""
<div style="margin-top: 4rem; border-top: 1px solid #1e293b; padding-top: 2rem; text-align: center; color: #64748b; font-size: 0.7rem;">
    <p>Jhojen DevOps Cloud Planner v2.0 (Streamlit Edition)</p>
    <p>"El contador de sexto año ha iniciado. Prepárate hoy para liderar mañana."</p>
</div>
""", unsafe_allow_html=True)
