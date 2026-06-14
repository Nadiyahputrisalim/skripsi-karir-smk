import pandas as pd # type: ignore

from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore

from sklearn.naive_bayes import MultinomialNB # type: ignore
import numpy as np # type: ignore

# membaca dataset
data = pd.read_csv("dataset.csv")

# data training
X = data["jawaban"]

# label
y = data["hasil"]

# ubah teks jadi angka
vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

# model naive bayes
model = MultinomialNB()

# training
model.fit(X_vector, y)

# fungsi prediksi
def prediksi_karir(jawaban):

    jawaban_vector = vectorizer.transform([jawaban])

    hasil = model.predict(jawaban_vector)

    return hasil[0]

# fungsi ranking & persentase
def prediksi_detail(jawaban):

    jawaban_vector = vectorizer.transform([jawaban])

    probabilitas = model.predict_proba(jawaban_vector)

    kelas = model.classes_

    hasil = []

    for i in range(len(kelas)):

        hasil.append(
            (kelas[i], probabilitas[0][i])
        )

    hasil = sorted(
        hasil,
        key=lambda x: x[1],
        reverse=True
    )

    return hasil


# TEST AI

if __name__ == "__main__":

    contoh = "Saya suka coding website dan teknologi"

    hasil_prediksi = prediksi_karir(contoh)

    print("Hasil rekomendasi karir:")
    print(hasil_prediksi)