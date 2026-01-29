import streamlit as st
import math
import datetime
import base64

# === ИНИЦИАЛИЗАЦИЯ ===
if 'current_view' not in st.session_state: st.session_state['current_view'] = 'HOME'
if 'start_horoscope' not in st.session_state: st.session_state['start_horoscope'] = False
if 'western_cat' not in st.session_state: st.session_state['western_cat'] = None
if 'astro_section' not in st.session_state: st.session_state['astro_section'] = 'menu'
if 'main_user' not in st.session_state: st.session_state['main_user'] = None

params = st.query_params
if "view" in params: st.session_state['current_view'] = params["view"]

# === КОНФИГУРАЦИЯ ===
initial_state = "expanded" if st.session_state['current_view'] == 'HOME' else "collapsed"
st.set_page_config(page_title="Езотерична Карта", layout="wide", initial_sidebar_state=initial_state)

# === ДАННИ ===
DAYS = [str(i) for i in range(1, 32)]
MONTHS = ["Януари", "Февруари", "Март", "Април", "Май", "Юни", "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"]
YEARS_BIRTH = [str(i) for i in range(1930, 2026)]
HOURS = [f"{i:02d}" for i in range(0, 24)]
MINUTES = [f"{i:02d}" for i in range(0, 60)]

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

western_menu_data = {
    "destiny": {
        "title": "👤 МОЯТА СЪДБА", "desc": "Личен анализ", "color": "#4682B4",
        "options": ["🔸 Пълна Рождена Карта", "🔸 Скрити Таланти и Потенциал", "🔸 Кармичен Път и Мисия"]
    },
    "love": {
        "title": "❤️ ЛЮБОВЕН КОМПАС", "desc": "Съвместимост", "color": "#FF1493",
        "options": ["🔹 Сродни души ли сме?", "🔹 Сексуална енергия", "🔹 Бъдеще на връзката"]
    },
    "future": {
        "title": "✨ КАРТА НА БЪДЕЩЕТО", "desc": "Прогнози", "color": "#9370DB",
        "options": ["🔹 Хороскоп за ДНЕС", "🔹 Месечен преглед", "🔹 Годишен солар"]
    },
    "money": {
        "title": "💰 УСПЕХ И ПАРИ", "desc": "Кариера", "color": "#FFD700",
        "options": ["🔸 Финансов Код и Богатство", "🔸 Избор на Златни Дни", "🔸 Професионално Призвание"]
    }
}

# === CSS ДИЗАЙН ===
bg_url = "https://hicomm.bg/uploads/articles/202202/69095/mainimage-eto-kolko-sa-zvezdite-v-nashata-galaktika-i-v-cyalata-vselena.jpg?1643808921546"

