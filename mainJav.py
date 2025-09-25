"""
Tokopedia Reviews Scraper - versi input
- Tidak perlu argumen command line
- User cukup input URL & jumlah review ketika program dijalankan
"""

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# -------- CONFIG (ubah sesuai hasil Inspect di Tokopedia)
SELECTORS = {
    "review_tab": "//button[contains(., 'Ulasan')]",
    "review_container": "section#review-feed",   # wadah besar semua ulasan
    "review_item": "article.css-15m2bcr",        # tiap review
    "username": "p[data-unify='Typography']",    # ini contoh, harus dicek lagi di dalam review
    "rating": "svg[aria-hidden='true']",
    "review_text": "p[data-unify='Typography']", # cek lagi teks ulasan
    "date": "p.css-xxxxxx",                      # cari elemen tanggal di dalam review
    "helpful": "button[data-testid='helpful-count']", # kalau ada
    "images": "img",                             # gambar dalam review
}


SCROLL_PAUSE = 1.0


def init_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


def open_product(driver, url):
    driver.get(url)
    try:
        tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, SELECTORS["review_tab"]))
        )
        tab.click()
        time.sleep(1)
    except Exception:
        print("⚠️ Tab ulasan tidak ditemukan, lanjutkan...")


def load_reviews(driver, max_reviews=100):
    container = driver.find_element(By.CSS_SELECTOR, SELECTORS["review_container"])
    collected = []

    while len(collected) < max_reviews:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", container)
        time.sleep(SCROLL_PAUSE)

        items = driver.find_elements(By.CSS_SELECTOR, SELECTORS["review_item"])
        if len(items) == len(collected):  # tidak ada tambahan
            break
        collected = items
    return collected[:max_reviews]


def parse_review(el):
    def get(css, attr=None):
        try:
            elem = el.find_element(By.CSS_SELECTOR, css)
            return elem.get_attribute(attr) if attr else elem.text.strip()
        except Exception:
            return None

    return {
        "username": get(SELECTORS["username"]),
        "rating": get(SELECTORS["rating"], "aria-label"),
        "review_text": get(SELECTORS["review_text"]),
        "date": get(SELECTORS["date"]),
        "helpful": get(SELECTORS["helpful"]),
        "images": "|".join(
            [img.get_attribute("src") for img in el.find_elements(By.CSS_SELECTOR, SELECTORS["images"])]
        ),
    }


def scrape(url, max_reviews=100, headless=False):
    driver = init_driver(headless)
    try:
        open_product(driver, url)
        elems = load_reviews(driver, max_reviews)
        data = [parse_review(e) for e in elems]
        return data
    finally:
        driver.quit()


def save_csv(data, filename="tokopedia_reviews_input.csv"):
    pd.DataFrame(data).to_csv(filename, index=False)
    print(f"✅ {len(data)} review tersimpan di {filename}")


# -------- MAIN
if __name__ == "__main__":
    url = input("Masukkan URL produk Tokopedia: ").strip()
    max_reviews = input("Mau ambil berapa review (default 100): ").strip()
    max_reviews = int(max_reviews) if max_reviews.isdigit() else 100

    results = scrape(url, max_reviews, headless=False)
    save_csv(results)
