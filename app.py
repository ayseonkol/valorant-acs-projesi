from flask import Flask, render_template, request
import pickle

# Flask uygulamasını (web sitemizi) başlatıyoruz
app = Flask(__name__)

# Eğittiğimiz modeli (beyni) içeri alıyoruz
with open('valorant_model.pkl', 'rb') as dosya:
    model = pickle.load(dosya)

# Sitenin ana sayfasına girildiğinde çalışacak kısım
@app.route('/')
def ana_sayfa():
    return render_template('index.html')

# Kullanıcı "Tahmin Et" butonuna bastığında çalışacak kısım
@app.route('/tahmin', methods=['POST'])
def tahmin_et():
    if request.method == 'POST':
        adr = float(request.form['adr'])
        kpr = float(request.form['kpr'])
        hs = float(request.form['hs'])
        kast = float(request.form['kast'])
        
        gelen_tahmin = model.predict([[adr, kpr, hs, kast]])
        sonuc = round(gelen_tahmin[0], 2)
        
        return render_template('index.html', tahmin_sonucu=f"Tahmini Combat Score (ACS): {sonuc}")

if __name__ == '__main__':
    app.run(debug=True)