st.markdown(f"""
<style>
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    footer, header {{ display: none !important; }}
    div[data-testid="column"] {{ gap: 0.1rem !important; }}
    h1, h2, h3, h4, h5, p {{ margin-bottom: 0.1rem !important; margin-top: 0.1rem !important; }}
    .stApp {{ background-image: url('{bg_url}'); background-size: cover; background-position: center; background-attachment: fixed; }}
    
    /* СНИМКА (МОМИЧЕТО) */
    .hero-container {{
        position: relative;
        width: 100%;
        height: auto;
        min-height: 85vh; 
        display: block;
    }}
    .hero-container img {{
        width: 100%;
        height: auto;
        display: block;
    }}
    
    /* БУТОН НАЗАД (ГОРЕ ВЛЯВО) */
    .hero-back-btn {{
        position: absolute; top: 20px; left: 20px; z-index: 999;
        text-decoration: none !important;
        background: rgba(0,0,0,0.6); 
        border: 1px solid rgba(255,255,255,0.5); color: #fff !important; 
        padding: 8px 20px; border-radius: 8px; font-weight: bold; font-size: 14px;
        backdrop-filter: blur(5px);
    }}

    section[data-testid="stSidebar"] {{ display: {initial_state if st.session_state['current_view'] == 'HOME' else 'none'} !important; }}
    .desktop-view {{ display: block !important; width: 100%; }}
    .mobile-view {{ display: none !important; }}
    
    @media only screen and (max-width: 900px) {{
        .desktop-view {{ display: none !important; }}
        .mobile-view {{ display: block !important; width: 100%; height: 100vh; overflow: hidden; position: relative; }}
        section[data-testid="stSidebar"] {{ display: none !important; }}
    }}
    
    /* МАНДАЛА */
    .mandala-wrapper {{ width: 100%; height: 90vh; display: flex; justify-content: center; align-items: center; padding-top: 20px; }}
    .mandala-box {{ position: relative; width: 1000px; height: 700px; }}
    .ellipse-node {{
        position: absolute; width: 190px; height: 55px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
        color: white !important; font-weight: bold; font-size: 12px; z-index: 200; border: 2px solid rgba(255,255,255,0.9); backdrop-filter: blur(5px);
    }}
    .center-circle {{
        position: absolute; width: 150px; height: 150px; border-radius: 50%; background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%);
        display: flex; justify-content: center; align-items: center; color: black !important; font-weight: 900; z-index: 210; border: 5px solid white; font-size: 14px; animation: pulse 3s infinite; text-decoration: none !important;
    }}
    .mob-container {{ position: relative; width: 360px; height: 500px; margin: 20px auto 0 auto; }}
    .mob-sun {{
        position: absolute; width: 100px; height: 100px; border-radius: 50%; background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%); left: 130px; top: 180px; 
        display: flex; justify-content: center; align-items: center; border: 4px solid white; box-shadow: 0 0 20px #FFD700; z-index: 10; color: black !important; font-weight: bold; font-size: 11px; text-align: center;
    }}
    .mob-planet {{
        position: absolute; width: 70px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center;
        color: white !important; font-weight: bold; font-size: 10px; z-index: 20; border: 2px solid rgba(255,255,255,0.8); backdrop-filter: blur(4px);
    }}
    
    /* ФОРМИ И БУТОНИ */
    div[data-testid="stSelectbox"] > label, div[data-testid="stTextInput"] > label, div[data-testid="stRadio"] > label {{
        color: #FFD700 !important; font-weight: bold; font-size: 10px !important; margin-bottom: -2px !important; height: auto !important; min-height: 0px !important;
    }}
    div[data-testid="stTextInput"] div[data-baseweb="input"] {{ min-height: 24px !important; height: 24px !important; padding: 0px !important; }}
    input {{ padding: 0px 5px !important; min-height: 24px !important; height: 24px !important; font-size: 12px !important; }}
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {{ min-height: 24px !important; height: 24px !important; }}
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {{ padding: 0px 2px !important; font-size: 12px !important; line-height: 24px !important; }}
    div[data-testid="stRadio"] div[role="radiogroup"] {{ background: rgba(255,255,255,0.1); padding: 0px 2px; border-radius: 5px; color: white; display: flex; align-items: center; height: 24px; }}
    div[data-testid="stRadio"] label {{ padding-right: 5px !important; font-size: 11px !important; }}
    div[data-testid="stRadio"] p {{ font-size: 11px !important; }}
    div[data-testid="element-container"] {{ margin-bottom: 2px !important; }}
    
    button[kind="secondary"] {{
        background-color: transparent !important; border: 1px solid rgba(255,255,255,0.3) !important; color: #ccc !important;
        padding: 2px 8px !important; height: auto !important; min-height: 0px !important; font-size: 12px !important;
    }}
    button[kind="secondary"]:hover {{ border-color: white !important; color: white !important; }}
    
    button[kind="primary"] {{
        background-color: #FF4500 !important; color: white !important; font-size: 18px !important; font-weight: bold !important;
        padding: 4px 12px !important; border-radius: 8px !important; border: none !important; width: 100%; margin-top: 5px !important;
        min-height: 0px !important; height: auto !important;
        box-shadow: 0 0 10px #FF4500;
    }}
    button[kind="primary"]:hover {{ background-color: #FF0000 !important; box-shadow: 0 0 20px #FF4500; }}
    
    @keyframes pulse {{ 0%, 100% {{ transform: scale(1); box-shadow: 0 0 30px #FFD700; }} 50% {{ transform: scale(1.05); box-shadow: 0 0 80px #FFD700; }} }}
</style>
""", unsafe_allow_html=True)
# === СТРАНИЧНА ЛЕНТА ===
if st.session_state['current_view'] == 'HOME':
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True) 
        st.info("🔐 АДМИНИСТРАТОР")
        st.text_input("Потребител"); st.text_input("Парола", type="password"); st.button("ВХОД")

