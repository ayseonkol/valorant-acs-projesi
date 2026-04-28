import pandas as pd

# 1. Veriyi okuma
df = pd.read_csv(r'C:\Users\ayseo\OneDrive\Desktop\Valorant_Proje\players_stats\players_stats.csv')

# 2. Sadece modelde kullanacağımız sütunları seçme
secilen_sutunlar = [
    'Average Combat Score', 
    'Average Damage Per Round', 
    'Kills Per Round', 
    'Headshot %', 
    'Kill, Assist, Trade, Survive %'
]
veri = df[secilen_sutunlar].copy()

# 3. Yüzde (%) işaretlerini temizleyip veriyi ondalık sayıya (float) çevirme
veri['Headshot %'] = veri['Headshot %'].astype(str).str.replace('%', '').astype(float)
veri['Kill, Assist, Trade, Survive %'] = veri['Kill, Assist, Trade, Survive %'].astype(str).str.replace('%', '').astype(float)

# 4. İçinde boşluk (NaN) olan satırları silme (Modelin çökmemesi için kritik)
veri = veri.dropna()

print("--- Temizlenmiş ve Modele Hazır Veri ---")
print(veri.head())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# 1. Özellikler (X) ve Hedef (y) belirleme
X = veri[['Average Damage Per Round', 'Kills Per Round', 'Headshot %', 'Kill, Assist, Trade, Survive %']]
y = veri['Average Combat Score'] # Tahmin etmek istediğimiz değer

# 2. Veriyi Eğitim ve Test olarak ayırma
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Modeli Kurma ve Eğitme
model = LinearRegression()
model.fit(X_train, y_train)

# 4. Modelin Başarısını Test Etme
y_tahmin = model.predict(X_test)
basari_orani = r2_score(y_test, y_tahmin)

print("\n--- Model Sonuçları ---")
print(f"Model Başarı Oranı (R-Squared): {basari_orani:.2f}")

import pickle

# Eğittiğimiz modeli 'valorant_model.pkl' adıyla kaydediyoruz
with open('valorant_model.pkl', 'wb') as dosya:
    pickle.dump(model, dosya)

print("Model başarıyla web sitesi için kaydedildi!")