import tensorflow as tf
from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import numpy as np

# ==============================
# 🔹 1. Load model dan tokenizer
# ==============================
MODEL_PATH = r"result"  # lokasi folder tempat kamu menyimpan model
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = TFAutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

# ==============================
# 🔹 2. Fungsi Prediksi Sentimen
# ==============================
def predict_sentiment(text):
    # Tokenisasi input
    tokens = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=128,
        return_tensors="tf"
    )

    # Prediksi
    logits = model(**tokens).logits
    probs = tf.nn.softmax(logits, axis=-1)
    label_id = tf.argmax(probs, axis=1).numpy()[0]
    return label_id, probs.numpy()[0]

# ==============================
# 🔹 3. Uji dengan contoh teks
# ==============================

import streamlit as st

sample_text = st.text_input("Masukkan Teks untuk Diprediksi:")
if st.button("Prediksi"):
    label, prob = predict_sentiment(sample_text)
    st.write("Prediksi Label:", ["Negatif", "Netral", "Positif"][label])
    st.write("Probabilitas:", prob)

# sample_text = input("Masukan Text Untuk Diprediksi: ")
# label, prob = predict_sentiment(sample_text)

# # Mapping label (ubah sesuai dataset kamu)
# if label == 2:
#     print("Prediksi Label: Positif")
# elif label == 1:
#     print("Prediksi Label: Netral")
# else:
#     print("Prediksi Label: Negatif")

# print("Probabilitas:", prob)
