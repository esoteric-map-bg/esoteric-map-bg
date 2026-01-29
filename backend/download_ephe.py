"""
Download Swiss Ephemeris files for asteroids - FIXED URLs
"""
import os
import urllib.request
from pathlib import Path

# Папка за ephemeris файлове
EPHE_DIR = Path(__file__).parent / "ephe"
EPHE_DIR.mkdir(exist_ok=True)

# Swiss Ephemeris правилен URL
BASE_URL = "https://www.astro.com/ftp/swisseph/ephe/"

# Нужни файлове - период 1800-2000 (за Айнщайн 1879)
FILES_NEEDED = [
    "seat_18.se1",  # Asteroids 1800-1900  
    "semo_18.se1",  # Moon 1800-1900
    "sepl_18.se1",  # Planets 1800-1900
]

def download_ephemeris_files():
    """Download нужните ephemeris файлове ако липсват"""
    print(f"Папка за ephemeris: {EPHE_DIR}")
    print("-" * 60)
    
    downloaded = 0
    for filename in FILES_NEEDED:
        filepath = EPHE_DIR / filename
        
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"OK {filename} - вече съществува ({size_mb:.1f} MB)")
            continue
        
        url = BASE_URL + filename
        print(f"Download: {filename}...")
        print(f"   От: {url}")
        
        try:
            urllib.request.urlretrieve(url, filepath)
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"OK {filename} - успешно! ({size_mb:.1f} MB)")
            downloaded += 1
        except urllib.error.HTTPError as e:
            print(f"ERROR HTTP {e.code}: {filename} не е намерен на сървъра")
            print(f"   Пробвам алтернативен източник...")
            # Пробваме директно от GitHub mirror
            alt_url = f"https://github.com/astrorigin/pyswisseph/raw/master/swisseph/{filename}"
            try:
                urllib.request.urlretrieve(alt_url, filepath)
                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"OK {filename} - успешно от алтернативен източник! ({size_mb:.1f} MB)")
                downloaded += 1
            except Exception as e2:
                print(f"ERROR: Не мога да download-на {filename}: {e2}")
        except Exception as e:
            print(f"ERROR при download на {filename}: {e}")
    
    print("-" * 60)
    if downloaded > 0:
        print(f"Download-нати {downloaded} файла!")
    print(f"Ephemeris файлове в: {EPHE_DIR}")
    
    # Проверка какво има в папката
    files = list(EPHE_DIR.glob("*.se1"))
    print(f"\nФайлове в папката ({len(files)} бр):")
    for f in files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"  - {f.name} ({size_mb:.1f} MB)")
    
    return str(EPHE_DIR)

if __name__ == "__main__":
    ephe_path = download_ephemeris_files()
    print(f"\nИзползвай този път в кода:")
    print(f"swe.set_ephe_path(r'{ephe_path}')")
