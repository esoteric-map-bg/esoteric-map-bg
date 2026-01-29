import streamlit as st
import math
import datetime

# === ИНИЦИАЛИЗАЦИЯ НА STATE ПРЕДИ ВСИЧКО ===
if 'current_view' not in st.session_state: st.session_state['current_view'] = 'HOME'
if 'start_horoscope' not in st.session_state: st.session_state['start_horoscope'] = False
if 'astro_section' not in st.session_state: st.session_state['astro_section'] = 'menu'
if 'main_user' not in st.session_state: st.session_state['main_user'] = None

# Проверка на URL параметри
params = st.query_params
if "view" in params:
    st.session_state['current_view'] = params["view"]

# === КОНФИГУРАЦИЯ ===
# Важно: initial_sidebar_state се контролира динамично
sidebar_state = "expanded" if st.session_state['current_view'] == 'HOME' else "collapsed"
st.set_page_config(page_title="Езотерична Карта", layout="wide", initial_sidebar_state=sidebar_state)

# === ДАННИ ===
DAYS = [str(i) for i in range(1, 32)]
MONTHS = ["Януари", "Февруари", "Март", "Април", "Май", "Юни", "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"]
YEARS_BIRTH = [str(i) for i in range(1900, 2028)]

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
def render_main_user_smart_form(key_context):
    if st.session_state.get('main_user'):
        u = st.session_state.main_user
        st.success(f"👤 {u['name']}")
        if st.button("🔄 Нов", key=f"reset_{key_context}"):
            st.session_state.main_user = None
            st.rerun()
    else:
        st.info("Въведи данни...")

# === ЛОГИКА ЗА СКРИВАНЕ НА МЕНЮТО ===
# Ако сме на HOME -> 'block' (вижда се). Ако не сме -> 'none' (скрито напълно).
menu_display = "block" if st.session_state['current_view'] == 'HOME' else "none"

# === CSS ДИЗАЙН ===
bg_url = "https://hicomm.bg/uploads/articles/202202/69095/mainimage-eto-kolko-sa-zvezdite-v-nashata-galaktika-i-v-cyalata-vselena.jpg?1643808921546"

