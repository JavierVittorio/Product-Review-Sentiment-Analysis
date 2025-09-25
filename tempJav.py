import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# --- KONFIGURASI ---
URL = "https://www.tokopedia.com/vicochairs/kursi-kantor-kursi-jaring-kursi-staff-1731892250275579665/review"
CHROMEDRIVER_PATH = r"chromedriver-win64/chromedriver.exe"   # ganti sesuai lokasi chromedriver
OUTPUT_FILE = "reviews.csv"
# --------------------

# Inisialisasi driver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

driver.get(URL)
time.sleep(3)

# Klik tab "Ulasan" kalau ada
try:
    review_tab = driver.find_element(By.XPATH, "//button[contains(text(), 'Ulasan')]")
    review_tab.click()
    print("Tab ulasan ditemukan dan diklik")
    time.sleep(2)
except:
    print("Tab ulasan tidak ditemukan, mungkin langsung tampil")

# Ambil semua review
reviews = driver.find_elements(By.CSS_SELECTOR, "section.css-1799hu")

print("Reviews:",reviews)

data = []
for r in reviews:
    try:
        # Ambil rating (jumlah bintang terisi)
        stars = r.find_elements(By.XPATH, ".//svg[@aria-hidden='true']")
        rating = len(stars)

        # Ambil teks ulasan
        text_elem = r.find_element(By.XPATH, "//span[@data-testid='lblItemUlasan']")
        text = text_elem.text.strip()

        data.append({"rating": rating, "review": text})
    except:
        pass

# Simpan ke CSV
df = pd.DataFrame(data)
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"Scraping selesai, total {len(df)} ulasan disimpan ke {OUTPUT_FILE}")

driver.quit()
