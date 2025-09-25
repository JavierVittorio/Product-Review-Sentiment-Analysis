# amazon_reviews_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd
from selenium.webdriver.chrome.service import Service

def make_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
    )

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    return driver


def scrape_amazon_reviews(product_reviews_url, max_pages=5, headless=True, delay_range=(1.0, 3.0)):
    """
    Ambil review text dan bintang (rating) dari halaman review Amazon.
    - product_reviews_url: URL halaman "All reviews", contoh:
      https://www.amazon.com/product-reviews/ASIN/   atau
      https://www.amazon.com/<product>/product-reviews/<ASIN>/
    - max_pages: jumlah halaman review yang akan diproses (default 5)
    """
    driver = make_driver(headless=headless)
    wait = WebDriverWait(driver, 15)
    results = []

    try:
        url = product_reviews_url
        driver.get(url)

        for page in range(1, max_pages + 1):
            # tunggu review container muncul
            try:
                wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-hook='review']")))
            except:
                # jika tidak muncul, break (mungkin diblokir atau tidak ada review)
                print(f"[!] Tidak menemukan review pada halaman {page}. Mungkin diblokir/struktur berbeda.")
                break

            time.sleep(random.uniform(*delay_range))

            review_blocks = driver.find_elements(By.XPATH, "//div[@data-hook='review']")
            print(f"[i] Halaman {page}: menemukan {len(review_blocks)} review")

            for r in review_blocks:
                # rating (misal "5.0 out of 5 stars")
                try:
                    rating_el = r.find_element(By.XPATH, ".//i[@data-hook='review-star-rating' or @data-hook='cmps-review-star-rating']//span")
                    rating_text = rating_el.get_attribute("innerText").strip()
                except:
                    # alternatif selector
                    try:
                        rating_el = r.find_element(By.XPATH, ".//i[@data-hook='review-star-rating']//span")
                        rating_text = rating_el.get_attribute("innerText").strip()
                    except:
                        rating_text = None

                # Ambil angka dari rating_text (contoh '5.0 out of 5 stars' -> '5.0')
                rating_value = None
                if rating_text:
                    parts = rating_text.split()
                    if len(parts) > 0:
                        # ambil bagian pertama yang berisi angka
                        rating_value = parts[0].replace(",", ".")  # ganti koma jika ada

                # review text
                try:
                    body_el = r.find_element(By.XPATH, ".//span[@data-hook='review-body']")
                    review_text = body_el.text.strip()
                except:
                    # fallback: cari element span panjang
                    try:
                        review_text = r.find_element(By.XPATH, ".//span").text.strip()
                    except:
                        review_text = None

                results.append({
                    "rating": rating_value,
                    "review": review_text
                })

            # Coba ke halaman berikutnya
            try:
                # selector pagination next
                next_btn = driver.find_element(By.XPATH, "//li[@class='a-last']/a")
                next_href = next_btn.get_attribute("href")
                if not next_href:
                    print("[i] Tidak ada tautan next (akhir halaman).")
                    break
                # klik next (lebih andal daripada load URL langsung karena Amazon kadang mengatur cookie)
                driver.execute_script("arguments[0].click();", next_btn)
                # tunggu sedikit sebelum memproses page berikutnya
                time.sleep(random.uniform(1.0, 2.5))
            except Exception as e:
                print(f"[i] Gagal menemukan tombol next atau paging selesai: {e}")
                break

        return results

    finally:
        driver.quit()

if __name__ == "__main__":
    # Contoh: gunakan URL halaman review produk Amazon.
    # Cara mudah dapatkan: buka produk di Amazon -> klik "See all reviews" -> salin URL
    # Contoh URL (ganti dengan produk target Anda):
    product_reviews_url = "https://www.amazon.com/product-reviews/B08N5WRWNW"  # ganti dengan URL review yang valid
    reviews = scrape_amazon_reviews(product_reviews_url, max_pages=10, headless=False)
    print("Total reviews scraped:", len(reviews))

    # Simpan ke CSV / JSON
    df = pd.DataFrame(reviews)
    df.to_csv("amazon_reviews.csv", index=False, encoding="utf-8-sig")
    df.to_json("amazon_reviews.json", orient="records", force_ascii=False)
    print("Disimpan ke amazon_reviews.csv / amazon_reviews.json")
