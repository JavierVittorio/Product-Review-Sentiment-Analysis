from transformers import TFBertForSequenceClassification, BertTokenizer
import numpy as np
from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import train_test_split

# Ganti path ke file kamu
DATA_PATH = r"Dataset Text Web.xlsx"

# Misalnya sheet berisi kolom: "text" dan "label"
df = pd.read_excel(DATA_PATH)

# Cek dulu struktur datanya
print(df.head())

# Split data menjadi train & test
train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["review"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
)


# Tokenisasi ulang data
train_encodings = tokenizer(
    list(train_texts),
    truncation=True,
    padding=True,
    max_length=128,
    return_tensors="tf"
)

test_encodings = tokenizer(
    list(test_texts),
    truncation=True,
    padding=True,
    max_length=128,
    return_tensors="tf"
)
# Load model & tokenizer dari folder "result"
model = TFBertForSequenceClassification.from_pretrained("result")
tokenizer = BertTokenizer.from_pretrained("result")

# Prediksi menggunakan model yang sudah diload
y_train_pred_logits = model.predict(train_encodings).logits
y_test_pred_logits = model.predict(test_encodings).logits

y_train_pred = np.argmax(y_train_pred_logits, axis=1)
y_test_pred = np.argmax(y_test_pred_logits, axis=1)

# Hitung akurasi
train_acc = accuracy_score(train_labels, y_train_pred)
test_acc = accuracy_score(test_labels, y_test_pred)

print(f"Training Accuracy: {train_acc:.4f}")
print(f"Test Accuracy: {test_acc:.4f}")
print(f"Gap: {train_acc - test_acc:.4f}")
