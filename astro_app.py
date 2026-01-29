import streamlit as st
import sys
from pathlib import Path

# Добавяме backend папката към path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

# Импортираме астро engine
from astro_engine_v1 import NatalChart

# === КОНФИГУРАЦИЯ ===
st.set_page_config(
    page_title="Астрологична Карта - LIVE",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === CSS ДИЗАЙН ===
st.markdown("""
<style>
    /* Глобален фон */
    .stApp {
        background: linear-gradient(to bottom, #0a0a1a, #1a0a2e);
        color: white;
    }
    
    /* Glassmorphism панели */
    .glass-panel {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 215, 0, 0.3);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
    }
    
    /* Златни заглавия */
    .gold-title {
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
        font-weight: bold;
        margin-bottom: 15px;
    }
    
    /* Таблици */
    .planet-table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .planet-table th {
        background: rgba(255, 215, 0, 0.2);
        color: #FFD700;
        padding: 10px;
        text-align: left;
        border-bottom: 2px solid rgba(255, 215, 0, 0.5);
    }
    
    .planet-table td {
        padding: 8px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .planet-table tr:hover {
        background: rgba(255, 215, 0, 0.1);
    }
    
    /* Ретроградна планета */
    .retrograde {
        color: #FF6B6B;
        font-weight: bold;
    }
    
    /* Бутони */
    .stButton > button {
        background: linear-gradient(135deg, #B8860B 0%, #FFD700 50%, #B8860B 100%);
        color: black;
        font-weight: bold;
        border: 2px solid white;
        border-radius: 10px;
        padding: 12px 24px;
        font-size: 16px;
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# === ЗАГЛАВИЕ ===
st.markdown("<h1 style='text-align: center; color: #FFD700; text-shadow: 0 0 20px rgba(255,215,0,0.5);'>⭐ АСТРОЛОГИЧНА КАРТА - LIVE ENGINE ⭐</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.7);'>Професионален астрологичен изчислител с Swiss Ephemeris</p>", unsafe_allow_html=True)

# === ФОРМА ЗА ДАННИ ===
st.markdown("---")
st.markdown("<h2 class='gold-title'>📝 ВЪВЕДИ ДАННИ ЗА НАТАЛНА КАРТА</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Име:", value="Albert Einstein", key="name")
    
with col2:
    date_input = st.date_input("Дата на раждане:", value=None, key="birth_date")
    
with col3:
    time_input = st.time_input("Час на раждане:", value=None, key="birth_time")

col4, col5 = st.columns(2)

with col4:
    city = st.text_input("Град на раждане:", value="Ulm, Germany", key="city")

with col5:
    # Опция за ръчни координати
    use_manual_coords = st.checkbox("Ръчни координати", key="manual_coords")

if use_manual_coords:
    col6, col7 = st.columns(2)
    with col6:
        lat = st.number_input("Latitude (°):", value=48.4, step=0.1, key="lat")
    with col7:
        lon = st.number_input("Longitude (°):", value=10.0, step=0.1, key="lon")
else:
    lat, lon = None, None

# === БУТОН ЗА ИЗЧИСЛЕНИЕ ===
st.markdown("---")
calculate_btn = st.button("✨ ИЗЧИСЛИ КАРТАТА ✨", use_container_width=True, type="primary")

# === ИЗЧИСЛЕНИЕ И ПОКАЗВАНЕ НА РЕЗУЛТАТИ ===
if calculate_btn:
    if not date_input or not time_input:
        st.error("⚠️ Моля въведи дата и час на раждане!")
    elif not city and (lat is None or lon is None):
        st.error("⚠️ Моля въведи град ИЛИ координати!")
    else:
        try:
            with st.spinner("🔮 Изчислявам астрологичната карта..."):
                # Форматиране на данните
                date_str = date_input.strftime("%Y-%m-%d")
                time_str = time_input.strftime("%H:%M")
                
                # Създаване на карта
                if use_manual_coords and lat is not None and lon is not None:
                    chart = NatalChart(
                        date_str=date_str,
                        time_str=time_str,
                        lat=lat,
                        lon=lon
                    )
                else:
                    chart = NatalChart(
                        date_str=date_str,
                        time_str=time_str,
                        city=city
                    )
            
            # УСПЕХ!
            st.success(f"✅ Картата за {name} е изчислена успешно!")
            
            # === ПОКАЗВАНЕ НА РЕЗУЛТАТИ ===
            st.markdown("---")
            st.markdown(f"<h2 class='gold-title'>🌟 НАТАЛНА КАРТА: {name.upper()}</h2>", unsafe_allow_html=True)
            
            # Информация
            info_col1, info_col2, info_col3 = st.columns(3)
            with info_col1:
                st.info(f"📅 **Дата:** {date_input.strftime('%d.%m.%Y')}")
            with info_col2:
                st.info(f"⏰ **Час:** {time_input.strftime('%H:%M')}")
            with info_col3:
                st.info(f"🌍 **Място:** {chart.city}")
            
            # === ЪГЛИ ===
            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
            st.markdown("<h3 class='gold-title'>🎯 ОСНОВНИ ЪГЛИ</h3>", unsafe_allow_html=True)
            
            angles_html = "<table class='planet-table'>"
            angles_html += "<tr><th>Ъгъл</th><th>Знак</th><th>Позиция</th></tr>"
            
            for angle_key, angle_data in chart.angles.items():
                angles_html += f"<tr>"
                angles_html += f"<td><b>{angle_data['name_bg']}</b></td>"
                angles_html += f"<td>{angle_data['sign_bg']}</td>"
                angles_html += f"<td>{angle_data['position']}</td>"
                angles_html += f"</tr>"
            
            angles_html += "</table>"
            st.markdown(angles_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # === ПЛАНЕТИ ===
            st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
            st.markdown("<h3 class='gold-title'>🪐 ПЛАНЕТИ</h3>", unsafe_allow_html=True)
            
            planets_html = "<table class='planet-table'>"
            planets_html += "<tr><th>Планета</th><th>Знак</th><th>Позиция</th><th>Статус</th></tr>"
            
            for planet_name, planet_data in chart.planets.items():
                retro = " <span class='retrograde'>R</span>" if planet_data.get('retrograde') else ""
                planets_html += f"<tr>"
                planets_html += f"<td><b>{planet_data['name_bg']}</b></td>"
                planets_html += f"<td>{planet_data['sign_bg']}</td>"
                planets_html += f"<td>{planet_data['position']}</td>"
                planets_html += f"<td>{retro if retro else '—'}</td>"
                planets_html += f"</tr>"
            
            planets_html += "</table>"
            st.markdown(planets_html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # === ДОМОВЕ ===
            col_houses1, col_houses2 = st.columns(2)
            
            with col_houses1:
                st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                st.markdown("<h3 class='gold-title'>🏠 ДОМОВЕ 1-6</h3>", unsafe_allow_html=True)
                
                houses_html = "<table class='planet-table'>"
                houses_html += "<tr><th>Дом</th><th>Знак на куспида</th><th>Градус</th></tr>"
                
                for house_num in range(1, 7):
                    house_data = chart.houses[house_num]
                    houses_html += f"<tr>"
                    houses_html += f"<td><b>Дом {house_num}</b></td>"
                    houses_html += f"<td>{house_data['cusp_sign_bg']}</td>"
                    houses_html += f"<td>{house_data['cusp_position']}</td>"
                    houses_html += f"</tr>"
                
                houses_html += "</table>"
                st.markdown(houses_html, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col_houses2:
                st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                st.markdown("<h3 class='gold-title'>🏠 ДОМОВЕ 7-12</h3>", unsafe_allow_html=True)
                
                houses_html = "<table class='planet-table'>"
                houses_html += "<tr><th>Дом</th><th>Знак на куспида</th><th>Градус</th></tr>"
                
                for house_num in range(7, 13):
                    house_data = chart.houses[house_num]
                    houses_html += f"<tr>"
                    houses_html += f"<td><b>Дом {house_num}</b></td>"
                    houses_html += f"<td>{house_data['cusp_sign_bg']}</td>"
                    houses_html += f"<td>{house_data['cusp_position']}</td>"
                    houses_html += f"</tr>"
                
                houses_html += "</table>"
                st.markdown(houses_html, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # === АСПЕКТИ ===
            if chart.aspects:
                st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
                st.markdown(f"<h3 class='gold-title'>✨ АСПЕКТИ ({len(chart.aspects)} намерени)</h3>", unsafe_allow_html=True)
                
                aspects_html = "<table class='planet-table'>"
                aspects_html += "<tr><th>Планета 1</th><th>Аспект</th><th>Планета 2</th><th>Орбис</th><th>Точност</th></tr>"
                
                for aspect in chart.aspects[:20]:  # Показваме първите 20
                    exact = "⭐ Точен!" if aspect['exact'] else ""
                    aspects_html += f"<tr>"
                    aspects_html += f"<td>{aspect['planet1_bg']}</td>"
                    aspects_html += f"<td><b>{aspect['aspect_bg']}</b></td>"
                    aspects_html += f"<td>{aspect['planet2_bg']}</td>"
                    aspects_html += f"<td>{aspect['orb']:.2f}°</td>"
                    aspects_html += f"<td>{exact}</td>"
                    aspects_html += f"</tr>"
                
                aspects_html += "</table>"
                st.markdown(aspects_html, unsafe_allow_html=True)
                
                if len(chart.aspects) > 20:
                    st.info(f"... и още {len(chart.aspects) - 20} аспекта")
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            # === СТАТИСТИКА ===
            st.markdown("---")
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                st.metric("Планети", len(chart.planets))
            with stat_col2:
                st.metric("Ъгли", len(chart.angles))
            with stat_col3:
                st.metric("Аспекти", len(chart.aspects))
            with stat_col4:
                retro_count = sum(1 for p in chart.planets.values() if p.get('retrograde'))
                st.metric("Ретроградни", retro_count)
            
        except Exception as e:
            st.error(f"❌ Грешка при изчисление: {str(e)}")
            st.exception(e)

# === FOOTER ===
st.markdown("---")
st.markdown("<p style='text-align: center; color: rgba(255,255,255,0.5); font-size: 0.9rem;'>© 2026 Астрологична Карта - Swiss Ephemeris Backend v3</p>", unsafe_allow_html=True)
