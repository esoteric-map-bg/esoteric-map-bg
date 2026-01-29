
import streamlit as st
import math
import datetime
import sys
import pandas as pd
from pathlib import Path

# ==============================================================================
# 0. BACKEND SETUP
# ==============================================================================
backend_path = Path(__file__).parent / "backend"
if str(backend_path) not in sys.path:
    sys.path.insert(0, str(backend_path))

try:
    from astro_engine_v1 import NatalChart
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

# ==============================================================================
# 1. КОНФИГУРАЦИЯ & ДАННИ
# ==============================================================================
st.set_page_config(page_title="Езотерична Карта", layout="wide", initial_sidebar_state="expanded")

# SESSION STATE HARD RESET LOGIC
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# URL PARAMETER HANDLING (Прихваща кликовете от Мандалата)
params = st.query_params
if "view" in params:
    view_target = params["view"]
    if view_target == "Western":
        # Ако е Западна, отиваме първо в ИНТРОТО
        if st.session_state['page'] != 'intro' and st.session_state['page'] != 'calculator':
            st.session_state['page'] = 'intro'
    elif view_target == "Center":
         # Центърът може да води другаде или да стои в Home
         pass
    else:
         # За другите модули
         st.session_state['page'] = 'module_wip'
         st.session_state['current_module_name'] = view_target

# CONSTANTS
DAYS = [str(i) for i in range(1, 32)]
MONTHS = ["Януари", "Февруари", "Март", "Април", "Май", "Юни", "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"]
YEARS_BIRTH = [str(i) for i in range(1900, 2028)]

modules = [
    {"key": "Western", "name": "ЗАПАДНА АСТРОЛОГИЯ", "color": "#1E90FF"},
    {"key": "Vedic", "name": "ВЕДИЧЕСКИ ДЖЙОТИШ", "color": "#FF8C00"},
    {"key": "Bazi", "name": "КИТАЙСКИ БА ДЗИ", "color": "#DC143C"},
    {"key": "Astrosofia", "name": "ЗВЕЗДНА АСТРОСОФИЯ", "color": "#9932CC"},
    {"key": "Numerology", "name": "УНИВЕРСАЛНА НУМЕРОЛОГИЯ", "color": "#2E8B57"},
    {"key": "Palmistry", "name": "ХИРОМАНТИЯ", "color": "#00CED1"},
    {"key": "Matrix", "name": "ЯПОНСКА МАТРИЦА", "color": "#FF69B4"},
    {"key": "Hermetic", "name": "ЕГИПЕТСКИ ХЕРМЕТИЗЪМ", "color": "#B8860B"},
    {"key": "Oracle", "name": "ОРАКУЛЕН СИНТЕЗ", "color": "#4B0082"},
    {"key": "Center", "name": "ВЪРХОВНАТА ИСТИНА", "color": "#FFD700"}
]
modules_dict = {m['key']: m for m in modules}

# ==============================================================================
# 2. CSS STYLES (ОРИГИНАЛ ОТ ВЕРСИЯ 4 + SIDEBAR FIX)
# ==============================================================================
bg_url = "https://hicomm.bg/uploads/articles/202202/69095/mainimage-eto-kolko-sa-zvezdite-v-nashata-galaktika-i-v-cyalata-vselena.jpg?1643808921546"

