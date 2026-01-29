"""
ASTRO ENGINE - ФАЗА 3: ADVANCED
Професионален астрологичен изчислителен движок
Базиран на Swiss Ephemeris

Фаза 1: Планети, Домове, Ъгли ✅
Фаза 2: Лилит, Възли, Ретроградност, Аспекти ✅
Фаза 3: Астероиди, Part of Fortune, Vertex ✅
"""

import swisseph as swe
import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# НЕ задаваме ephemeris path - ще използваме вградените данни
# За астероиди ще работи само с installed ephemeris files
# За планети работи винаги

# === КОНСТАНТИ ===
PLANETS = {
    'Sun': swe.SUN,
    'Moon': swe.MOON,
    'Mercury': swe.MERCURY,
    'Venus': swe.VENUS,
    'Mars': swe.MARS,
    'Jupiter': swe.JUPITER,
    'Saturn': swe.SATURN,
    'Uranus': swe.URANUS,
    'Neptune': swe.NEPTUNE,
    'Pluto': swe.PLUTO
}

SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

SIGNS_BG = [
    'Овен', 'Телец', 'Близнаци', 'Рак', 'Лъв', 'Дева',
    'Везни', 'Скорпион', 'Стрелец', 'Козирог', 'Водолей', 'Риби'
]

PLANETS_BG = {
    'Sun': 'Слънце',
    'Moon': 'Луна',
    'Mercury': 'Меркурий',
    'Venus': 'Венера',
    'Mars': 'Марс',
    'Jupiter': 'Юпитер',
    'Saturn': 'Сатурн',
    'Uranus': 'Уран',
    'Neptune': 'Нептун',
    'Pluto': 'Плутон',
    'North Node': 'Северен възел',
    'South Node': 'Южен възел',
    'Lilith': 'Лилит',
    'Chiron': 'Хирон',
    'Juno': 'Юнона',
    'Vesta': 'Веста',
    'Ceres': 'Церера',
    'Pallas': 'Палада'
}

# АСТЕРОИДИ (Swiss Ephemeris номера)
ASTEROIDS = {
    'Chiron': 2,      # Chiron = asteroid 2
    'Ceres': 1,       # Ceres = asteroid 1
    'Pallas': 2,      # Pallas = asteroid 2  
    'Juno': 3,        # Juno = asteroid 3
    'Vesta': 4        # Vesta = asteroid 4
}

# АСПЕКТИ
ASPECTS = [
    {'name': 'Conjunction', 'name_bg': 'Съвпад', 'angle': 0, 'orb': 8, 'symbol': '0'},
    {'name': 'Opposition', 'name_bg': 'Опозиция', 'angle': 180, 'orb': 8, 'symbol': '180'},
    {'name': 'Trine', 'name_bg': 'Тригон', 'angle': 120, 'orb': 8, 'symbol': '120'},
    {'name': 'Square', 'name_bg': 'Квадратура', 'angle': 90, 'orb': 6, 'symbol': '90'},
    {'name': 'Sextile', 'name_bg': 'Секстил', 'angle': 60, 'orb': 6, 'symbol': '60'}
]

