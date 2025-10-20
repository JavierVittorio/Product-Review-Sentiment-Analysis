import pandas as pd
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from tqdm import tqdm
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Load the dataset
df = pd.read_excel('Dataset Text Web.xlsx')

# Manual normalization dictionary
normalization_dict = {
    'dgn': 'dengan',
    'yg': 'yang',
    'gk': 'tidak',
    'ga': 'tidak',
    'tdk': 'tidak',
    'gak': 'tidak',
    'utk': 'untuk',
    'u': 'untuk',
    'udh': 'sudah',
    'udah': 'sudah',
    'aja': 'saja',
    'bgt': 'banget',
    'dah': 'sudah',
    'emg': 'memang',
    'kmrn': 'kemarin',
    'skrg': 'sekarang',
    'bs': 'bisa',
    'bisa': 'dapat',
    'hrs': 'harus',
    'tp': 'tapi',
    'trs': 'terus',
    'krn': 'karena',
    'sy': 'saya',
    'org': 'orang',
    'q': 'aku'
}

# Manual stopwords list (extend this list as needed)
stopwords = {
    'yang', 'di', 'ke', 'dari', 'pada', 'dalam', 'untuk', 'dengan', 'dan', 'atau',
    'ini', 'itu', 'juga', 'sudah', 'saya', 'anda', 'dia', 'mereka', 'kita', 'akan',
    'bisa', 'ada', 'tidak', 'saat', 'oleh', 'setelah', 'tentang', 'seperti', 'ketika',
    'bagi', 'sampai', 'karena', 'jika', 'namun', 'serta', 'lain', 'sebuah', 'para',
    'masih', 'hal', 'setiap', 'harus', 'besar', 'pada', 'telah', 'dapat', 'sekarang',
    'lalu', 'sangat', 'sementara', 'tetapi', 'sehingga', 'lagi'
}


#--------------------------------------------------
# INI BATAS
# -------------------------------------------------

# Normalisasi: ['mini', 'cocok', 'hrgany', 'wangi', 'amanaah', 'pnipuan', 'biasaa', 'fress', 'harum', 'sekali', 'murah', 'bagus', 'waktu', 'lamaa', 'sekaliiii', 'kecewa', 'polll', 'dikit', 'kecil', 'susah', 'parfum']
# Stopwords ['kira', 'ternyata', 'sic', 'dg', 'emang', 'cm', 'rb', 'aj', 'parfumnya', 'kok', 'koyok', 'ngengek', 'dikirim', 'minyak', 'mili', 'iklan', 'nya', 'mli', 'sunggu', 'luar', 'awalnya', 'beneran', 'serahan', 'jasa', 'kirim', 'baca', 'betul', 'cuma', 'tester', 'baik', 'testyr', 'kurang', 'relatif', 'kualitas', 'produk', 'sesuai', 'pesanan', 'pengiriman', 'tepat', 'kemasan', 'mantab', 'gan', 'ngakak', 'tau', 'kalau', 'mana', 'isinya', 'bukanya', 'ralat', 'botolan', 'diskripsi', 'perlu', 'biasa', 'mksih', 'kak', 'paketnya', 'cepat', 'barang', 'semoga', 'sukses', 'sellu', 'buat', 'tokonya', 'akibat']

#--------------------------------------------------
# INI BATAS
# -------------------------------------------------



list_kata = []
count_kata = []
word_freq = {}

def preprocess_text(text):
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text)
    
    # Remove numbers and special characters
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Get Sastrawi stopwords
    sastrawi_stopwords = StopWordRemoverFactory().get_stop_words()
    
    # Split into words
    words = text.split()
    
    
    for word in words:
        if (word not in normalization_dict and word not in stopwords and word not in sastrawi_stopwords):
            if(len(list_kata) == 0):
                list_kata.append(word)
                count_kata.append(1)
            else:
                for i in range(0, len(list_kata)):
                    if(list_kata[i] == word):
                        count_kata[i] += 1
                        break
                    elif(list_kata[len(list_kata)-1] != word and i == len(list_kata)-1):
                        list_kata.append(word)
                        count_kata.append(1)
                # print(list_kata[len(list_kata)-1] != word)

        # if (word not in normalization_dict and 
        #     word not in stopwords and 
        #     word not in sastrawi_stopwords):
        #     word_freq[word] = word_freq.get(word, 0) + 1
    
    # Print unique words and their frequencies if any found
    # print(words)
    # if word_freq:
    #     print("\nUnique words and their frequencies:")
    #     for word, freq in sorted(word_freq.items()):
    #         print(f"{word}: {freq}")
    
    # Normalize words
    normalized_words = [normalization_dict.get(word, word) for word in words]
    
    # Remove stopwords
    cleaned_words = [word for word in normalized_words if word not in stopwords]
    
    return ' '.join(cleaned_words)

# Function to find words not in Sastrawi stopwords
def find_unique_stopwords():
    sastrawi_stopwords = StopWordRemoverFactory().get_stop_words()
    
    manual_not_in_sastrawi = set(stopwords) - set(sastrawi_stopwords)
    sastrawi_not_in_manual = set(sastrawi_stopwords) - set(stopwords)
    
    # print("\nWords in our manual stopwords but not in Sastrawi:")
    # print(sorted(manual_not_in_sastrawi))
    # print("\nWords in Sastrawi but not in our manual stopwords:")
    # print(sorted(sastrawi_not_in_manual))

# Preprocess the dataset
# print("Preprocessing the dataset...")
df['processed_text'] = df['review'].apply(preprocess_text)

# Show words not in Sastrawi
# find_unique_stopwords()
print(list_kata)

list_stopwords_new = []
list_normalisasi_new = []

for i in range(0, len(list_kata)):
    print(list_kata[i])
    user_input  = input("1/2: ")
    if user_input  == '1':
        list_stopwords_new.append(list_kata[i])
    elif user_input  == '2':
        list_normalisasi_new.append(list_kata[i])
    elif user_input  == '3':
        break

print("Normalisasi:", list_normalisasi_new)
print("Stopwords", list_stopwords_new)


# Print sample of preprocessed text
# print("\nSample of preprocessed texts:")
# print(df[['review', 'processed_text']].head())

# Save preprocessed dataset
# df.to_csv('preprocessed_dataset.csv', index=False)
# print("\nPreprocessed dataset saved to 'preprocessed_dataset.csv'")