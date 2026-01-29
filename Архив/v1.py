import streamlit as st
import math
import datetime

# === КОНФИГУРАЦИЯ ===
st.set_page_config(page_title="Езотерична Карта", layout="wide", initial_sidebar_state="expanded")

# === ДАННИ ===
DAYS = [str(i) for i in range(1, 32)]
MONTHS = ["Януари", "Февруари", "Март", "Април", "Май", "Юни", "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"]
YEARS_BIRTH = [str(i) for i in range(1900, 2028)]

# Съкратени имена за малките кръгчета на телефона
modules = [
    {"key": "Western", "name": "ЗАПАДНА АСТРОЛОГИЯ", "short": "ЗАП", "color": "#1E90FF"},
    {"key": "Vedic", "name": "ВЕДИЧЕСКИ ДЖЙОТИШ", "short": "ВЕД", "color": "#FF8C00"},
    {"key": "Bazi", "name": "КИТАЙСКИ БА ДЗИ", "short": "БАД", "color": "#DC143C"},
    {"key": "Astrosofia", "name": "ЗВЕЗДНА АСТРОСОФИЯ", "short": "АСТ", "color": "#9932CC"},
    {"key": "Numerology", "name": "УНИВЕРСАЛНА НУМЕРОЛОГИЯ", "short": "НУМ", "color": "#2E8B57"},
    {"key": "Palmistry", "name": "ХИРОМАНТИЯ", "short": "ХИР", "color": "#00CED1"},
    {"key": "Matrix", "name": "ЯПОНСКА МАТРИЦА", "short": "МАТ", "color": "#FF69B4"},
    {"key": "Hermetic", "name": "ЕГИПЕТСКИ ХЕРМЕТИЗЪМ", "short": "ХЕР", "color": "#B8860B"},
    {"key": "Oracle", "name": "ОРАКУЛЕН СИНТЕЗ", "short": "ОРА", "color": "#4B0082"},
    {"key": "Center", "name": "ВЪРХОВНАТА ИСТИНА", "short": "ИСТИНА", "color": "#FFD700"}
]
modules_dict = {m['key']: m for m in modules}

# === ФУНКЦИИ ===
def render_date_selectors(key_prefix):
    c_d, c_m, c_y = st.columns([1, 2, 1])
    with c_d: d = st.selectbox("Ден", DAYS, key=f"{key_prefix}_d")
    with c_m: m = st.selectbox("Месец", MONTHS, key=f"{key_prefix}_m")
    with c_y: y = st.selectbox("Година", YEARS_BIRTH, key=f"{key_prefix}_y")
    return d, m, y

def render_main_user_smart_form(key_context):
    if st.session_state.get('main_user'):
        u = st.session_state.main_user
        st.success(f"👤 {u['name']}")
        if st.button("🔄 Нов", key=f"reset_{key_context}"):
            st.session_state.main_user = None
            st.rerun()
    else:
        st.info("Въведи данни...")

# === ИНИЦИАЛИЗАЦИЯ ===
params = st.query_params
if 'current_view' not in st.session_state: st.session_state['current_view'] = 'HOME'
if 'show_form' not in st.session_state: st.session_state['show_form'] = False
if 'start_horoscope' not in st.session_state: st.session_state['start_horoscope'] = False
if 'astro_section' not in st.session_state: st.session_state['astro_section'] = 'menu'
if 'main_user' not in st.session_state: st.session_state['main_user'] = None

if "view" in params:
    st.session_state['current_view'] = params["view"]

# === CSS ДИЗАЙН ===
bg_url = "https://hicomm.bg/uploads/articles/202202/69095/mainimage-eto-kolko-sa-zvezdite-v-nashata-galaktika-i-v-cyalata-vselena.jpg?1643808921546"

st.markdown(f"""
<style>
    .block-container {{ padding-top: 0px !important; margin-top: 0px !important; max-width: 100% !important; }}
    header[data-testid="stHeader"] {{ display: none !important; }} 
    footer {{ display: none !important; }}
    
    .stApp {{
        background-image: url('{bg_url}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* === СТРОГО РАЗДЕЛЯНЕ === */
    .desktop-view {{ display: block !important; width: 100%; }}
    .mobile-view {{ display: none !important; }}

    @media only screen and (max-width: 900px) {{
        .desktop-view {{ display: none !important; }}
        .mobile-view {{ display: block !important; width: 100%; height: 100vh; overflow: hidden; position: relative; }}
        
        /* СКРИВАНЕ НА МЕНЮТО (АДМИНИСТРАТОР) ПРИ МОБИЛНИ */
        section[data-testid="stSidebar"] {{ display: none !important; }}
        button[data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}
    }}

    /* === DESKTOP STYLES (Старата мандала) === */
    .mandala-wrapper {{ width: 100%; height: 90vh; display: flex; justify-content: center; align-items: center; padding-top: 20px; }}
    .mandala-box {{ position: relative; width: 1000px; height: 700px; }}

    .ellipse-node {{
        position: absolute; width: 190px; height: 55px; 
        border-radius: 50%; display: flex; justify-content: center; align-items: center;
        color: white !important; font-weight: bold; font-size: 12px; z-index: 200; 
        border: 2px solid rgba(255,255,255,0.9); text-decoration: none !important;
        backdrop-filter: blur(5px);
    }}
    .center-circle {{
        position: absolute; width: 150px; height: 150px; border-radius: 50%;
        background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%);
        display: flex; justify-content: center; align-items: center;
        color: black !important; font-weight: 900; z-index: 210; 
        border: 5px solid white; font-size: 14px; animation: pulse 3s infinite;
        text-decoration: none !important;
    }}

    /* === MOBILE STYLES (Новият Компас) === */
    .mob-container {{
        position: relative; width: 360px; height: 400px; margin: 50px auto 0 auto;
    }}
    
    .mob-sun {{
        position: absolute; width: 100px; height: 100px; border-radius: 50%;
        background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%);
        left: 130px; top: 150px; /* Център на контейнера */
        display: flex; justify-content: center; align-items: center;
        border: 4px solid white; box-shadow: 0 0 20px #FFD700; z-index: 10;
        color: black !important; font-weight: bold; font-size: 12px; text-align: center;
    }}

    .mob-planet {{
        position: absolute; width: 55px; height: 55px; border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        color: white !important; font-weight: bold; font-size: 10px; z-index: 20;
        border: 2px solid rgba(255,255,255,0.8);
        backdrop-filter: blur(4px);
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); box-shadow: 0 0 30px #FFD700; }}
        50% {{ transform: scale(1.05); box-shadow: 0 0 80px #FFD700; }}
    }}
</style>
""", unsafe_allow_html=True)

