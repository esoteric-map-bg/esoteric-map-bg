import streamlit as st
import math
import datetime
from PIL import UnidentifiedImageError

# Import horoscope logic from app.py
# Constants
DAYS = [str(i) for i in range(1, 32)]
MONTHS = ["Януари", "Февруари", "Март", "Април", "Май", "Юни", "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"]
YEARS_BIRTH = [str(i) for i in range(1900, 2028)]
YEARS_HISTORY = [str(i) for i in range(1950, 2051)]
YEARS_FUTURE = [str(i) for i in range(2025, 2041)]

# Functions from app.py
def render_date_selectors(key_prefix, mode="birth"):
    c_d, c_m, c_y = st.columns([1, 2, 1], gap="small")
    
    if mode == "birth":
        years_list = YEARS_BIRTH
    elif mode == "future":
        years_list = YEARS_FUTURE
    else: # history
        years_list = YEARS_HISTORY
    
    idx_d, idx_m, idx_y = None, None, None
    
    if mode != "birth":
        today = datetime.date.today()
        idx_d = DAYS.index(str(today.day))
        idx_m = today.month - 1
        curr_y_str = str(today.year)
        if curr_y_str in years_list: 
            idx_y = years_list.index(curr_y_str)
        elif mode == "future":
            idx_y = 0

    with c_d: d = st.selectbox("Ден", DAYS, index=idx_d, key=f"{key_prefix}_d", placeholder="Ден")
    with c_m: m = st.selectbox("Месец", MONTHS, index=idx_m, key=f"{key_prefix}_m", placeholder="Месец")
    with c_y: y = st.selectbox("Година", years_list, index=idx_y, key=f"{key_prefix}_y", placeholder="Година")
    return d, m, y

def render_person_form(key_suffix, show_header=True, label="Данни"):
    if show_header: st.subheader(label)
    c1, c2 = st.columns([2, 1])
    with c1: name = st.text_input("Име:", key=f"name_{key_suffix}")
    with c2: gender = st.radio("Пол:", ["👩 Жена", "👨 Мъж"], horizontal=True, key=f"gender_{key_suffix}", label_visibility="visible")
    st.write("Дата на раждане:")
    d, m, y = render_date_selectors(f"birth_{key_suffix}", mode="birth")
    c3, c4 = st.columns([1, 2])
    with c3: time_obj = st.time_input("Час:", value=None, key=f"time_{key_suffix}")
    with c4: city = st.text_input("Град на раждане:", key=f"city_{key_suffix}")
    return {"name": name, "gender": gender, "d": d, "m": m, "y": y, "time": time_obj, "city": city}

def render_main_user_smart_form(key_context):
    if st.session_state.get('main_user'):
        u = st.session_state.main_user
        st.success(f"👤 Използвам данни за: **{u['name']}** ({u['gender']})")
        with st.expander("ℹ️ Виж детайли или промени"):
            st.write(f"📅 {u['d']} {u['m']} {u['y']} ⏰ {u['time']} 🌍 {u['city']}")
            if st.button("🔄 Изчисти и въведи нов", key=f"reset_{key_context}"):
                st.session_state.main_user = None
                st.rerun()
        return u
    else:
        data = render_person_form(f"main_{key_context}", show_header=False)
        if data['name'] and data['d'] and data['m'] and data['y'] and data['city']:
            st.session_state.main_user = data
            st.rerun()
        return None

# 1. ГЛОБАЛНИ НАСТРОЙКИ
st.set_page_config(page_title="Езотерична Карта", layout="wide", initial_sidebar_state="expanded")

# --- ДАННИ ---
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

# --- ЛОГИКА ---
params = st.query_params

if 'current_view' not in st.session_state:
    st.session_state['current_view'] = 'HOME'
if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False
if 'start_horoscope' not in st.session_state:
    st.session_state['start_horoscope'] = False
if 'astro_section' not in st.session_state:
    st.session_state['astro_section'] = 'menu'
if 'main_user' not in st.session_state:
    st.session_state['main_user'] = None

