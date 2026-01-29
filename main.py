import streamlit as st
import math
import base64

# ==============================================================================
# 1. НАСТРОЙКА
# ==============================================================================
st.set_page_config(page_title="Езотерична Карта", layout="wide", initial_sidebar_state="collapsed")

# ==============================================================================
# 2. АВТОМАТИЧЕН РАЗПРЕДЕЛИТЕЛ (JS)
# ==============================================================================
if "device" not in st.query_params:
    st.markdown(
        """
        <script>
            var width = window.innerWidth;
            if (width <= 900) {
                var url = new URL(window.location.href);
                url.searchParams.set('device', 'mobile');
                window.location.href = url.toString();
            } else {
                var url = new URL(window.location.href);
                url.searchParams.set('device', 'desktop');
                window.history.replaceState(null, null, url.toString());
            }
        </script>
        """,
        unsafe_allow_html=True
    )

device_type = st.query_params.get("device", "desktop")

# ==============================================================================
# 3. ДАННИ И ПРОМЕНЛИВИ
# ==============================================================================
url_view = st.query_params.get("view")
if 'current_view' not in st.session_state: st.session_state['current_view'] = 'HOME'
if url_view and url_view != st.session_state['current_view']: st.session_state['current_view'] = url_view

if 'start_horoscope' not in st.session_state: st.session_state['start_horoscope'] = False
if 'western_cat' not in st.session_state: st.session_state['western_cat'] = None

# Списъци
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
    "destiny": {"title": "👤 МОЯТА СЪДБА", "desc": "Личен анализ", "color": "#4682B4", "options": ["🔸 Пълна Рождена Карта", "🔸 Скрити Таланти", "🔸 Кармичен Път"]},
    "love": {"title": "❤️ ЛЮБОВЕН КОМПАС", "desc": "Съвместимост", "color": "#FF1493", "options": ["🔹 Сродни души ли сме?", "🔹 Сексуална енергия", "🔹 Бъдеще на връзката"]},
    "future": {"title": "✨ КАРТА НА БЪДЕЩЕТО", "desc": "Прогнози", "color": "#9370DB", "options": ["🔹 Хороскоп за ДНЕС", "🔹 Месечен преглед", "🔹 Годишен солар"]},
    "money": {"title": "💰 УСПЕХ И ПАРИ", "desc": "Кариера", "color": "#FFD700", "options": ["🔸 Финансов Код", "🔸 Златни Дни", "🔸 Професионално Призвание"]}
}

bg_url = "https://hicomm.bg/uploads/articles/202202/69095/mainimage-eto-kolko-sa-zvezdite-v-nashata-galaktika-i-v-cyalata-vselena.jpg?1643808921546"

# ==============================================================================
# 4. УМНАТА ФОРМА
# ==============================================================================
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

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) 
    c_b1, c_b2, c_b3 = st.columns([1, 2, 1])
    with c_b2: st.button("🔥 ИЗЧИСЛИ СЕГА", key=f"submit_{key_context}", type="primary", use_container_width=True)
    st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# 5. ФУНКЦИЯ ЗА КОМПЮТЪР (DESKTOP)
