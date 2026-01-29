"""
Автоматичен инсталатор на Swiss Ephemeris файлове за астероиди
Автор: Astro Engine v3
Дата: 2026-01-23
"""

import os
import sys
import urllib.request
from pathlib import Path

# Папка за ephemeris файлове
SCRIPT_DIR = Path(__file__).parent
EPHE_DIR = SCRIPT_DIR / "ephe"

# Swiss Ephemeris файлове - нужни за периода 1800-2100
EPHEMERIS_FILES = {
    # Планети (1800-1900, 1900-2000, 2000-2100)
    "sepl_18.se1": "http://www.astro.com/ftp/swisseph/ephe/sepl_18.se1",
    "sepl_19.se1": "http://www.astro.com/ftp/swisseph/ephe/sepl_19.se1", 
    "sepl_20.se1": "http://www.astro.com/ftp/swisseph/ephe/sepl_20.se1",
    
    # Луна (1800-1900, 1900-2000, 2000-2100)
    "semo_18.se1": "http://www.astro.com/ftp/swisseph/ephe/semo_18.se1",
    "semo_19.se1": "http://www.astro.com/ftp/swisseph/ephe/semo_19.se1",
    "semo_20.se1": "http://www.astro.com/ftp/swisseph/ephe/semo_20.se1",
    
    # Астероиди (1800-2099)
    "seas_18.se1": "http://www.astro.com/ftp/swisseph/ephe/seas_18.se1",
}

def create_ephe_directory():
    """Създава папка ephe ако не съществува"""
    if not EPHE_DIR.exists():
        EPHE_DIR.mkdir(parents=True)
        print(f"[OK] Създадена папка: {EPHE_DIR}")
    else:
        print(f"[OK] Папка вече съществува: {EPHE_DIR}")
    return EPHE_DIR

def download_file_with_progress(url, destination):
    """Download файл с прогрес бар"""
    try:
        # Опит за tqdm прогрес бар
        try:
            from tqdm import tqdm
            use_tqdm = True
        except ImportError:
            use_tqdm = False
            print(f"   (Инсталирай 'tqdm' за прогрес бар: pip install tqdm)")
        
        # Проверка размер на файла
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req) as response:
            file_size = int(response.headers.get('Content-Length', 0))
        
        # Download с прогрес
        if use_tqdm and file_size > 0:
            # С tqdm прогрес бар
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=destination.name) as pbar:
                def reporthook(block_num, block_size, total_size):
                    downloaded = block_num * block_size
                    if downloaded <= total_size:
                        pbar.update(block_size)
                
                urllib.request.urlretrieve(url, destination, reporthook=reporthook)
        else:
            # Без прогрес бар - с точки
            print(f"   Download {destination.name} ({file_size / (1024*1024):.1f} MB)...", end='', flush=True)
            
            def simple_progress(block_num, block_size, total_size):
                if block_num % 50 == 0:  # Точка на всеки 50 блока
                    print('.', end='', flush=True)
            
            urllib.request.urlretrieve(url, destination, reporthook=simple_progress)
            print(" OK!")
        
        return True
        
    except urllib.error.HTTPError as e:
        print(f"\n   [ERROR] HTTP Error {e.code}: Файлът не е намерен на сървъра")
        return False
    except Exception as e:
        print(f"\n   [ERROR] Грешка: {e}")
        return False

def install_ephemeris_files():
    """Главна функция - download на всички нужни файлове"""
    print("=" * 70)
    print("SWISS EPHEMERIS АВТОМАТИЧЕН ИНСТАЛАТОР")
    print("=" * 70)
    print()
    
    # Стъпка 1: Създаване на папка
    ephe_dir = create_ephe_directory()
    print()
    
    # Стъпка 2: Download на файлове
    print(f"Започвам download на {len(EPHEMERIS_FILES)} файла...")
    print("-" * 70)
    
    downloaded = 0
    skipped = 0
    failed = 0
    
    for filename, url in EPHEMERIS_FILES.items():
        filepath = ephe_dir / filename
        
        # Проверка дали вече съществува
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024 * 1024)
            print(f"[SKIP] {filename} - вече съществува ({size_mb:.1f} MB)")
            skipped += 1
            continue
        
        # Download
        print(f"\n[DOWN] Download: {filename}")
        print(f"   URL: {url}")
        
        if download_file_with_progress(url, filepath):
            if filepath.exists():
                size_mb = filepath.stat().st_size / (1024 * 1024)
                print(f"   [OK] Успешно! ({size_mb:.1f} MB)")
                downloaded += 1
            else:
                print(f"   [ERROR] Файлът не е записан!")
                failed += 1
        else:
            failed += 1
    
    # Резултати
    print()
    print("=" * 70)
    print("РЕЗУЛТАТИ:")
    print(f"  [OK] Download-нати:  {downloaded}")
    print(f"  [SKIP] Пропуснати:   {skipped} (вече съществуват)")
    print(f"  [ERROR] Неуспешни:   {failed}")
    print("=" * 70)
    
    # Показваме какво има в папката
    print()
    print("Файлове в папка ephe/:")
    print("-" * 70)
    
    all_files = sorted(ephe_dir.glob("*.se1"))
    total_size = 0
    
    for f in all_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        total_size += size_mb
        print(f"  - {f.name:20} ({size_mb:6.1f} MB)")
    
    print("-" * 70)
    print(f"TOTAL: {len(all_files)} файла, {total_size:.1f} MB")
    print()
    
    # Инструкции за употреба
    print("=" * 70)
    print("КАК ДА ИЗПОЛЗВАШ:")
    print("=" * 70)
    print()
    print("В astro_engine_v1.py добави в началото:")
    print()
    print(f"  import swisseph as swe")
    print(f"  swe.set_ephe_path(r'{ephe_dir}')")
    print()
    print("=" * 70)
    
    return downloaded > 0 or skipped > 0

if __name__ == "__main__":
    try:
        success = install_ephemeris_files()
        
        if success:
            print("\n[OK] ИНСТАЛАЦИЯТА Е ЗАВЪРШЕНА УСПЕШНО!")
            sys.exit(0)
        else:
            print("\n[ERROR] ИНСТАЛАЦИЯТА НЕУСПЕШНА - моля проверете грешките!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n[STOP] Прекъснато от потребителя!")
        sys.exit(2)
    except Exception as e:
        print(f"\n[ERROR] КРИТИЧНА ГРЕШКА: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(3)