if "view" in params:
    st.session_state['current_view'] = params["view"]
    if 'keep_form' in st.session_state:
        del st.session_state['keep_form']
    else:
        st.session_state['show_form'] = False

def go_home():
    st.session_state['current_view'] = 'HOME'
    st.session_state['show_form'] = False
    st.query_params.clear()

def toggle_form():
    st.session_state['show_form'] = True

# --- CSS ДИЗАЙН И МОБИЛНА АДАПТАЦИЯ ---
bg_url_main = "https://hicomm.bg/uploads/articles/202202/69095/mainimage-eto-kolko-sa-zvezdite-v-nashata-galaktika-i-v-cyalata-vselena.jpg?1643808921546"

st.markdown(f"""
<style>
    /* 1. ГЛОБАЛНИ СТИЛОВЕ */
    .block-container {{ 
        padding-top: 25px !important; 
        padding-bottom: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important; 
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
        visibility: visible !important;
        z-index: 1000;
        height: 30px !important; 
    }}
    
    /* 2. БУТОН ЗА МЕНЮТО (Хамбургер/Стрелка) */
    button[data-testid="stSidebarCollapsedControl"] {{
        display: block !important;
        color: #FFD700 !important;
        background-color: rgba(0,0,0,0.8) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 50% !important;
        width: 30px !important;
        height: 30px !important;
        z-index: 1000000 !important;
        position: fixed !important;
        top: 2px !important;
        left: 2px !important;
    }}
    
    /* 3. ФОН - ГАЛАКТИКА (Въртяща се) */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('{bg_url_main}');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        animation: rotateGalaxy 300s linear infinite;
        z-index: -1;
    }}
    @keyframes rotateGalaxy {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    /* 4. ЗАГЛАВИЕ (ЛЕНТА) */
    .top-header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 30px;
        background: rgba(0,0,0,0.85); z-index: 999;
        display: flex; justify-content: center; align-items: center;
        border-bottom: 2px solid #FFD700;
    }}
    .top-header h1 {{
        color: white; margin: 0; 
        font-size: 1.2rem; letter-spacing: 2px; 
        text-transform: uppercase; font-family: serif; font-weight: bold;
        text-shadow: 0 0 5px #FFD700;
    }}

    /* 5. МАНДАЛА (СХЕМА) */
    .mandala-wrapper {{
        width: 100%; height: 90vh; 
        display: flex; justify-content: center; align-items: center;
        margin-top: 0px !important;
        overflow: hidden;
    }}
    .mandala-box {{ position: relative; width: 1000px; height: 700px; transform-origin: center center; }}

    .ellipse-node {{
        position: absolute; 
        width: 190px; height: 55px; 
        border-radius: 50%;
        display: flex; justify-content: center; align-items: center;
        text-align: center; color: white !important; font-weight: bold; font-size: 12px;
        z-index: 200; 
        border: 2px solid rgba(255,255,255,0.9);
        text-decoration: none !important; transition: all 0.3s;
        backdrop-filter: blur(5px);
        box-shadow: 0 0 10px rgba(0,0,0,0.8);
        text-transform: uppercase;
    }}
    .ellipse-node:hover {{ transform: scale(1.1); box-shadow: 0 0 30px gold; border-color: gold; color: black !important; z-index: 300; }}

    .center-circle {{
        position: absolute; width: 150px; height: 150px; border-radius: 50%;
        background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%);
        display: flex; justify-content: center; align-items: center; text-align: center;
        color: black !important; font-weight: 900; z-index: 210; 
        border: 5px solid white; box-shadow: 0 0 50px #FFD700;
        font-size: 14px; animation: pulse 3s infinite;
        text-decoration: none !important;
    }}

    /* --- МОБИЛНА АДАПТАЦИЯ (МЕДИЯ КУЕРИ) --- */
    /* Ако екранът е по-малък от 600px (Телефони) */
    @media only screen and (max-width: 600px) {{
        /* Свиване на мандалата */
        .mandala-box {{
            transform: scale(0.38); /* Намалява до 38% */
            margin-top: -150px;     /* Обира празното място горе */
            margin-bottom: -150px;  /* Обира празното място долу */
        }}
        /* Центриране на заглавието */
        .top-header h1 {{
            margin-left: 0 !important;
            font-size: 0.9rem !important;
            text-align: center;
            width: 100%;
        }}
        /* Махане на излишни падинги */
        .block-container {{
            padding-left: 0.2rem !important;
            padding-right: 0.2rem !important;
        }}
    }}

    /* CSS ЗА ОПРАВЯНЕ НА МЕНЮТО (SIDEBAR) */
    [data-testid="stSidebarUserContent"] .stButton {{
        margin-bottom: -15px !important;
        margin-top: 0px !important;
    }}
    [data-testid="stSidebarUserContent"] h1, 
    [data-testid="stSidebarUserContent"] h3 {{
        margin-top: 0px !important;
        padding-top: 10px !important;
        margin-bottom: 0px !important;
    }}
    [data-testid="stSidebar"] .block-container {{
        padding-top: 2rem !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    if st.session_state['current_view'] == 'HOME':
        st.markdown("<br>", unsafe_allow_html=True) 
        st.info("🔐 АДМИНИСТРАТОР")
        st.text_input("Потребител")
        st.text_input("Парола", type="password")
        st.button("ВХОД")
    else:
        # Бутон за начало
        if st.button("🏠 КЪМ ГАЛАКТИКАТА"):
            st.query_params.clear()
            st.session_state.clear()
            st.rerun()
        
        st.markdown("<p style='color: #FFD700; text-align:center; font-weight:bold; margin-top:15px; margin-bottom:5px;'>БЪРЗ ДОСТЪП</p>", unsafe_allow_html=True)
        
        for m in modules:
            st.markdown(f"""
            <a href="?view={m['key']}" target="_self" style="text-decoration:none;">
                <div style="
                    background: {m['color']}; 
                    padding: 5px; 
                    margin-bottom: 4px; 
                    border-radius: 20px; 
                    color: white; 
                    text-align: center; 
                    font-weight: bold; font-size: 13px;
                    border: 1px solid white;
                    text-shadow: 1px 1px 2px black;
                    transition: 0.3s;
                " onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'">
                    {m['name']}
                </div>
            </a>
            """, unsafe_allow_html=True)

    # --- TRUST & SECURITY SECTION ---
    with st.expander("🛡️ СИГУРНОСТ И ЛИЧНИ ДАННИ"):
        st.caption("Ние не съхраняваме публично вашите данни.")
        st.markdown("<p style='text-align:center; font-size:0.8rem;'>© 2026 Езотерична Карта.</p>", unsafe_allow_html=True)

# --- ГЛАВЕН ЕКРАН ---
if st.session_state['current_view'] == 'HOME':
    st.markdown('<div class="top-header"><h1>СВЕТОВНА КАРТА НА ЕЗОТЕРИКАТА</h1></div>', unsafe_allow_html=True)
    
    # КООРДИНАТИ НА МАНДАЛАТА
    center_x, center_y = 500, 360 
    radius_x, radius_y = 350, 200

    m_html = []
    m_html.append('<div class="mandala-wrapper"><div class="mandala-box">')
    
    m_html.append('<svg width="1000" height="700" style="position: absolute; top:0; left:0; z-index:1;">')
    m_html.append('<defs><marker id="arrowhead" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0, 12 4, 0 8" fill="#FFD700" /></marker></defs>')
    
    for i in range(9):
        angle = math.radians(i * (360/9) - 90)
        x1 = center_x + (radius_x - 30) * math.cos(angle)
        y1 = center_y + (radius_y - 15) * math.sin(angle)
        x2 = center_x + 85 * math.cos(angle)
        y2 = center_y + 85 * math.sin(angle)
        m_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="2" marker-end="url(#arrowhead)" opacity="1.0" />')
    
    m_html.append('</svg>')

    center_mod = modules[9]
    m_html.append(f'<a href="?view={center_mod["key"]}" target="_self" class="center-circle" style="left: 425px; top: 285px;">{center_mod["name"]}</a>')

    for i in range(9):
        mod = modules[i]
        angle = math.radians(i * (360/9) - 90)
        x = (center_x + radius_x * math.cos(angle)) - 95 
        y = (center_y + radius_y * math.sin(angle)) - 27.5
        m_html.append(f'<a href="?view={mod["key"]}" target="_self" class="ellipse-node" style="background-color: {mod["color"]}; left: {x}px; top: {y}px;">{mod["name"]}</a>')

    m_html.append('</div></div>')
    
    st.markdown("".join(m_html), unsafe_allow_html=True)

else:
    # --- ВЪТРЕШНА СТРАНИЦА ---
    key = st.session_state['current_view']
    if key not in modules_dict: key = "Western"
    data = modules_dict[key]

    if st.session_state['show_form']:
        # ФОРМА ЗА ДАННИ
        st.markdown(f"""<div style="text-align: center; margin-bottom: 20px;"><h1 style="color:{data['color']}; text-shadow: 0 0 25px {data['color']}; font-size: 2.5rem; margin:0;">{data['name']} (Данни)</h1></div>""", unsafe_allow_html=True)
        
        with st.container(border=True):
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Име на клиента")
                st.date_input("Дата на раждане")
            with c2:
                st.time_input("Час на раждане")
                st.text_input("Място на раждане")
            
            st.write("")
            if st.button("🚀 ИЗЧИСЛИ СЕГА"):
                st.success("Изчисляване...")

    else:
        # ЗАГЛАВИЕ НА МОДУЛА
        if key != "Western":
            st.markdown(f"""<div style="text-align: center; margin-bottom: 5px;"><h1 style="color:{data['color']}; text-shadow: 0 0 25px {data['color']}; font-size: 2.2rem; text-transform: uppercase; margin:0;">{data['name']}</h1></div>""", unsafe_allow_html=True)

        if key == "Western":
            # --- ЗАПАДНА АСТРОЛОГИЯ (MAIN) ---
            if st.session_state.get('start_horoscope', False):
                # МЕНЮ С БУТОНИ - НОВ ДИЗАЙН
                st.markdown("""
                <style>
                    .stApp { background-image: none !important; background-color: #000000 !important; }
                </style>
                """, unsafe_allow_html=True)
                
                # Показване на менюто
                if st.session_state['astro_section'] == 'menu':
                    st.markdown("<h2 style='text-align: center; color: white;'>Какво искаш да разбереш днес?</h2>", unsafe_allow_html=True)
                    st.write("")
                    c1, c2, c3, c4 = st.columns(4, gap="medium")
                    
                    # 4-ТЕ НОВИ БУТОНА (HOOK TITLES)
                    with c1:
                        if st.button("👤\nМОЯТА\nСЪДБА", use_container_width=True): 
                            st.session_state['astro_section'] = "natal"
                            st.rerun()
                    with c2:
                        if st.button("❤️\nЛЮБОВЕН\nКОМПАС", use_container_width=True): 
                            st.session_state['astro_section'] = "synastry"
                            st.rerun()
                    with c3:
                        if st.button("✨\nКАРТА НА\nБЪДЕЩЕТО", use_container_width=True): 
                            st.session_state['astro_section'] = "forecast"
                            st.rerun()
                    with c4:
                        if st.button("💰\nУСПЕХ И\nПАРИ", use_container_width=True): 
                            st.session_state['astro_section'] = "election"
                            st.rerun()
                            
                # ФОРМИ ЗА ПОПЪЛВАНЕ (Със старите връзки, но новите имена)
                elif st.session_state['astro_section'] == "natal":
                    st.title("👤 МОЯТА СЪДБА (Личен анализ)")
                    st.markdown('<div class="intro-box">"Това е твоят космически паспорт. Тук ще разбереш коя е твоята истинска сила и кармична задача."</div>', unsafe_allow_html=True)
                    if not st.session_state.get('main_user'):
                        st.warning("👇 Въведи данните си:")
                    user_data = render_main_user_smart_form("natal")
                    if user_data:
                        st.button("🚀 РАЗКРИЙ СЪДБАТА МИ", type="primary", use_container_width=True)
                    if st.button("← Назад"):
                        st.session_state['astro_section'] = 'menu'
                        st.rerun()

                elif st.session_state['astro_section'] == "synastry":
                    st.title("❤️ ЛЮБОВЕН КОМПАС")
                    st.markdown('<div class="intro-box">"Сродни души ли сте? Провери съвместимостта и разбери има ли бъдеще връзката."</div>', unsafe_allow_html=True)
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.subheader("👤 ТИ")
                        render_main_user_smart_form("synastry")
                    with col_b:
                        st.subheader("❤️ ТЕ (Партньор)")
                        render_person_form("partner_b", show_header=False)
                    st.write("\n")
                    st.button("🔥 ПРОВЕРИ ЛЮБОВТА", type="primary", use_container_width=True)
                    if st.button("← Назад"):
                        st.session_state['astro_section'] = 'menu'
                        st.rerun()

                elif st.session_state['astro_section'] == "forecast":
                    st.title("✨ КАРТА НА БЪДЕЩЕТО")
                    st.markdown('<div class="intro-box">"Какво те очаква? Дневен, месечен или годишен хороскоп според личните ти транзити."</div>', unsafe_allow_html=True)
                    type_forecast = st.radio("Избери:", ["👤 Лична прогноза (Днес/Утре)", "🎂 Годишен Солар (РД)"], horizontal=True)
                    render_main_user_smart_form("forecast_single")
                    st.button("🔮 ВИЖ БЪДЕЩЕТО", type="primary", use_container_width=True)
                    if st.button("← Назад"):
                        st.session_state['astro_section'] = 'menu'
                        st.rerun()

                elif st.session_state['astro_section'] == "election":
                    st.title("💰 УСПЕХ И ПАРИ (Избор на момент)")
                    st.markdown('<div class="intro-box">"Кога да стартираш бизнес или проект? Намери златния момент за успех."</div>', unsafe_allow_html=True)
                    render_main_user_smart_form("election")
                    st.selectbox("Цел:", ["💼 Бизнес старт", "💰 Инвестиция", "✍️ Подписване на договор"])
                    st.button("⏳ НАМЕРИ ДАТАТА", type="primary", use_container_width=True)
                    if st.button("← Назад"):
                        st.session_state['astro_section'] = 'menu'
                        st.rerun()

            else:
                # НАЧАЛЕН ЕКРАН НА ЗАПАДНА (Снимка + Бутон)
                st.markdown("""
                <style>
                    .stApp { background-image: none !important; background-color: #000000 !important; }
                    .block-container { padding: 0 !important; max-width: 100% !important; }
                    [data-testid="stImage"] > img { height: 85vh !important; width: 100% !important; object-fit: cover !important; }
                    div.stButton > button { position: relative !important; z-index: 99999 !important; top: -80px !important; padding: 12px !important; }
                </style>
                """, unsafe_allow_html=True)
                
                try:
                    st.image("galaxy.png", use_container_width=True)
                except:
                    st.error("Липсва galaxy.png")
                
                c1, c2, c3 = st.columns([1, 2, 1])
                with c2:
                    st.markdown(f"""<style>div.stButton > button {{ background: {data['color']}; color: black !important; font-size: 18px; border-radius: 15px; border: 2px solid white; }}</style>""", unsafe_allow_html=True)
                    if st.button("✨ ЗАПОЧНИ СВОЯ ХОРОСКОП ✨", use_container_width=True):
                        st.session_state['start_horoscope'] = True
                        st.session_state['astro_section'] = 'menu'
                        st.rerun()
        else:
             # Други модули (в строеж)
            st.markdown(f"""<div class="content-box" style="border-color: {data['color']};">{data['name']} е в процес на разработка...</div>""", unsafe_allow_html=True)
            if st.button("✨ ЗАПОЧНИ ✨"):
                toggle_form()
                st.rerun()