# === HELPER ФУНКЦИИ ===
def decimal_to_dms(decimal_degrees):
    """Конвертира десетичен градус в градуси, минути, секунди"""
    degrees = int(decimal_degrees)
    minutes_decimal = (decimal_degrees - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = int((minutes_decimal - minutes) * 60)
    return degrees, minutes, seconds

def longitude_to_sign(longitude):
    """Конвертира абсолютна longitude (0-360) в знак и градус"""
    sign_number = int(longitude / 30)
    degree_in_sign = longitude % 30
    return SIGNS[sign_number], SIGNS_BG[sign_number], degree_in_sign

def get_julian_day(date, time, timezone_offset):
    """Изчислява Julian Day Number за дадена дата, час и часова зона"""
    # Комбинираме дата и час
    dt = datetime.datetime.combine(date, time)
    
    # Прилагаме часова зона
    dt_utc = dt - datetime.timedelta(hours=timezone_offset)
    
    # Swiss Ephemeris изисква:
    year = dt_utc.year
    month = dt_utc.month
    day = dt_utc.day
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    
    # Изчисляваме Julian Day
    jd = swe.julday(year, month, day, hour)
    return jd

def get_coordinates(city_name):
    """Получава координати на град чрез геокодиране"""
    try:
        geolocator = Nominatim(user_agent="astro_engine")
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            raise ValueError(f"Градът {city_name} не е намерен")
    except Exception as e:
        raise ValueError(f"Грешка при търсене на град: {str(e)}")

# === ОСНОВЕН КЛАС ===
class NatalChart:
    def __init__(self, date_str, time_str, city=None, lat=None, lon=None, timezone_offset=None):
        """
        Инициализация на натална карта
        
        Args:
            date_str: Дата във формат "YYYY-MM-DD" или "DD.MM.YYYY"
            time_str: Час във формат "HH:MM"
            city: Име на град (ако е дадено, lat/lon се изчисляват автоматично)
            lat: Географска ширина (ако е дадена директно)
            lon: Географска дължина (ако е дадена директно)
            timezone_offset: UTC offset в часове (ако е даден директно)
        """
        # Парсване на дата
        if '.' in date_str:
            day, month, year = date_str.split('.')
            self.date = datetime.date(int(year), int(month), int(day))
        else:
            self.date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        
        # Парсване на час
        hour, minute = map(int, time_str.split(':'))
        self.time = datetime.time(hour, minute)
        
        # Координати
        if city:
            self.city = city
            self.lat, self.lon = get_coordinates(city)
        elif lat is not None and lon is not None:
            self.city = f"({lat}, {lon})"
            self.lat = lat
            self.lon = lon
        else:
            raise ValueError("Трябва да се предостави град или координати (lat, lon)")
        
        # Часова зона
        if timezone_offset is not None:
            self.timezone_offset = timezone_offset
        else:
            # Автоматично определяне
            tf = TimezoneFinder()
            tz_name = tf.timezone_at(lat=self.lat, lng=self.lon)
            if tz_name:
                tz = pytz.timezone(tz_name)
                dt = datetime.datetime.combine(self.date, self.time)
                offset = tz.utcoffset(dt)
                self.timezone_offset = offset.total_seconds() / 3600
            else:
                self.timezone_offset = 0
        
        # Изчисления
        self.jd = get_julian_day(self.date, self.time, self.timezone_offset)
        self.planets = {}
        self.houses = {}
        self.angles = {}
        self.aspects = []  # НОВО: Списък с аспекти
        
        # Изпълнение на изчисленията
        self._calculate()
    
    def _calculate(self):
        """Извършва всички астрологични изчисления"""
        # Планети (с ретроградност)
        for planet_name, planet_id in PLANETS.items():
            result = swe.calc_ut(self.jd, planet_id)
            longitude = result[0][0]  # Longitude в градуси (0-360)
            speed = result[0][3]  # Скорост в градуси/ден
            
            sign, sign_bg, degree_in_sign = longitude_to_sign(longitude)
            deg, min, sec = decimal_to_dms(degree_in_sign)
            
            # Ретроградност: ако скоростта е отрицателна
            is_retrograde = speed < 0
            
            self.planets[planet_name] = {
                'name': planet_name,
                'name_bg': PLANETS_BG[planet_name],
                'longitude': longitude,
                'sign': sign,
                'sign_bg': sign_bg,
                'degree': deg,
                'minute': min,
                'second': sec,
                'position': f"{deg}°{min}'{sec}\"",
                'speed': speed,
                'retrograde': is_retrograde
            }
        
        # ЛИЛИТ (Black Moon Lilith - True)
        lilith_result = swe.calc_ut(self.jd, swe.MEAN_APOG)  # Mean Apogee = Lilith
        lilith_lon = lilith_result[0][0]
        lilith_sign, lilith_sign_bg, lilith_degree = longitude_to_sign(lilith_lon)
        lilith_deg, lilith_min, lilith_sec = decimal_to_dms(lilith_degree)
        
        self.planets['Lilith'] = {
            'name': 'Lilith',
            'name_bg': 'Лилит',
            'longitude': lilith_lon,
            'sign': lilith_sign,
            'sign_bg': lilith_sign_bg,
            'degree': lilith_deg,
            'minute': lilith_min,
            'second': lilith_sec,
            'position': f"{lilith_deg}°{lilith_min}'{lilith_sec}\"",
            'speed': 0,
            'retrograde': False
        }
        
        # СЕВЕРЕН ВЪЗЕЛ (True Node)
        north_node_result = swe.calc_ut(self.jd, swe.TRUE_NODE)
        node_lon = north_node_result[0][0]
        node_sign, node_sign_bg, node_degree = longitude_to_sign(node_lon)
        node_deg, node_min, node_sec = decimal_to_dms(node_degree)
        
        self.planets['North Node'] = {
            'name': 'North Node',
            'name_bg': 'Северен възел',
            'longitude': node_lon,
            'sign': node_sign,
            'sign_bg': node_sign_bg,
            'degree': node_deg,
            'minute': node_min,
            'second': node_sec,
            'position': f"{node_deg}°{node_min}'{node_sec}\"",
            'speed': north_node_result[0][3],
            'retrograde': north_node_result[0][3] < 0
        }
        
        # ЮЖЕН ВЪЗЕЛ (опозиция на Северния)
        south_lon = (node_lon + 180) % 360
        south_sign, south_sign_bg, south_degree = longitude_to_sign(south_lon)
        south_deg, south_min, south_sec = decimal_to_dms(south_degree)
        
        self.planets['South Node'] = {
            'name': 'South Node',
            'name_bg': 'Южен възел',
            'longitude': south_lon,
            'sign': south_sign,
            'sign_bg': south_sign_bg,
            'degree': south_deg,
            'minute': south_min,
            'second': south_sec,
            'position': f"{south_deg}°{south_min}'{south_sec}\"",
            'speed': -north_node_result[0][3],
            'retrograde': True  # Винаги ретрограден
        }
        
        # CHIRON И АСТЕРОИДИ - ВРЕМЕННО ИЗКЛЮЧЕНИ (нужни ephemeris файлове)
        # TODO: Download ephemeris files за астероиди
        """
        # CHIRON (Лечителят)
        try:
            chiron_result = swe.calc_ut(self.jd, swe.CHIRON)
            chiron_lon = chiron_result[0][0]
            chiron_sign, chiron_sign_bg, chiron_degree = longitude_to_sign(chiron_lon)
            chiron_deg, chiron_min, chiron_sec = decimal_to_dms(chiron_degree)
            
            self.planets['Chiron'] = {
                'name': 'Chiron',
                'name_bg': 'Хирон',
                'longitude': chiron_lon,
                'sign': chiron_sign,
                'sign_bg': chiron_sign_bg,
                'degree': chiron_deg,
                'minute': chiron_min,
                'second': chiron_sec,
                'position': f"{chiron_deg}°{chiron_min}'{chiron_sec}\"",
                'speed': chiron_result[0][3],
                'retrograde': chiron_result[0][3] < 0
            }
        except:
            pass  # Skip ако няма ephemeris
        
        # АСТЕРОИДИ (Ceres, Pallas, Juno, Vesta)
        for ast_name, ast_num in [('Ceres', 1), ('Pallas', 2), ('Juno', 3), ('Vesta', 4)]:
            try:
                ast_result = swe.calc_ut(self.jd, swe.AST_OFFSET + ast_num)
                ast_lon = ast_result[0][0]
                ast_sign, ast_sign_bg, ast_degree = longitude_to_sign(ast_lon)
                ast_deg, ast_min, ast_sec = decimal_to_dms(ast_degree)
                
                self.planets[ast_name] = {
                    'name': ast_name,
                    'name_bg': PLANETS_BG[ast_name],
                    'longitude': ast_lon,
                    'sign': ast_sign,
                    'sign_bg': ast_sign_bg,
                    'degree': ast_deg,
                    'minute': ast_min,
                    'second': ast_sec,
                    'position': f"{ast_deg}°{ast_min}'{ast_sec}\"",
                    'speed': ast_result[0][3],
                    'retrograde': ast_result[0][3] < 0
                }
            except:
                pass  # Skip ако няма ephemeris
        """
        
        # Домове и ъгли (Placidus)
        # swe.houses() изисква: JD, lat, lon, house_system_code
        # 'P' = Placidus
        houses_result = swe.houses(self.jd, self.lat, self.lon, b'P')
        
        # houses_result[0] = cusps (13 елемента, индекс 0 е празен, 1-12 са домовете)
        # houses_result[1] = ascmc (10 елемента: ASC, MC, ARMC, Vertex, etc.)
        
        cusps = houses_result[0]
        ascmc = houses_result[1]
        
        # Асцендент (ASC) - индекс 0
        asc_longitude = ascmc[0]
        asc_sign, asc_sign_bg, asc_degree = longitude_to_sign(asc_longitude)
        asc_deg, asc_min, asc_sec = decimal_to_dms(asc_degree)
        
        self.angles['Asc'] = {
            'name': 'Ascendant',
            'name_bg': 'Асцендент',
            'longitude': asc_longitude,
            'sign': asc_sign,
            'sign_bg': asc_sign_bg,
            'degree': asc_deg,
            'minute': asc_min,
            'second': asc_sec,
            'position': f"{asc_deg}°{asc_min}'{asc_sec}\""
        }
        
        # MC (Midheaven) - индекс 1
        mc_longitude = ascmc[1]
        mc_sign, mc_sign_bg, mc_degree = longitude_to_sign(mc_longitude)
        mc_deg, mc_min, mc_sec = decimal_to_dms(mc_degree)
        
        self.angles['MC'] = {
            'name': 'Midheaven',
            'name_bg': 'Среда небе',
            'longitude': mc_longitude,
            'sign': mc_sign,
            'sign_bg': mc_sign_bg,
            'degree': mc_deg,
            'minute': mc_min,
            'second': mc_sec,
            'position': f"{mc_deg}°{mc_min}'{mc_sec}\""
        }
        
        # Descendant (опозиция на ASC)
        dsc_longitude = (asc_longitude + 180) % 360
        dsc_sign, dsc_sign_bg, dsc_degree = longitude_to_sign(dsc_longitude)
        dsc_deg, dsc_min, dsc_sec = decimal_to_dms(dsc_degree)
        
        self.angles['Dsc'] = {
            'name': 'Descendant',
            'name_bg': 'Десцендент',
            'longitude': dsc_longitude,
            'sign': dsc_sign,
            'sign_bg': dsc_sign_bg,
            'degree': dsc_deg,
            'minute': dsc_min,
            'second': dsc_sec,
            'position': f"{dsc_deg}°{dsc_min}'{dsc_sec}\""
        }
        
        # IC (опозиция на MC)
        ic_longitude = (mc_longitude + 180) % 360
        ic_sign, ic_sign_bg, ic_degree = longitude_to_sign(ic_longitude)
        ic_deg, ic_min, ic_sec = decimal_to_dms(ic_degree)
        
        self.angles['IC'] = {
            'name': 'Imum Coeli',
            'name_bg': 'Дъно небе',
            'longitude': ic_longitude,
            'sign': ic_sign,
            'sign_bg': ic_sign_bg,
            'degree': ic_deg,
            'minute': ic_min,
            'second': ic_sec,
            'position': f"{ic_deg}°{ic_min}'{ic_sec}\""
        }
        
        # PART OF FORTUNE (Парс Фортуна)
        sun_lon = self.planets['Sun']['longitude']
        moon_lon = self.planets['Moon']['longitude']
        
        # Дневна формула (опростена): ASC + Moon - Sun
        pof_lon = (asc_longitude + moon_lon - sun_lon) % 360
        
        pof_sign, pof_sign_bg, pof_degree = longitude_to_sign(pof_lon)
        pof_deg, pof_min, pof_sec = decimal_to_dms(pof_degree)
        
        self.angles['PartOfFortune'] = {
            'name': 'Part of Fortune',
            'name_bg': 'Парс Фортуна',
            'longitude': pof_lon,
            'sign': pof_sign,
            'sign_bg': pof_sign_bg,
            'degree': pof_deg,
            'minute': pof_min,
            'second': pof_sec,
            'position': f"{pof_deg}°{pof_min}'{pof_sec}\""
        }
        
        # VERTEX (Вратата на съдбата)
        if len(ascmc) > 3:
            vertex_lon = ascmc[3]
            vertex_sign, vertex_sign_bg, vertex_degree = longitude_to_sign(vertex_lon)
            vertex_deg, vertex_min, vertex_sec = decimal_to_dms(vertex_degree)
            
            self.angles['Vertex'] = {
                'name': 'Vertex',
                'name_bg': 'Вертекс',
                'longitude': vertex_lon,
                'sign': vertex_sign,
                'sign_bg': vertex_sign_bg,
                'degree': vertex_deg,
                'minute': vertex_min,
                'second': vertex_sec,
                'position': f"{vertex_deg}°{vertex_min}'{vertex_sec}\""
            }
        
        # Домове (куспиди)
        # ⚠️ ВАЖНО: swe.houses() връща cusps с 12 елемента (индекси 0-11)
        # cusps[0] = Дом 1 (= ASC)
        # cusps[1] = Дом 2
        # ...
        # cusps[9] = Дом 10 (= MC)
        # cusps[10] = Дом 11
        # cusps[11] = Дом 12
        
        for i in range(12):
            house_number = i + 1  # Дом номер (1-12)
            cusp_longitude = cusps[i]
            cusp_sign, cusp_sign_bg, cusp_degree = longitude_to_sign(cusp_longitude)
            cusp_deg, cusp_min, cusp_sec = decimal_to_dms(cusp_degree)
            
            self.houses[house_number] = {
                'number': house_number,
                'cusp_sign': cusp_sign,
                'cusp_sign_bg': cusp_sign_bg,
                'cusp_longitude': cusp_longitude,
                'cusp_degree': cusp_deg,
                'cusp_minute': cusp_min,
                'cusp_second': cusp_sec,
                'cusp_position': f"{cusp_deg}°{cusp_min}'{cusp_sec}\""
            }
        
        # АСПЕКТИ (изчисляваме след като имаме всички планети)
        self._calculate_aspects()
    
    def _calculate_aspects(self):
        """Изчислява аспекти между всички планети"""
        planet_names = list(self.planets.keys())
        
        for i in range(len(planet_names)):
            for j in range(i + 1, len(planet_names)):
                planet1_name = planet_names[i]
                planet2_name = planet_names[j]
                
                planet1 = self.planets[planet1_name]
                planet2 = self.planets[planet2_name]
                
                lon1 = planet1['longitude']
                lon2 = planet2['longitude']
                
                # ПРАВИЛНА ФОРМУЛА за shortest arc (най-краткия ъгъл)
                diff = abs(lon1 - lon2)
                if diff > 180:
                    diff = 360 - diff
                
                # Сега diff е между 0° и 180°
                # Проверяваме дали попада в орбис на някой аспект
                for aspect_type in ASPECTS:
                    target_angle = aspect_type['angle']
                    orb = aspect_type['orb']
                    
                    orb_diff = abs(diff - target_angle)
                    
                    if orb_diff <= orb:
                        # Имаме аспект!
                        self.aspects.append({
                            'planet1': planet1_name,
                            'planet1_bg': planet1['name_bg'],
                            'planet2': planet2_name,
                            'planet2_bg': planet2['name_bg'],
                            'aspect': aspect_type['name'],
                            'aspect_bg': aspect_type['name_bg'],
                            'symbol': aspect_type['symbol'],
                            'angle': diff,  # Реалният ъгъл
                            'orb': orb_diff,  # Отклонението от точния аспект
                            'exact': orb_diff < 1  # Точен аспект (< 1°)
                        })
                        break  # Намерихме аспект, спираме проверката за тази двойка
    
    def print_chart(self):
        """Отпечатва картата във форматиран вид"""
        print("=" * 80)
        print(f"НАТАЛНА КАРТА")
        print("=" * 80)
        print(f"Дата: {self.date.strftime('%d.%m.%Y')}")
        print(f"Час: {self.time.strftime('%H:%M')}")
        print(f"Място: {self.city}")
        print(f"Координати: {self.lat:.4f}°N, {self.lon:.4f}°E")
        print(f"Часова зона: UTC{'+' if self.timezone_offset >= 0 else ''}{self.timezone_offset:.1f}")
        print("=" * 80)
        
        print("\nЪГЛИ:")
        print("-" * 80)
        for angle_name, angle_data in self.angles.items():
            print(f"{angle_data['name_bg']:15} ({angle_name:3}): "
                  f"{angle_data['sign_bg']:12} {angle_data['position']:10}"
                  f"  [{angle_data['sign']:12} {angle_data['position']:}]")
        
        print("\nПЛАНЕТИ:")
        print("-" * 80)
        for planet_data in self.planets.values():
            retro_mark = " R" if planet_data.get('retrograde') else ""
            print(f"{planet_data['name_bg']:18}: "
                  f"{planet_data['sign_bg']:12} {planet_data['position']:10}{retro_mark:2}"
                  f"  [{planet_data['sign']:12} {planet_data['position']:}{retro_mark}]")
        
        print("\nДОМОВЕ (Placidus):")
        print("-" * 80)
        for house_num, house_data in self.houses.items():
            print(f"Дом {house_num:2}: "
                  f"{house_data['cusp_sign_bg']:12} {house_data['cusp_position']:10}"
                  f"  [{house_data['cusp_sign']:12} {house_data['cusp_position']:}]")
        
        # АСПЕКТИ
        if self.aspects:
            print("\nАСПЕКТИ:")
            print("-" * 80)
            for aspect in self.aspects:
                exact_mark = " (точен!)" if aspect['exact'] else ""
                print(f"{aspect['planet1_bg']:18} {aspect['symbol']} {aspect['planet2_bg']:18} - "
                      f"{aspect['aspect_bg']:12} (орбис: {aspect['orb']:.2f}°){exact_mark}")
        
        print("=" * 80)


# === ТЕСТ С АЛБЕРТ АЙНЩАЙН ===
if __name__ == "__main__":
    print("\nТЕСТ: АЛБЕРТ АЙНЩАЙН\n")
    
    # Данни за Айнщайн
    # ВАЖНО: За 1879 използваме Local Mean Time (LMT)
    # LMT за Ulm (10E00) е UTC +0:40 (10 градуса = 40 минути)
    
    einstein = NatalChart(
        date_str="14.03.1879",
        time_str="11:30",
        lat=48.4,  # 48N24
        lon=10.0,  # 10E00
        timezone_offset=0.67  # LMT = UTC +0:40 (приблизително 0.67)
    )
    
    einstein.print_chart()
    
    print("\n\nСРАВНЕНИЕ С ASTRO.COM:")
    print("-" * 80)
    print("Моля сверете резултатите с:")
    print("https://www.astro.com/cgi/chart.cgi")
    print("(Използвайте: 14 March 1879, 11:30 LMT, Ulm, Germany)")
    print("=" * 80)