st.markdown(f"""
<style>
    .block-container {{ padding-top: 0px !important; margin-top: 0px !important; max-width: 100% !important; }}
    footer {{ display: none !important; }}
    
    .stApp {{
        background-image: url('{bg_url}');
        background-size: cover; background-position: center; background-attachment: fixed;
    }}

    /* === ЖЕЛЕЗЕН КОНТРОЛ НА МЕНЮТО === */
    section[data-testid="stSidebar"] {{
        display: {menu_display} !important;
    }}
    
    /* Скриваме и хедъра с бутона за менюто, когато не сме на HOME */
    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 60px !important;
        display: {menu_display} !important; 
    }}

    /* === СТРОГО РАЗДЕЛЯНЕ === */
    .desktop-view {{ display: block !important; width: 100%; }}
    .mobile-view {{ display: none !important; }}

    /* === ПРАВИЛА ЗА ТЕЛЕФОН (ПОД 900px) === */
    @media only screen and (max-width: 900px) {{
        .desktop-view {{ display: none !important; }}
        .mobile-view {{ display: block !important; width: 100%; height: 100vh; overflow: hidden; position: relative; }}
        
        /* НА ТЕЛЕФОН МЕНЮТО Е ВИНАГИ СКРИТО */
        section[data-testid="stSidebar"] {{ display: none !important; }}
        header[data-testid="stHeader"] {{ display: none !important; }}
    }}

    /* === DESKTOP STYLES === */
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

    /* === MOBILE STYLES (С КОРЕКЦИИ ПО СНИМКАТА) === */
    .mob-container {{
        position: relative; width: 360px; height: 500px; margin: 20px auto 0 auto;
    }}
    
    .mob-sun {{
        position: absolute; 
        width: 100px; height: 100px; 
        border-radius: 50%;
        background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%);
        left: 130px; top: 180px; 
        display: flex; justify-content: center; align-items: center;
        border: 4px solid white; box-shadow: 0 0 20px #FFD700; z-index: 10;
        color: black !important; font-weight: bold; font-size: 11px; text-align: center;
    }}

    .mob-planet {{
        position: absolute; 
        width: 70px; height: 40px; 
        border-radius: 50%;
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

# === СТРАНИЧНА ЛЕНТА (Вижда се само на PC HOME) ===
with st.sidebar:
    if st.session_state['current_view'] == 'HOME':
        st.markdown("<br>", unsafe_allow_html=True) 
        st.info("🔐 АДМИНИСТРАТОР")
        st.text_input("Потребител")
        st.text_input("Парола", type="password")
        st.button("ВХОД")

# === ГЛАВНА СТРАНИЦА ===
if st.session_state['current_view'] == 'HOME':
    
    # --- 1. ДЕСКТОП ---
    desktop_html = ['<div class="desktop-view">']
    desktop_html.append('<div style="text-align:center; margin-top:10px;"><h1 style="color:white; text-shadow:0 0 10px gold;">СВЕТОВНА КАРТА НА ЕЗОТЕРИКАТА</h1></div>')
    desktop_html.append('<div class="mandala-wrapper"><div class="mandala-box">')
    
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

    center = modules[9]
    desktop_html.append(f'<a href="?view={center["key"]}" target="_self" class="center-circle" style="left: 425px; top: 285px;">{center["name"]}</a>')

    for i in range(9):
        m = modules[i]
        angle = math.radians(i * (360/9) - 90)
        x = (c_x + r_x * math.cos(angle)) - 95 
        y = (c_y + r_y * math.sin(angle)) - 27.5
        desktop_html.append(f'<a href="?view={m["key"]}" target="_self" class="ellipse-node" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["name"]}</a>')

    desktop_html.append('</div></div></div>')
    st.markdown("".join(desktop_html), unsafe_allow_html=True)


    # --- 2. МОБИЛЕН (С КОРЕКЦИИ ПО СНИМКАТА) ---
    mobile_html = ['<div class="mobile-view">']
    mobile_html.append('<div class="mob-container">')
    
    mob_cx, mob_cy = 155, 175
    mob_radius_x = 115 
    mob_radius_y = 160 

    # КОРЕКЦИИ:
    # 0 (Горе): -90
    # 1 (Дясно горе - ВЕД): Беше -50 -> Правим -45 (По-близо до центъра/горе) ЧЕРВЕНО
    # 2 (Дясно - БАД): Беше -10 -> Правим -15 (Леко нагоре)
    # 3 (Дясно долу - АСТ): Беше 28 -> Правим 25 (Леко нагоре) ЧЕРВЕНО
    # 4 (ДЯСНО ДЪНО - БАД): Искаш го НАДЯСНО (СИНЬО). Беше 75 -> Правим 60.
    # 5 (ЛЯВО ДЪНО - ХИР): Искаш го НАЛЯВО (СИНЬО). Беше 105 -> Правим 120.
    # 6 (Ляво долу): 155
    # 7 (Ляво): 195
    # 8 (Ляво горе - ОРА): 230 -> 225 (По-близо до центъра/горе) ЧЕРВЕНО
    
    manual_angles = [-90, -45, -15, 25, 60, 120, 155, 195, 225]

    mobile_html.append('<svg width="360" height="500" style="position: absolute; top:0; left:0; z-index:1;">')
    for i in range(9):
        angle = math.radians(manual_angles[i])
        sx = mob_cx + 25
        sy = mob_cy + 55
        
        x1 = sx + (mob_radius_x - 30) * math.cos(angle)
        y1 = sy + (mob_radius_y - 20) * math.sin(angle)
        x2 = sx + 25 * math.cos(angle)
        y2 = sy + 25 * math.sin(angle)
        mobile_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="1" opacity="0.6" />')
    mobile_html.append('</svg>')

    mobile_html.append(f'<div class="mob-sun">ВЪРХОВНАТА<br>ИСТИНА</div>')

    for i in range(9):
        m = modules[i]
        angle = math.radians(manual_angles[i])
        x = mob_cx + mob_radius_x * math.cos(angle) - 10
        y = mob_cy + 35 + mob_radius_y * math.sin(angle)
        
        mobile_html.append(f'<div class="mob-planet" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["short"]}</div>')

    mobile_html.append('</div></div>') 
    st.markdown("".join(mobile_html), unsafe_allow_html=True)

# === ВЪТРЕШНИ СТРАНИЦИ ===
else:
    key = st.session_state['current_view']
    mod = modules_dict.get(key, modules[0])

    if key == "Western":
        if st.session_state.get('start_horoscope', False):
            # ФОРМА
            st.markdown("""<style>.stApp { background-image: none !important; background-color: #000000 !important; } .block-container { max-width: 100% !important; padding: 2rem 5rem !important; }</style>""", unsafe_allow_html=True)
            if st.button("⬅️ НАЗАД", key="back_form"):
                st.session_state['start_horoscope'] = False
                st.rerun()
                
            st.title("👤 ЛИЧЕН АНАЛИЗ")
            render_main_user_smart_form("natal")
            
        else:
            # СТРАНИЦА С МОМИЧЕТО (ЧИСТА - БЕЗ СТРАНИЧНО МЕНЮ)
            st.markdown("""
            <style>
                .stApp { background-color: #000000 !important; }
                .block-container { padding: 0 !important; max-width: 100% !important; }
                [data-testid="stImage"] > img { height: 85vh !important; width: 100% !important; object-fit: cover !important; }
                div.stButton > button { position: relative !important; z-index: 99999 !important; top: -80px !important; margin: 0 auto; display: block; }
            </style>
            """, unsafe_allow_html=True)
            
            # ИЗРИЧНО БУТОН ЗА ВРЪЩАНЕ - РАБОТЕЩ
            st.markdown("""
                <a href="?view=HOME" target="_self" style="position: absolute; top: 20px; left: 20px; z-index: 999999; text-decoration: none;">
                    <div style="background: rgba(0,0,0,0.6); color: #FFD700; padding: 10px 20px; border-radius: 10px; border: 2px solid #FFD700; font-weight: bold; font-size: 16px; display: flex; align-items: center; gap: 5px; box-shadow: 0 0 10px black;">
                        ⬅️ НАЗАД
                    </div>
                </a>
            """, unsafe_allow_html=True)

            try:
                st.image("galaxy.png", use_container_width=True)
            except:
                st.error("⚠️ Снимката 'galaxy.png' липсва!")
            
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                st.markdown(f"""<style>div.stButton > button {{ background: {mod['color']}; color: black !important; font-size: 18px; padding: 12px; width: 100%; border-radius: 15px; border: 2px solid white; }}</style>""", unsafe_allow_html=True)
                if st.button("✨ ЗАПОЧНИ СВОЯ ХОРОСКОП ✨", use_container_width=True):
                    st.session_state['start_horoscope'] = True
                    st.rerun()

    else:
        # Други модули
        st.markdown(f"""<div style="text-align: center; margin-top:50px;"><h1 style="color:{mod['color']};">{mod['name']}</h1></div>""", unsafe_allow_html=True)
        # Бутон за връщане
        st.markdown("""
            <a href="?view=HOME" target="_self" style="display: block; width: 100px; margin: 20px auto; text-align: center; background: #333; color: white; padding: 10px; border-radius: 5px; text-decoration: none;">
                🏠 НАЧАЛО
            </a>
        """, unsafe_allow_html=True)