# === СТРАНИЧНА ЛЕНТА ===
with st.sidebar:
    if st.session_state['current_view'] == 'HOME':
        st.markdown("<br>", unsafe_allow_html=True) 
        st.info("🔐 АДМИНИСТРАТОР")
        st.text_input("Потребител")
        st.text_input("Парола", type="password")
        st.button("ВХОД")
    else:
        if st.button("🏠 КЪМ ГАЛАКТИКАТА"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()

# === ГЛАВНА СТРАНИЦА ===
if st.session_state['current_view'] == 'HOME':
    
    # --- 1. ДЕСКТОП (Широка Мандала) ---
    desktop_html = ['<div class="desktop-view">']
    desktop_html.append('<div style="text-align:center; margin-top:10px;"><h1 style="color:white; text-shadow:0 0 10px gold;">СВЕТОВНА КАРТА НА ЕЗОТЕРИКАТА</h1></div>')
    desktop_html.append('<div class="mandala-wrapper"><div class="mandala-box">')
    
    # Линии (Desktop)
    desktop_html.append('<svg width="1000" height="700" style="position: absolute; top:0; left:0; z-index:1;">')
    desktop_html.append('<defs><marker id="arrowhead" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0, 12 4, 0 8" fill="#FFD700" /></marker></defs>')
    c_x, c_y, r_x, r_y = 500, 360, 350, 200
    for i in range(9):
        angle = math.radians(i * (360/9) - 90)
        x1 = c_x + (r_x - 30) * math.cos(angle)
        y1 = c_y + (r_y - 15) * math.sin(angle)
        x2 = c_x + 85 * math.cos(angle)
        y2 = c_y + 85 * math.sin(angle)
        desktop_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="2" marker-end="url(#arrowhead)" />')
    desktop_html.append('</svg>')

    # Слънце (Desktop)
    center = modules[9]
    desktop_html.append(f'<a href="?view={center["key"]}" target="_self" class="center-circle" style="left: 425px; top: 285px;">{center["name"]}</a>')

    # Планети (Desktop)
    for i in range(9):
        m = modules[i]
        angle = math.radians(i * (360/9) - 90)
        x = (c_x + r_x * math.cos(angle)) - 95 
        y = (c_y + r_y * math.sin(angle)) - 27.5
        desktop_html.append(f'<a href="?view={m["key"]}" target="_self" class="ellipse-node" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["name"]}</a>')

    desktop_html.append('</div></div></div>')
    st.markdown("".join(desktop_html), unsafe_allow_html=True)


    # --- 2. МОБИЛЕН (Сбит Компас) ---
    mobile_html = ['<div class="mobile-view">']
    mobile_html.append('<div class="mob-container">')
    
    # Мобилни координати (Център на контейнера)
    mob_cx, mob_cy = 155, 175
    mob_radius = 125 # Разстояние на планетите от слънцето

    # Линии (Mobile - по-тънки)
    mobile_html.append('<svg width="360" height="400" style="position: absolute; top:0; left:0; z-index:1;">')
    for i in range(9):
        angle = math.radians(i * (360/9) - 90)
        x1 = (mob_cx + 25) + (mob_radius - 25) * math.cos(angle) 
        y1 = (mob_cy + 25) + (mob_radius - 25) * math.sin(angle)
        x2 = (mob_cx + 25) + 35 * math.cos(angle)
        y2 = (mob_cy + 25) + 35 * math.sin(angle)
        mobile_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="1" opacity="0.6" />')
    mobile_html.append('</svg>')

    # Слънце (Mobile)
    mobile_html.append(f'<div class="mob-sun">ВЪРХОВНАТА<br>ИСТИНА</div>')

    # Планети (Mobile - Кръгли)
    for i in range(9):
        m = modules[i]
        angle = math.radians(i * (360/9) - 90)
        x = mob_cx + mob_radius * math.cos(angle)
        y = mob_cy + mob_radius * math.sin(angle)
        
        mobile_html.append(f'<div class="mob-planet" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["short"]}</div>')

    mobile_html.append('</div></div>') # Край на mob-container и mobile-view
    st.markdown("".join(mobile_html), unsafe_allow_html=True)

# === ВЪТРЕШНИ СТРАНИЦИ ===
else:
    # Засега просто placeholder
    key = st.session_state['current_view']
    mod = modules_dict.get(key, modules[0])
    st.markdown(f"""<div style="text-align: center; margin-top:50px;"><h1 style="color:{mod['color']};">{mod['name']}</h1></div>""", unsafe_allow_html=True)
    if st.button("⬅️ НАЗАД"):
        st.session_state['current_view'] = 'HOME'
        st.rerun()