# === УНИВЕРСАЛНА ФОРМА ===
def render_main_user_smart_form(key_context, is_compatibility=False):
    if is_compatibility:
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown("<h5 style='color:#9370DB; text-align: center; margin:0 0 2px 0; font-size: 24px !important; font-weight: bold;'>👤 ТИ</h5>", unsafe_allow_html=True)
            c_name, c_sex = st.columns([1.8, 1.2])
            with c_name: st.text_input("Име:", key=f"name_p1_{key_context}")
            with c_sex: st.radio("Пол:", ["ЖЕНА", "МЪЖ"], key=f"sex_p1_{key_context}") 
            st.markdown("<div style='margin-top: 2px; font-weight:bold; color:#FFD700; font-size: 11px;'>Дата на раждане:</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.selectbox("Ден", DAYS, key=f"d_p1_{key_context}")
            with c2: st.selectbox("Месец", MONTHS, key=f"m_p1_{key_context}")
            with c3: st.selectbox("Година", YEARS_BIRTH, index=60, key=f"y_p1_{key_context}")
            c4, c5 = st.columns(2)
            with c4: st.selectbox("Час:", HOURS, key=f"h_p1_{key_context}")
            with c5: st.text_input("Град:", key=f"city_p1_{key_context}")
        with c_right:
            st.markdown("<h5 style='color:#FF69B4; text-align: center; margin:0 0 2px 0; font-size: 24px !important; font-weight: bold;'>💗 ПАРТНЬОР</h5>", unsafe_allow_html=True)
            c_name, c_sex = st.columns([1.8, 1.2])
            with c_name: st.text_input("Име:", key=f"name_p2_{key_context}")
            with c_sex: st.radio("Пол:", ["ЖЕНА", "МЪЖ"], key=f"sex_p2_{key_context}")
            st.markdown("<div style='margin-top: 2px; font-weight:bold; color:#FFD700; font-size: 11px;'>Дата на раждане:</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: st.selectbox("Ден", DAYS, key=f"d_p2_{key_context}")
            with c2: st.selectbox("Месец", MONTHS, key=f"m_p2_{key_context}")
            with c3: st.selectbox("Година", YEARS_BIRTH, index=60, key=f"y_p2_{key_context}")
            c4, c5 = st.columns(2)
            with c4: st.selectbox("Час:", HOURS, key=f"h_p2_{key_context}")
            with c5: st.text_input("Град:", key=f"city_p2_{key_context}")
    else:
        st.markdown("<h5 style='color:#9370DB; text-align: center; margin:0 0 2px 0; font-size: 20px !important; font-weight: bold;'>👤 ЛИЧНИ ДАННИ</h5>", unsafe_allow_html=True)
        c_spacer_l, c_main, c_spacer_r = st.columns([1, 4, 1]) 
        with c_main:
            c_name, c_sex = st.columns([2, 1])
            with c_name: name = st.text_input("Име", key=f"name_{key_context}")
            with c_sex: sex = st.radio("Пол", ["ЖЕНА", "МЪЖ"], key=f"sex_{key_context}")
            st.markdown("<div style='margin-top: 2px; font-weight:bold; color:#FFD700; font-size: 11px;'>Дата на раждане:</div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: d = st.selectbox("Ден", DAYS, key=f"d_{key_context}")
            with c2: m = st.selectbox("Месец", MONTHS, key=f"m_{key_context}")
            with c3: y = st.selectbox("Година", YEARS_BIRTH, index=60, key=f"y_{key_context}")
            c4, c5 = st.columns(2)
            with c4: hour = st.selectbox("Час", HOURS, key=f"h_{key_context}")
            with c5: minute = st.selectbox("Мин", MINUTES, key=f"min_{key_context}")
            city = st.text_input("Град", key=f"city_{key_context}")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True) 
    c_b1, c_b2, c_b3 = st.columns([1, 2, 1])
    with c_b2: st.button("🔥 ИЗЧИСЛИ СЕГА", key=f"submit_{key_context}", type="primary", use_container_width=True)

# === ГЛАВНА СТРАНИЦА (БАЛАНСИРАНА МАНДАЛА) ===
if st.session_state['current_view'] == 'HOME':
    desktop_html = ['<div class="desktop-view">']
    desktop_html.append('<div style="text-align:center; margin-top:10px;"><h1 style="color:white; text-shadow:0 0 10px gold;">СВЕТОВНА КАРТА НА ЕЗОТЕРИКАТА</h1></div>')
    desktop_html.append('<div class="mandala-wrapper"><div class="mandala-box">')
    desktop_html.append('<svg width="1000" height="700" style="position: absolute; top:0; left:0; z-index:1;"><defs><marker id="arrowhead" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0, 12 4, 0 8" fill="#FFD700" /></marker></defs>')
    
    # ТУК Е ФИНАЛНАТА НАСТРОЙКА: c_y = 310 (По средата между 290 и 330)
    c_x, c_y, r_x, r_y = 500, 310, 350, 200
    
    for i in range(9):
        angle = math.radians(i * (360/9) - 90)
        x1 = c_x + (r_x - 30) * math.cos(angle); y1 = c_y + (r_y - 15) * math.sin(angle)
        x2 = c_x + 85 * math.cos(angle); y2 = c_y + 85 * math.sin(angle)
        desktop_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="2" marker-end="url(#arrowhead)" />')
    desktop_html.append('</svg>')
    
    center = modules[9]
    # ТУК СЪЩО ЦЕНТРИРАМЕ: top = 235 (Съобразено с 310)
    desktop_html.append(f'<a href="?view={center["key"]}" target="_self" class="center-circle" style="left: 425px; top: 235px;">{center["name"]}</a>')
    
    for i in range(9):
        m = modules[i]
        angle = math.radians(i * (360/9) - 90)
        x = (c_x + r_x * math.cos(angle)) - 95; y = (c_y + r_y * math.sin(angle)) - 27.5
        desktop_html.append(f'<a href="?view={m["key"]}" target="_self" class="ellipse-node" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["name"]}</a>')
    desktop_html.append('</div></div></div>')
    st.markdown("".join(desktop_html), unsafe_allow_html=True)

    mobile_html = ['<div class="mobile-view">']
    mobile_html.append('<div class="mob-container">')
    mob_cx, mob_cy = 155, 175; mob_radius_x = 115; mob_radius_y = 160 
    manual_angles = [-90, -45, -10, 30, 65, 115, 150, 190, 225]
    mobile_html.append('<svg width="360" height="500" style="position: absolute; top:0; left:0; z-index:1;">')
    for i in range(9):
        angle = math.radians(manual_angles[i])
        sx = mob_cx + 25; sy = mob_cy + 55
        x1 = sx + (mob_radius_x - 30) * math.cos(angle); y1 = sy + (mob_radius_y - 20) * math.sin(angle)
        x2 = sx + 25 * math.cos(angle); y2 = sy + 25 * math.sin(angle)
        mobile_html.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="1" opacity="0.6" />')
    mobile_html.append('</svg>')
    mobile_html.append(f'<div class="mob-sun">ВЪРХОВНАТА<br>ИСТИНА</div>')
    for i in range(9):
        m = modules[i]
        angle = math.radians(manual_angles[i])
        x = mob_cx + mob_radius_x * math.cos(angle) - 10; y = mob_cy + 35 + mob_radius_y * math.sin(angle)
        mobile_html.append(f'<div class="mob-planet" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["short"]}</div>')
    mobile_html.append('</div></div>') 
    st.markdown("".join(mobile_html), unsafe_allow_html=True)

# === ВЪТРЕШНИ СТРАНИЦИ ===
else:
    key = st.session_state['current_view']
    mod = modules_dict.get(key, modules[0])

    if key == "Western":
        if not st.session_state['start_horoscope']:
            st.markdown("""<style>.stApp { background-color: #000000 !important; } .block-container { padding: 0 !important; max-width: 100% !important; }</style>""", unsafe_allow_html=True)
            
            st.markdown('<a href="?view=HOME" target="_self" class="hero-back-btn">⬅️ НАЗАД</a>', unsafe_allow_html=True)
            
            try:
                with open("galaxy.png", "rb") as f:
                    data = f.read()
                    encoded = base64.b64encode(data).decode()
                img_src = f"data:image/png;base64,{encoded}"
            except:
                img_src = "https://raw.githubusercontent.com/zahari89/astro-images/main/galaxy.png"

            st.markdown(f'<div class="hero-container"><img src="{img_src}" alt="Galaxy Girl"></div>', unsafe_allow_html=True)

            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                # ЧЕРНИЯТ БУТОН ЗА СТАРТ
                st.markdown("""
                <style>
                div.stButton > button {
                    background-color: black !important;
                    border: 2px solid #FFD700 !important;
                    color: #FFD700 !important;
                    opacity: 1 !important;
                    font-weight: 900 !important;
                    box-shadow: 0 0 15px rgba(255,215,0,0.5) !important;
                    margin-top: -30px !important;
                    margin-bottom: 50px !important;
                }
                div.stButton > button:hover {
                    box-shadow: 0 0 25px #FFD700 !important;
                    background-color: #111 !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                if st.button("✨ ЗАПОЧНИ СВОЯ ХОРОСКОП ✨", use_container_width=True):
                    st.session_state['start_horoscope'] = True
                    st.rerun()
        else:
            st.markdown("""<style>.stApp { background-image: none !important; background-color: #000000 !important; } .block-container { max-width: 100% !important; padding: 2rem 1rem !important; }</style>""", unsafe_allow_html=True)
            if st.session_state['western_cat'] is None:
                if st.button("⬅️ НАЗАД", type="secondary"): st.session_state['start_horoscope'] = False; st.rerun()
                st.markdown("<h1 style='text-align: center; color: #FFD700; font-size: 40px; font-weight: bold; text-shadow: 0 0 20px #FFD700; margin-bottom: 0px;'>✨ ИЗБЕРИ СВОЯ ПЪТ ✨</h1>", unsafe_allow_html=True)
                
                st.markdown("<div style='height: 150px;'></div>", unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns(4)
                
                def cat_btn(title, desc, color, key_name):
                    st.markdown(f"""
                    <div style='text-align: center; margin-bottom: 20px;'>
                        <div style='color: {color}; font-size: 22px; font-weight: 900; text-transform: uppercase; text-shadow: 0 0 15px {color}; margin-bottom: 10px; line-height: 1.1;'>{title}</div>
                        <div style='color: #E0E0E0; font-size: 16px; font-weight: 500; font-style: italic; min-height: 40px;'>{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("👉 ОТВОРИ", key=f"btn_{key_name}", use_container_width=True): st.session_state['western_cat'] = key_name; st.rerun()
                
                with col1: cat_btn(western_menu_data['destiny']['title'], western_menu_data['destiny']['desc'], western_menu_data['destiny']['color'], 'destiny')
                with col2: cat_btn(western_menu_data['love']['title'], western_menu_data['love']['desc'], western_menu_data['love']['color'], 'love')
                with col3: cat_btn(western_menu_data['future']['title'], western_menu_data['future']['desc'], western_menu_data['future']['color'], 'future')
                with col4: cat_btn(western_menu_data['money']['title'], western_menu_data['money']['desc'], western_menu_data['money']['color'], 'money')
            else:
                cat_key = st.session_state['western_cat']
                cat_data = western_menu_data.get(cat_key, western_menu_data['destiny'])
                c_back, c_title, c_empty = st.columns([1, 4, 1])
                with c_back:
                    if st.button("⬅️ НАЗАД", type="secondary"): st.session_state['western_cat'] = None; st.rerun()
                with c_title:
                    st.markdown(f"<h2 style='margin:0; padding-top: 5px; color: {cat_data['color']}; text-align: center;'>{cat_data['title']}</h2>", unsafe_allow_html=True)
                
                if cat_key == 'love': st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

                opts_col1, opts_col2, opts_col3 = st.columns(3)
                for idx, opt in enumerate(cat_data['options']):
                    curr_col = [opts_col1, opts_col2, opts_col3][idx % 3]
                    with curr_col:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 5px; border-radius: 8px; margin-bottom: 5px; border-left: 5px solid {cat_data['color']}; text-align: center;">
                            <h4 style="color: #00FFFF; margin: 0; font-size: 18px; font-weight: bold; line-height: 1.2;">{opt}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                render_main_user_smart_form(f"cat_{cat_key}", is_compatibility=(cat_key == "love"))
    else:
        st.markdown(f"""<div style="text-align: center; margin-top:50px;"><h1 style="color:{mod['color']};">{mod['name']}</h1></div>""", unsafe_allow_html=True)
        st.markdown("""<a href="?view=HOME" target="_self" style="display: block; width: 100px; margin: 20px auto; text-align: center; background: #333; color: white; padding: 10px; border-radius: 5px; text-decoration: none;">🏠 НАЧАЛО</a>""", unsafe_allow_html=True)