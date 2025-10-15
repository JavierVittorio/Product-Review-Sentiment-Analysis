import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

# === 1. Baca dataset dari file Excel ===
df = pd.read_excel("Dataset Text Web.xlsx")
df = df[['review']]  # ambil kolom review saja

# === 2. Dictionary normalisasi ===
normalisasi_dict = {
    "gak": "tidak",
    "ga": "tidak",
    "nggak": "tidak",
    "bgt": "banget",
    "bngt": "banget",
    "bener": "benar",
    "bgtu": "begitu",
    "tp": "tapi",
    "yg": "yang",
    "aja": "saja",
    "nih": "ini",
    "dong": "",
    "deh": "",
    "si": "",
    "msh": "masih",
    "okelah": "oke",
    "aamiin": "",
    "abang": "",
    "abis": "habis",
    "abiss": "habis",
    "abisss": "habis",
    "acara": "",
    "ada": "terdapat",
    "admin": "penjual",
    "aer": "air",
    "aesthetic": "",
    "agak": "cukup",
    "agustus": "",
    "aikr": "",
    "air": "air",
    "airnya": "air",
    "airr": "air",
    "ajaa": "saja",
    "ajah": "saja",
    "ajh": "saja",
    "alau": "walau",
}

# === 3. Stopwords manual tambahan ===
extra_stopwords = {
    "ya", "yaa", "kan", "nih", "dong", "deh", "loh", "kok",
    "sih", "lah", "nya", "tuh", "nah", "eh", "ayo", "cie", "ciee",
    "hehe", "haha", "wkwk", "wkwkwk", "akan", "akhirnya", "akibat", 
    "aku", "alamat", "alfa", "alfamart", "alhamdulilah", "alkohol", "alkoholnya",
    "allaahumma", "amaaatttt", "amah", "aman", "amanaah", "amanahbarang", "amanahbnr",
    "amanahminyak", "amanahsangat", "amanahseller", "amanterimakasih", "amat", "ampun", "anak",
    "and", "anda"
}

stop_words = set(stopwords.words('indonesian')) | extra_stopwords

def normalisasi_kata(text):
    words = text.split()
    new_words = []
    unknown_words = []

    for w in words:
        if w in stop_words:  # ← stopword, lewati dari unknown list
            continue
        if w in normalisasi_dict:
            new_words.append(normalisasi_dict[w])
        else:
            new_words.append(w)
            if len(w) > 2:
                unknown_words.append(w)
    return " ".join(new_words), unknown_words


# === 5. Fungsi cleaning ===
def clean_text(text):
    if not isinstance(text, str):
        return "", []
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    normalized_text, unknown = normalisasi_kata(text)
    tokens = word_tokenize(normalized_text)
    stop_words = set(stopwords.words('indonesian')) | extra_stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]
    cleaned_text = " ".join(filtered_tokens)
    return cleaned_text, unknown

# === 6. Terapkan cleaning + deteksi ===
df[['clean_text', 'unknown_words']] = df['review'].apply(
    lambda x: pd.Series(clean_text(x))
)

# === 7. Gabungkan semua kata yang belum dikenal ===
all_unknown_words = sorted(set(sum(df['unknown_words'], [])))

# === 8. Simpan hasil ke file baru ===
# df.to_excel("Dataset Text Web Cleaned.xlsx", index=False)

# === 9. Tampilkan ringkasan ===
print(df.head())
print("\nKata yang belum ada di kamus normalisasi:")
print(all_unknown_words)
print("\n✅ File hasil cleaning sudah disimpan sebagai 'Dataset Text Web Cleaned.xlsx'")