def load_custom_css():
    st.markdown(f"""
    <style>
        .block-container {{ padding-top: 35px !important; max-width: 100% !important; }}
        header[data-testid="stHeader"] {{ background: transparent !important; height: 30px !important; }}
        footer {{ visibility: hidden !important; }}
        
        .stApp {{
            background-image: url('{bg_url}');
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        .top-header {{
            position: fixed; top: 0; left: 0; width: 100%; height: 30px;
            background: rgba(0,0,0,0.85); z-index: 999;
            display: flex; justify-content: center; align-items: center; border-bottom: 2px solid #FFD700;
        }}
        .top-header h1 {{
            color: #FFD700; margin-left: 290px;
            font-size: 1.2rem; letter-spacing: 2px; text-shadow: 0 0 5px #FFD700;
        }}
        
        /* MANDALA CSS */
        .mandala-wrapper {{ width: 100%; height: 90vh; display: flex; justify-content: center; align-items: center; }}
        .mandala-box {{ position: relative; width: 1000px; height: 700px; }}
        
        .ellipse-node {{
            position: absolute; width: 190px; height: 55px; border-radius: 50%;
            display: flex; justify-content: center; align-items: center;
            color: white !important; font-weight: bold; font-size: 12px; z-index: 200;
            border: 2px solid rgba(255,255,255,0.9); text-decoration: none !important;
            backdrop-filter: blur(5px); transition: all 0.3s;
        }}
        .ellipse-node:hover {{ transform: scale(1.1); box-shadow: 0 0 30px gold; border-color: #FFD700; color: #FFD700 !important; cursor: pointer; }}
        
        .center-circle {{
            position: absolute; width: 150px; height: 150px; border-radius: 50%;
            background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%);
            display: flex; justify-content: center; align-items: center;
            color: black !important; font-weight: 900; z-index: 210;
            border: 5px solid white; font-size: 14px; animation: pulse 3s infinite; text-decoration: none !important;
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 30px #FFD700; }}
            50% {{ transform: scale(1.05); box-shadow: 0 0 80px #FFD700; }}
        }}
        
        /* GLASS PANEL */
        .glass-panel {{
            background: rgba(0, 0, 0, 0.75); backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 215, 0, 0.4); border-radius: 15px;
            padding: 20px; margin-bottom: 20px;
        }}
        
        /* MOBILE OPTIMIZATIONS */
        @media only screen and (max-width: 900px) {{
            svg {{ width: 100vw !important; height: auto !important; position: relative !important; }}
            .mandala-box {{ transform: scale(0.35); transform-origin: top center; width: 1000px !important; margin-left: -500px; left: 50%; height: 700px !important; margin-top: 50px; }}
            .mandala-wrapper {{ height: 450px !important; overflow: hidden !important; display: block !important; }}
            /* Скриваме сайдбара само на мобилни, за да не пречи */
            section[data-testid="stSidebar"] {{ display: none !important; }} 
        }}
    </style>
    """, unsafe_allow_html=True)

# ==============================================================================
# 3. COMPONENT FUNCTIONS
# ==============================================================================

def render_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; color:#FFD700;'>ASTRO LOGOS</h2>", unsafe_allow_html=True)
        
        # 4. БУТОН ЗА СПАСЕНИЕ (RESET)
        if st.button("🏠 КЪМ НАЧАЛО (RESET)", use_container_width=True):
            st.session_state['page'] = 'home'
            st.query_params.clear()
            st.rerun()

        st.markdown("---")
        st.info("🔐 АДМИНИСТРАТОР")
        st.text_input("Потребител")
        st.text_input("Парола", type="password")
        st.button("ВХОД")
        
        st.markdown("---")
        st.markdown("<p style='color: #FFD700; text-align:center;'>БЪРЗ ДОСТЪП</p>", unsafe_allow_html=True)
        for m in modules:
             st.markdown(f"<a href='?view={m['key']}' target='_self' style='text-decoration:none; display:block; background:{m['color']}; color:white; padding:5px; margin:2px; border-radius:5px; text-align:center;'>{m['name']}</a>", unsafe_allow_html=True)

