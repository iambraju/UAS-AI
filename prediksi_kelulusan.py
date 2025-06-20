import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("data_lulus_tepat_waktu.csv")

# Encode target
df['tepat'] = LabelEncoder().fit_transform(df['tepat'])  # 'Ya' = 1, 'Tidak' = 0
X = df[['ip1', 'ip2', 'ip3', 'ip4']]
y = df['tepat']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Fungsi prediksi
def prediksi(ip1, ip2, ip3, ip4):
    data_input = pd.DataFrame([[ip1, ip2, ip3, ip4]], columns=['ip1', 'ip2', 'ip3', 'ip4'])
    proba = model.predict_proba(data_input)[0]
    pred = np.argmax(proba)
    hasil = "Lulus Tepat Waktu" if pred == 1 else "Tidak Lulus Tepat Waktu"
    persen = round(proba[1] * 100, 2)

    # Visualisasi probabilitas
    plt.figure(figsize=(5, 3))
    plt.bar(['Tidak Lulus', 'Lulus'], proba, color=['salmon', 'skyblue'])
    plt.title(f"Probabilitas Prediksi\nKemungkinan Lulus: {persen}%")
    plt.ylabel("Probabilitas")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

    # Visualisasi feature importance
    importances = model.feature_importances_
    fitur = X.columns
    df_imp = pd.DataFrame({'Fitur': fitur, 'Importance': importances}).sort_values(by='Importance', ascending=False)

    print(f"\nHasil Prediksi: {hasil}")
    print(f"Probabilitas Lulus: {persen}%")
    print("\nPengaruh Setiap Fitur terhadap Prediksi:")
    print(df_imp.to_string(index=False))

    # Grafik pengaruh fitur
    plt.figure(figsize=(5, 3))
    sns.barplot(x='Importance', y='Fitur', data=df_imp, palette='viridis')
    plt.title("Fitur yang Mempengaruhi Prediksi")
    plt.tight_layout()
    plt.show()

    # Pause sebelum kembali ke menu
    input("\nTekan Enter untuk kembali ke menu...")

# CLI Interaktif
while True:
    print("\n=== PREDIKSI KELULUSAN MAHASISWA ===")
    print("1. Input nilai IP manual")
    print("2. Gunakan data dari nomor baris")
    print("0. Keluar")
    pilihan = input("Pilih opsi (0/1/2): ")

    if pilihan == '1':
        try:
            ip1 = float(input("IP Semester 1: "))
            ip2 = float(input("IP Semester 2: "))
            ip3 = float(input("IP Semester 3: "))
            ip4 = float(input("IP Semester 4: "))
            prediksi(ip1, ip2, ip3, ip4)
        except:
            print("Input tidak valid. Harap masukkan angka desimal.")
    elif pilihan == '2':
        try:
            idx = int(input(f"Masukkan nomor baris (0 - {len(df)-1}): "))
            if 0 <= idx < len(df):
                baris = df.iloc[idx]
                print(f"\nData IP yang dipilih: {baris[['ip1','ip2','ip3','ip4']].to_dict()}")
                prediksi(baris['ip1'], baris['ip2'], baris['ip3'], baris['ip4'])
            else:
                print("Nomor baris tidak tersedia.")
        except:
            print("Masukkan angka yang valid.")
    elif pilihan == '0':
        print("Sampai jumpa!")
        break
    else:
        print("Pilihan tidak valid.")