# ==============================================================================
def run_desktop():
    # CSS ЗА PC
    st.markdown(f"""
    <style>
        .block-container {{ padding: 0 !important; max-width: 100% !important; }}
        header {{ visibility: visible !important; }}
        
        /* ЛЯВА ЛЕНТА (АДМИН) - СТИЛИЗАЦИЯ (САМО ЗА PC) */
        [data-testid="stSidebar"] {{
            background-color: #0e0e0e !important;
            border-right: 1px solid #FFD700;
        }}
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div {{
            color: #FFD700 !important;
        }}
        
        /* СТРЕЛКА ЗА ОТВАРЯНЕ НА АДМИН ПАНЕЛА (ГОРЕ ВЛЯВО) */
        [data-testid="stSidebarCollapsedControl"] {{ 
            color: #FFD700 !important; 
            background-color: rgba(0,0,0,0.8) !important; 
            border: 1px solid #FFD700;
            border-radius: 50%; 
            display: block !important;
            z-index: 9999 !important;
            width: 40px !important;
            height: 40px !important;
            top: 10px;
            left: 10px;
        }}
        [data-testid="stSidebarCollapsedControl"] svg {{
            width: 25px !important;
            height: 25px !important;
        }}

        .stApp {{ background-image: url('{bg_url}'); background-size: cover; background-position: center; background-attachment: fixed; }}
        
        /* МАНДАЛА ЦЕНТРИРАНЕ */
        .mandala-wrapper {{ width: 100%; height: 90vh; display: flex; justify-content: center; align-items: center; padding-top: 50px; }}
        .mandala-box {{ position: relative; width: 1000px; height: 700px; }}
        
        .ellipse-node {{ position: absolute; width: 190px; height: 55px; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white !important; font-weight: bold; font-size: 12px; z-index: 200; border: 2px solid rgba(255,255,255,0.9); backdrop-filter: blur(5px); text-decoration: none !important; }}
        .center-circle {{ position: absolute; width: 150px; height: 150px; border-radius: 50%; background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%); display: flex; justify-content: center; align-items: center; color: black !important; font-weight: 900; z-index: 210; border: 5px solid white; font-size: 14px; animation: pulse 3s infinite; text-decoration: none !important; }}
        
        div[data-testid="stSelectbox"] > label, div[data-testid="stTextInput"] > label, div[data-testid="stRadio"] > label {{ color: #FFD700 !important; font-weight: bold; font-size: 10px !important; margin-bottom: -2px !important; }}
        button[kind="primary"] {{ background-color: #FF4500 !important; color: white !important; font-size: 18px !important; font-weight: bold !important; padding: 4px 12px !important; border-radius: 8px !important; border: none !important; width: 100%; margin-top: 5px !important; box-shadow: 0 0 10px #FF4500; }}
        
        div.stButton > button[kind="secondary"] {{
            background: rgba(0,0,0,0.6) !important;
            border: 2px solid #FFD700 !important;
            color: #FFD700 !important;
            border-radius: 20px !important;
            padding: 5px 20px !important;
            font-weight: bold !important;
            transition: 0.3s;
        }}
        div.stButton > button[kind="secondary"]:hover {{
            background: #FFD700 !important;
            color: black !important;
            box-shadow: 0 0 15px #FFD700;
        }}

        .hero-back-btn {{ 
            position: absolute; top: 60px; left: 30px; z-index: 999; 
            text-decoration: none !important; 
            background: rgba(0,0,0,0.7); 
            border: 2px solid #FFD700; 
            color: #FFD700; 
            padding: 10px 25px; 
            border-radius: 30px; 
            font-weight: bold; 
            font-size: 16px;
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
            transition: all 0.3s ease;
        }}
        .hero-back-btn:hover {{ background: #FFD700; color: black; box-shadow: 0 0 20px #FFD700; }}
        
        @keyframes pulse {{ 0%, 100% {{ transform: scale(1); box-shadow: 0 0 30px #FFD700; }} 50% {{ transform: scale(1.05); box-shadow: 0 0 80px #FFD700; }} }}
    </style>
    """, unsafe_allow_html=True)

    # ------------------ ЛЯВА ЛЕНТА (САМО ТУК) ------------------
    with st.sidebar:
        st.markdown("<div style='text-align: center; margin-top: 20px;'><h2 style='color: #FFD700;'>🔐 ADMIN PANEL</h2></div>", unsafe_allow_html=True)
        st.markdown("---")
        with st.form("admin_login"):
            st.text_input("Потребител", key="admin_user")
            st.text_input("Парола", type="password", key="admin_pass")
            st.form_submit_button("ВЛЕЗ В СИСТЕМАТА")
        st.markdown("<br><br><div style='text-align: center; color: gray; font-size: 10px;'>Esoteric Map v3.0</div>", unsafe_allow_html=True)

    if st.session_state['current_view'] == 'HOME':
        # ГОЛЯМА МАНДАЛА
        h = ['<div class="mandala-wrapper"><div class="mandala-box">']
        h.append('<div style="text-align:center; margin-top:10px;"><h1 style="color:white; text-shadow:0 0 10px gold;">СВЕТОВНА КАРТА НА ЕЗОТЕРИКАТА</h1></div>')
        h.append('<svg width="1000" height="700" style="position: absolute; top:0; left:0; z-index:1;"><defs><marker id="arr" markerWidth="12" markerHeight="8" refX="10" refY="4" orient="auto"><polygon points="0 0, 12 4, 0 8" fill="#FFD700" /></marker></defs>')
        
        c_x, c_y = 500, 360 
        r_x, r_y = 350, 200

        for i in range(9):
            ang = math.radians(i * (360/9) - 90)
            x1=c_x+(r_x-30)*math.cos(ang); y1=c_y+(r_y-15)*math.sin(ang)
            x2=c_x+85*math.cos(ang); y2=c_y+85*math.sin(ang)
            h.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="2" marker-end="url(#arr)" />')
        h.append('</svg>')
        h.append(f'<a href="?view=Center&device=desktop" target="_self" class="center-circle" style="left: 425px; top: {c_y - 75}px;">ВЪРХОВНАТА<br>ИСТИНА</a>')
        for i in range(9):
            m = modules[i]; ang = math.radians(i * (360/9) - 90)
            x=(c_x+r_x*math.cos(ang))-95; y=(c_y+r_y*math.sin(ang))-27.5
            h.append(f'<a href="?view={m["key"]}&device=desktop" target="_self" class="ellipse-node" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["name"]}</a>')
        h.append('</div></div>')
        st.markdown("".join(h), unsafe_allow_html=True)

    elif st.session_state['current_view'] == 'Western':
        # СТРАНИЦА ЗАПАД - DESKTOP
        if not st.session_state['start_horoscope']:
            st.markdown("""<style>.stApp { background-color: #000000 !important; }</style>""", unsafe_allow_html=True)
            st.markdown('<a href="?view=HOME&device=desktop" target="_self" class="hero-back-btn">⬅️ КЪМ КАРТАТА</a>', unsafe_allow_html=True)
            try:
                with open("galaxy.png", "rb") as f: enc = base64.b64encode(f.read()).decode()
                st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{enc}" style="width:100%; max-height:85vh;"></div>', unsafe_allow_html=True)
            except:
                st.markdown('<div style="text-align:center;"><img src="https://raw.githubusercontent.com/zahari89/astro-images/main/galaxy.png" style="width:100%;"></div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([1, 2, 1])
            with c2:
                # ЧЕРНИЯТ БУТОН
                st.markdown("""<style>div.stButton > button { background-color: black !important; border: 2px solid #FFD700 !important; color: #FFD700 !important; font-weight: 900; box-shadow: 0 0 15px rgba(255,215,0,0.5); margin-top: -30px; margin-bottom: 50px; } div.stButton > button:hover { box-shadow: 0 0 25px #FFD700 !important; background-color: #111 !important; }</style>""", unsafe_allow_html=True)
                if st.button("✨ ЗАПОЧНИ СВОЯ ХОРОСКОП ✨", key="pc_start", use_container_width=True):
                    st.session_state['start_horoscope'] = True; st.rerun()
        else:
            # МЕНЮ И ФОРМИ - DESKTOP
            st.markdown("""<style>.stApp { background-image: none !important; background-color: #000000 !important; }</style>""", unsafe_allow_html=True)
            if st.session_state['western_cat'] is None:
                # ХУБАВ БУТОН НАЗАД (Стрелка)
                c_back, _, _ = st.columns([1, 4, 1])
                with c_back:
                    if st.button("⬅️ НАЗАД", key="pc_back2", type="secondary"): 
                        st.session_state['start_horoscope'] = False; st.rerun()
                
                # ТУК: Добавям разстояние, за да не се блъска заглавието в стрелката
                st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
                
                st.markdown("<h1 style='text-align: center; color: #FFD700;'>✨ ИЗБЕРИ СВОЯ ПЪТ ✨</h1><div style='height:50px'></div>", unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                def cat_btn(title, desc, color, key_name):
                    st.markdown(f"""<div style='text-align: center; margin-bottom: 20px;'><div style='color: {color}; font-size: 22px; font-weight: 900; text-transform: uppercase; text-shadow: 0 0 15px {color}; margin-bottom: 10px;'>{title}</div><div style='color: #E0E0E0; font-style: italic;'>{desc}</div></div>""", unsafe_allow_html=True)
                    if st.button("👉 ОТВОРИ", key=f"btn_{key_name}", use_container_width=True): st.session_state['western_cat'] = key_name; st.rerun()
                
                with col1: cat_btn(western_menu_data['destiny']['title'], western_menu_data['destiny']['desc'], western_menu_data['destiny']['color'], 'destiny')
                with col2: cat_btn(western_menu_data['love']['title'], western_menu_data['love']['desc'], western_menu_data['love']['color'], 'love')
                with col3: cat_btn(western_menu_data['future']['title'], western_menu_data['future']['desc'], western_menu_data['future']['color'], 'future')
                with col4: cat_btn(western_menu_data['money']['title'], western_menu_data['money']['desc'], western_menu_data['money']['color'], 'money')
            else:
                cat = st.session_state['western_cat']; data = western_menu_data[cat]
                c_back, c_title, _ = st.columns([1, 4, 1])
                with c_back:
                    if st.button("⬅️ МЕНЮ", key="pc_back3", type="secondary"): st.session_state['western_cat'] = None; st.rerun()
                
                # И ТУК: Добавям малко въздух отгоре
                st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
                
                with c_title: st.markdown(f"<h2 style='text-align:center; color:{data['color']};'>{data['title']}</h2>", unsafe_allow_html=True)
                st.markdown("---")

                opts_col1, opts_col2, opts_col3 = st.columns(3)
                for idx, opt in enumerate(data['options']):
                    curr_col = [opts_col1, opts_col2, opts_col3][idx % 3]
                    with curr_col:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.05); padding: 8px; border-radius: 8px; margin-bottom: 10px; border-left: 2px solid {data['color']}; text-align: center;">
                            <h4 style="color: #00FFFF; margin: 0; font-size: 20px; font-weight: bold; line-height: 1.2;">{opt}</h4>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                render_main_user_smart_form(f"pc_form_{cat}", is_compatibility=(cat == "love"))
    else:
        st.title(f"PC: {st.session_state['current_view']}")
        if st.button("НАЧАЛО"): st.session_state.update(current_view='HOME'); st.rerun()

# ==============================================================================
# 6. ФУНКЦИЯ ЗА ТЕЛЕФОН (MOBILE) - СИМУЛАТОР "ЧЕРЕН ЕКРАН"
# ==============================================================================
def run_mobile():
    # ТОВА Е НОВИЯТ ТРИК ЗА "ТЕЛЕФОН В ТЪМНОТО"
    st.markdown(f"""
    <style>
        /* ЦЕЛИЯТ ЕКРАН НА КОМПЮТЪРА СТАВА ЧЕРЕН */
        .stApp {{ background-color: #000000 !important; background-image: none !important; }}
        
        /* СКРИВАМЕ АДМИН ЛЕНТАТА И ХЕДЪРА НАПЪЛНО */
        header {{ display: none !important; }}
        [data-testid="stSidebar"] {{ display: none !important; }}
        [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

        /* ПРАВИМ ЦЕНТРАЛНАТА ЧАСТ ТЯСНА КАТО ТЕЛЕФОН */
        .block-container {{ 
            width: 360px !important; 
            max-width: 360px !important; 
            margin: 0 auto !important; 
            background-image: url('{bg_url}'); 
            background-size: cover; 
            min-height: 100vh; 
            border-left: 2px solid #333; 
            border-right: 2px solid #333;
            padding-top: 20px !important;
        }}

        .mob-container {{ position: relative; width: 340px; height: 500px; margin: 0 auto; }}
        .mob-sun {{ position: absolute; width: 100px; height: 100px; border-radius: 50%; background: radial-gradient(circle, #FFD700 0%, #FF8C00 100%); left: 120px; top: 180px; display: flex; justify-content: center; align-items: center; border: 4px solid white; box-shadow: 0 0 20px #FFD700; z-index: 10; color: black !important; font-weight: bold; font-size: 11px; text-align: center; }}
        .mob-planet {{ position: absolute; width: 70px; height: 40px; border-radius: 50%; display: flex; justify-content: center; align-items: center; color: white !important; font-weight: bold; font-size: 10px; z-index: 20; border: 2px solid rgba(255,255,255,0.8); backdrop-filter: blur(4px); text-decoration: none; }}
        
        .hero-back-btn {{ position: absolute; top: 20px; left: 10px; z-index: 999; text-decoration: none !important; background: rgba(0,0,0,0.6); border: 1px solid white; color: #fff; padding: 5px 15px; border-radius: 8px; font-weight: bold; font-size: 12px; }}
        
        button[kind="primary"] {{ background-color: #FF4500 !important; color: white !important; font-size: 18px !important; width: 100%; }}
        div[data-testid="stSelectbox"] > label, div[data-testid="stTextInput"] > label {{ color: #FFD700 !important; font-size: 12px !important; }}
    </style>
    """, unsafe_allow_html=True)
    
    # НЯМА ЛЯВА ЛЕНТА ТУК!

    if st.session_state['current_view'] == 'HOME':
        # МАЛКА МАНДАЛА
        mh = ['<div class="mob-container">']
        mh.append('<svg width="340" height="500" style="position: absolute; top:0; left:0; z-index:1;">')
        mx, my = 145, 175
        angs = [-90, -45, -10, 30, 65, 115, 150, 190, 225]
        for ang in angs:
            rad = math.radians(ang); x1=mx+25+(85)*math.cos(rad); y1=my+55+(140)*math.sin(rad); x2=mx+25+25*math.cos(rad); y2=my+55+25*math.sin(rad)
            mh.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#FFD700" stroke-width="1" opacity="0.6" />')
        mh.append('</svg><div class="mob-sun">ВЪРХОВНАТА<br>ИСТИНА</div>')
        for i, ang in enumerate(angs):
            m = modules[i]; rad = math.radians(ang); x=mx+115*math.cos(rad)-10; y=my+35+160*math.sin(rad)
            mh.append(f'<a href="?view={m["key"]}&device=mobile" target="_self" class="mob-planet" style="background-color: {m["color"]}; left: {x}px; top: {y}px;">{m["short"]}</a>')
        mh.append('</div>')
        st.markdown("".join(mh), unsafe_allow_html=True)

    elif st.session_state['current_view'] == 'Western':
        # ЕКРАН 1 MOBILE
        if not st.session_state['start_horoscope']:
            st.markdown("""<style>.block-container { background-image: none !important; background-color: black !important; }</style>""", unsafe_allow_html=True)
            st.markdown('<a href="?view=HOME&device=mobile" target="_self" class="hero-back-btn">⬅️ НАЗАД</a>', unsafe_allow_html=True)
            st.markdown('<img src="https://i.postimg.cc/8cVnWmFH/mobile.png" style="width:100%; height:auto;">', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✨ ЗАПОЧНИ ✨", key="mob_start", use_container_width=True):
                st.session_state['start_horoscope'] = True; st.rerun()
        else:
            # ЕКРАН 2 MOBILE (МЕНЮ И ФОРМИ)
            st.markdown("""<style>.block-container { background-image: none !important; background-color: black !important; }</style>""", unsafe_allow_html=True)
            if st.session_state['western_cat'] is None:
                if st.button("⬅️ НАЗАД", key="mob_back2"): st.session_state['start_horoscope'] = False; st.rerun()
                st.markdown("<h2 style='text-align: center; color: #FFD700;'>✨ ИЗБЕРИ ПЪТ ✨</h2>", unsafe_allow_html=True)
                for k, v in western_menu_data.items():
                    st.markdown(f"<div style='text-align:center; margin-top:20px'><h4 style='color:{v['color']}'>{v['title']}</h4></div>", unsafe_allow_html=True)
                    if st.button("👉 ОТВОРИ", key=f"mob_btn_{k}", use_container_width=True): st.session_state['western_cat'] = k; st.rerun()
            else:
                cat = st.session_state['western_cat']; data = western_menu_data[cat]
                if st.button("⬅️ НАЗАД", key="mob_back3"): st.session_state['western_cat'] = None; st.rerun()
                st.markdown(f"<h3 style='text-align:center; color:{data['color']}'>{data['title']}</h3>", unsafe_allow_html=True)
                st.markdown("---")
                render_main_user_smart_form(f"mob_form_{cat}", is_compatibility=(cat == "love"))

    else:
        st.title(f"Mobile: {st.session_state['current_view']}")
        if st.button("НАЧАЛО"): st.session_state.update(current_view='HOME'); st.rerun()

# ==============================================================================
# 7. ИЗПЪЛНЕНИЕ
# ==============================================================================
if device_type == "mobile":
    run_mobile()
else:
    run_desktop()

# --- ТЕСТ НА ВРЪЗКАТА ---
st.sidebar.markdown("---")
st.sidebar.success("🚀 Система: Онлайн (GitHub свързан!)")