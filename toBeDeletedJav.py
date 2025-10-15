import pandas as pd
import re
import string
from collections import Counter

# === 1. Baca dataset Excel ===
df = pd.read_excel("Dataset Text Web.xlsx")

# === 2. Ambil kolom teks (ubah sesuai nama kolom kamu) ===
texts = df['review']  # ganti dengan nama kolom sebenarnya

# === 3. Bersihkan teks dasar ===
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # hapus angka & simbol
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df['cleaned'] = texts.apply(clean_text)

# === 4. Tokenisasi semua kata ===
all_words = ' '.join(df['cleaned']).split()

print(all_words[:200])  # contoh 20 kata pertama

# === 5. Kata unik + frekuensi ===
word_freq = Counter(all_words)

# === 6. Contoh daftar kata baku sederhana (simulasi KBBI) ===
kata_baku = {"yang", "tidak", "barang", "terima", "kasih", "sampai", "amanah", "penipuan", "kak", "minyak", "dikirim"}

# === 7. Cari kata yang tidak ada di kamus baku ===
unknown_words = [w for w in word_freq if w not in kata_baku and len(w) > 2]

# === 8. Tampilkan beberapa kandidat kata untuk dinormalisasi ===
# print("Kata yang perlu dicek (kemungkinan perlu dinormalisasi):\n")
# for w in unknown_words[:30]:
#     print(f"- {w}")

# === 9. (Opsional) Tambahkan ke normalisasi_dict secara manual ===
# normalisasi_dict = {}
# for w in unknown_words[:30]:
#     suggestion = input(f"Masukkan bentuk baku untuk '{w}' (tekan ENTER jika biarkan): ")
#     if suggestion:
#         normalisasi_dict[w] = suggestion

# print("\n=== Kamus Normalisasi Baru ===")
# print(normalisasi_dict)