def render_home_page():
    # ЕКСТРАКЦИЯ ОТ АРХИВ/ВЕР 4.PY
    st.markdown('<div class="top-header"><h1>СВЕТОВНА КАРТА НА ЕЗОТЕРИКАТА</h1></div>', unsafe_allow_html=True)
    
    center_x, center_y = 500, 360 
    radius_x, radius_y = 350, 200

    m_html = ['<div class="mandala-wrapper"><div class="mandala-box">']
    m_html.append('<svg width="1000" height="700" viewBox="0 0 1000 700" style="position: absolute; top:0; left:0; z-index:1;">')
    m_html.append('<defs><marker id="arrowhead" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0, 12 4, 0 8" fill="#FFD700" /></marker></defs>')
    
    # Lines
    for i in range(9):
        angle = math.radians(i * (360/9) - 90)
        x1 = center_x + (radius_x - 30) * math.cos(angle)
        y1 = center_y + (radius_y - 15) * math.sin(angle)
        x2 = center_x + 85 * math.cos(angle)
        y2 = center_y + 85 * math.sin(angle)
        m_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="2" marker-end="url(#arrowhead)" />')
    m_html.append('</svg>')
    
    # Center
    center_mod = modules[9]
    m_html.append(f'<a href="?view={center_mod["key"]}" target="_self" class="center-circle" style="left: 425px; top: 285px;">{center_mod["name"]}</a>')
    
    # Ellipses
    for i in range(9):
        mod = modules[i]
        angle = math.radians(i * (360/9) - 90)
        x = (center_x + radius_x * math.cos(angle)) - 95 
        y = (center_y + radius_y * math.sin(angle)) - 27.5
        m_html.append(f'<a href="?view={mod["key"]}" target="_self" class="ellipse-node" style="background-color: {mod["color"]}; left: {x}px; top: {y}px;">{mod["name"]}</a>')

    m_html.append('</div></div>')
    st.markdown("".join(m_html), unsafe_allow_html=True)

def render_intro_page():
    # ФОН ЗА ИНТРО
    st.markdown("""
    <style>
        .stApp { background-image: none !important; background-color: #000000 !important; }
        .block-container { padding: 0 !important; max-width: 100% !important; }
        [data-testid="stImage"] > img { height: 85vh !important; width: 100% !important; object-fit: cover !important; }
    </style>
    """, unsafe_allow_html=True)
    
    try:
        st.image("galaxy.png", use_container_width=True)
    except:
        st.title("🌌")
    
    # Overlay button
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        if st.button("✨ ЗАПОЧНИ СВОЯ ХОРОСКОП ✨", type="primary", use_container_width=True):
            st.session_state['page'] = 'calculator'
            st.rerun()

def show_calculator_interface():
    # FORCING BLACK BACKGROUND FOR TOOLS
    st.markdown("""
    <style>
        .stApp { background-image: none !important; background-color: #050505 !important; }
        .block-container { max-width: 1200px !important; padding: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="top-header"><h1>ЗАПАДНА АСТРОЛОГИЯ</h1></div>', unsafe_allow_html=True)
    st.markdown('<div style="height: 60px;"></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.subheader("📝 Въведете данни")
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Име:", value="Client")
        city = st.text_input("Град:", value="Sofia, Bulgaria")
    with c2:
        date = st.date_input("Дата:", value=datetime.date(1990, 1, 1))
        time = st.time_input("Час:", value=datetime.time(12, 00))
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 ИЗЧИСЛИ КАРТАТА", type="primary", use_container_width=True):
        if not BACKEND_AVAILABLE:
            st.error("Backend engine not found!")
        else:
            with st.spinner("Изчисляване..."):
                try:
                    d_str = date.strftime("%Y-%m-%d")
                    t_str = time.strftime("%H:%M")
                    chart = NatalChart(d_str, t_str, lat=42.7, lon=23.3) # Hardcoded for now
                    
                    st.success(f"Картата за {name} е готова!")
                    
                    t1, t2 = st.tabs(["ПЛАНЕТИ", "ДОМОВЕ"])
                    with t1:
                        st.dataframe(pd.DataFrame(chart.planets).T, use_container_width=True)
                    with t2:
                        st.dataframe(pd.DataFrame(chart.houses).T, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Error: {e}")

# ==============================================================================
# 4. MAIN DISPATCHER
# ==============================================================================
def main():
    load_custom_css()
    render_sidebar()
    
    # DEBUG INFO (Може да се премахне по-късно)
    # st.write(f"Current State: {st.session_state['page']}")
    
    if st.session_state['page'] == 'home':
        render_home_page()
    elif st.session_state['page'] == 'intro':
        render_intro_page()
    elif st.session_state['page'] == 'calculator':
        show_calculator_interface()
    elif st.session_state['page'] == 'module_wip':
        st.title(f"Модул: {st.session_state.get('current_module_name', 'Unknown')}")
        st.info("В разработка...")
    else:
        # Fallback
        render_home_page()

if __name__ == "__main__":
    main()
