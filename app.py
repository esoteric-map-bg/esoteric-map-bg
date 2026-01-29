import streamlit as st
import datetime

# --- 1. ГЛОБАЛНИ НАСТРОЙКИ ---
st.set_page_config(page_title="MYSTIC MASTER", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

# --- 2. ПАМЕТ И СЪСТОЯНИЕ ---
if 'astro_section' not in st.session_state: st.session_state.astro_section = "menu" 
if 'main_user' not in st.session_state: st.session_state.main_user = None 

# --- 3. ДИНАМИЧЕН ДИЗАЙН ---
css_space = """
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1465101162946-4377e57745c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1778&q=80");
    background-size: cover; background-position: center center; background-repeat: no-repeat; background-attachment: fixed;
}
.stApp::before {
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.5); z-index: -1;
}
</style>
"""

css_work_mode = """
<style>
.stApp {
    background-image: none !important;
    background-color: #1a1a1a !important; /* ТЪМНО СИВО ЗА РАБОТА */
}
</style>
"""

if st.session_state.astro_section == "menu":
    st.markdown(css_space, unsafe_allow_html=True)
else:
    st.markdown(css_work_mode, unsafe_allow_html=True)

# Общ стил
common_css = """
<style>
/* Текстове - Бели */
h1, h2, h3, p, label, span, .stMarkdown, .stRadio label, .stSelectbox label, .stTextInput label {
    color: white !important; text-shadow: 1px 1px 2px #000000;
}
/* Описателни карета */
.intro-box {
    background-color: rgba(50, 50, 50, 0.6);
    border-left: 5px solid #FFD700;
    padding: 20px;
    border-radius: 10px;
    font-style: italic;
    font-size: 1.15em;
    line-height: 1.6;
    margin-bottom: 30px;
    color: #f0f0f0 !important;
}
/* БУТОНИТЕ */
div.stButton > button {
    background-color: #222222 !important; 
    color: white !important;
    border: 2px solid #FFD700 !important; 
    border-radius: 15px !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
    opacity: 1 !important;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
}
div.stButton > button:hover {
    background-color: #444444 !important; 
    border-color: #FFFFFF !important;
    transform: scale(1.02);
}
</style>
"""
st.markdown(common_css, unsafe_allow_html=True)

# --- 4. ПОМОЩНИ ДАННИ (ТУК СА НОВИТЕ ЛОГИЧЕСКИ СПИСЪЦИ) ---
DAYS = [str(i) for i in range(1, 32)]
MONTHS = ["Януари", "Февруари", "Март", "Април", "Май", "Юни", "Юли", "Август", "Септември", "Октомври", "Ноември", "Декември"]

# 1. ЗА РАЖДАНЕ: 1900 - 2027 (Минало -> Днес)
YEARS_BIRTH = [str(i) for i in range(1900, 2028)]

# 2. ЗА ПРОГНОЗИ: 1950 - 2050 (Минало <-> Бъдеще)
YEARS_HISTORY = [str(i) for i in range(1950, 2051)]

# 3. ЗА ПЛАНИРАНЕ (ЕЛЕКЦИЯ): 2025 - 2040 (Само Бъдеще)
YEARS_FUTURE = [str(i) for i in range(2025, 2041)]

# --- 5. ФУНКЦИИ ---
# mode може да бъде: "birth", "history", "future"
def render_date_selectors(key_prefix, mode="birth"):
    c_d, c_m, c_y = st.columns([1, 2, 1], gap="small")
    
    # ИЗБОР НА СПИСЪК СПОРЕД РЕЖИМА
    if mode == "birth":
        years_list = YEARS_BIRTH
    elif mode == "future":
        years_list = YEARS_FUTURE
    else: # history
        years_list = YEARS_HISTORY
    
    # Логика за подразбиране (днешна дата)
    idx_d, idx_m, idx_y = None, None, None
    
    # Ако не е раждане (т.е. е прогноза или планиране), слагаме днешна дата по подразбиране
    if mode != "birth":
        today = datetime.date.today()
        idx_d = DAYS.index(str(today.day))
        idx_m = today.month - 1
        curr_y_str = str(today.year)
        # Проверка дали текущата година я има в списъка
        if curr_y_str in years_list: 
            idx_y = years_list.index(curr_y_str)
        elif mode == "future":
            # Ако сме в бъдещето и днешната година я няма (напр. сме 2024, а списъка почва 2025)
            # слагаме първата възможна година
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
    # ЗА РОЖДЕН ДЕН ВИНАГИ ПОЛЗВАМЕ mode="birth"
    d, m, y = render_date_selectors(f"birth_{key_suffix}", mode="birth")
    c3, c4 = st.columns([1, 2])
    with c3: time_obj = st.time_input("Час:", value=None, key=f"time_{key_suffix}")
    with c4: city = st.text_input("Град на раждане:", key=f"city_{key_suffix}")
    return {"name": name, "gender": gender, "d": d, "m": m, "y": y, "time": time_obj, "city": city}

def render_main_user_smart_form(key_context):
    if st.session_state.main_user:
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

# --- 6. ЛЯВО МЕНЮ ---
with st.sidebar:
    st.header("🧩 ГЛАВНО МЕНЮ")
    selected_module = st.radio("Избери наука:", ["Астрология", "Нумерология", "Хиромантия", "Хюман Дизайн", "Психотест", "Върховен Синтез"])
    st.write("---")
    if selected_module == "Астрология":
        if st.button("🏠 Астро-Начало"):
            st.session_state.astro_section = "menu"
            st.rerun()

# --- 7. ЛОГИКА ---
if selected_module != "Астрология":
    st.title(f"✨ {selected_module}")
    st.info("🚧 Очаквайте скоро!")
else:
    # 7.1. НАЧАЛО (МЕНЮ)
    if st.session_state.astro_section == "menu":
        st.write("\n" * 2)
        st.markdown("<h1 style='text-align: center; font-size: 5em;'>МИСТИЧЕН МАСТЕР</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.8em; font-style: italic; color: #ddd;'>Отключи съдбата си.</p>", unsafe_allow_html=True)
        st.write("\n" * 3)

        c1, c2, c3, c4 = st.columns(4, gap="medium")
        with c1:
            if st.button("👤\nЛИЧЕН\nАНАЛИЗ", use_container_width=True): 
                st.session_state.astro_section = "natal"
                st.rerun()
        with c2:
            if st.button("❤️\nСЪВМЕСТИМОСТ\n(Синастрия)", use_container_width=True): 
                st.session_state.astro_section = "synastry"
                st.rerun()
        with c3:
            if st.button("🔮\nБЪДЕЩЕ\n(Прогнози)", use_container_width=True): 
                st.session_state.astro_section = "forecast"
                st.rerun()
        with c4:
            if st.button("⏳\nИЗБОР НА\nМОМЕНТ", use_container_width=True): 
                st.session_state.astro_section = "election"
                st.rerun()

    # 7.2. ЛИЧЕН АНАЛИЗ (НАТАЛ)
    elif st.session_state.astro_section == "natal":
        st.title("👤 ЛИЧЕН АНАЛИЗ")
        st.markdown('<div class="intro-box">"Това е твоят космически паспорт. Тук разглеждаме разположението на планетите в момента на първата ти глътка въздух. Наталната карта е твоят космически ДНК код. Тя не показва само какъв си, а какъв можеш да бъдеш. Тук ще разбереш силните си страни, скритите таланти и кармичните уроци."</div>', unsafe_allow_html=True)
        
        if not st.session_state.main_user:
             st.warning("👇 Моля, въведи своите данни:")
        user_data = render_main_user_smart_form("natal")
        
        if user_data:
            st.write("\n")
            st.button("🚀 ИЗЧИСЛИ КАРТАТА", type="primary", use_container_width=True)

    # 7.3. СЪВМЕСТИМОСТ (СИНАСТРИЯ)
    elif st.session_state.astro_section == "synastry":
        st.title("❤️ ЛЮБОВНА СЪВМЕСТИМОСТ")
        st.markdown('<div class="intro-box">"Любовта не е случайност. Тук наслагваме две карти една върху друга, за да видим как енергиите ви танцуват заедно. Този модул разкрива химията помежду ви. Ще разбереш дали сте сродни души, къде ще имате търкания и каква е висшата цел на вашата връзка."</div>', unsafe_allow_html=True)
        
        if not st.session_state.main_user:
            st.warning("👤 Моля, въведи твоите данни в лявата колона:")

        col_a, col_b = st.columns(2, gap="large")
        with col_a:
            st.subheader("👤 ТИ (Партньор А)")
            user_data = render_main_user_smart_form("synastry")
        with col_b:
            st.subheader("❤️ ТЕ (Партньор Б)")
            p2_data = render_person_form("partner_b", show_header=False)
            
        st.write("\n")
        st.button("🔥 ПРОВЕРИ ЛЮБОВТА", type="primary", use_container_width=True)

    # 7.4. БЪДЕЩЕ (ПРОГНОЗИ)
    elif st.session_state.astro_section == "forecast":
        st.title("🔮 ПРОГНОЗИ ЗА БЪДЕЩЕТО")
        st.markdown('<div class="intro-box">"Вселената е часовников механизъм. Планетите никога не спират да се движат. Тук ще видиш как текущото им положение активира твоята карта. Избери <b>Лична прогноза</b> за ежедневието или <b>Солар</b> за твоята лична година, за да имаш навигатор за предстоящите събития."</div>', unsafe_allow_html=True)
        
        type_forecast = st.radio("Избери тип:", ["👤 Лична прогноза", "💑 Прогноза за ДВАМА", "🎂 Солар (Годишен хороскоп)"], horizontal=True)
        st.write("---")

        if type_forecast == "💑 Прогноза за ДВАМА":
            if not st.session_state.main_user:
                 st.warning("👤 Въведи твоите данни:")
            c1, c2 = st.columns(2, gap="large")
            with c1:
                st.subheader("👤 ТИ")
                render_main_user_smart_form("forecast_p1")
            with c2:
                st.subheader("❤️ ПАРТНЬОРЪТ")
                render_person_form("forecast_p2", show_header=False)
        else:
            st.subheader("👤 Твоите данни")
            if not st.session_state.main_user:
                 st.warning("👇 Моля, въведи своите данни:")
            render_main_user_smart_form("forecast_single")

        st.write("---")
        st.subheader("📅 Период на прогнозата")
        
        # ЗА ПРОГНОЗИ ИЗПОЛЗВАМЕ mode="history" (1950-2050)
        start_d, start_m, start_y = render_date_selectors("forecast_start", mode="history")
        st.selectbox("Продължителност:", ["Дневен хороскоп", "Седмичен", "Месечен", "Годишен обзор"])
        
        st.write("\n")
        st.button("🔮 ВИЖ БЪДЕЩЕТО", type="primary", use_container_width=True)

    # 7.5. ИЗБОР НА МОМЕНТ
    elif st.session_state.astro_section == "election":
        st.title("⏳ ИЗБОР НА МОМЕНТ")
        st.markdown('<div class="intro-box">"Всяко начало има свое бъдеще. Искаш успех в бизнеса или щастие в брака? Използвай древната мъдрост на Елекционната астрология, за да избереш перфектния ден и час за старт, когато Вселената духа в платната ти."</div>', unsafe_allow_html=True)
        
        st.subheader("1. За кого търсим дата?")
        if not st.session_state.main_user:
                 st.warning("👇 Моля, въведи своите данни:")
        render_main_user_smart_form("election")
        st.write("---")
        
        c_evt, c_time = st.columns(2, gap="large")
        with c_evt:
            st.subheader("2. Какво събитие?")
            st.selectbox("Цел:", ["💼 Бизнес / Договор", "💍 Сватба / Любов", "✈️ Пътуване", "🏥 Здраве / Операция", "🏠 Имот", "✂️ Красота"])
        with c_time:
            st.subheader("3. Начална дата за търсене:")
            # ЗА ПЛАНИРАНЕ ИЗПОЛЗВАМЕ mode="future" (2025-2040)
            render_date_selectors("elec_start", mode="future")
            st.write("\n")
            st.selectbox("Период на търсене:", ["1 седмица", "1 месец", "3 месеца", "6 месеца", "1 година"])

        st.write("\n")
        st.button("⏳ НАМЕРИ ЗЛАТНИТЕ ДАТИ", type="primary", use_container_width=True)