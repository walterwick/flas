from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def fetch_div_content():
    # Hedef site URL'si
    url = "https://www.google.com/finance/quote/USD-TRY"
    
    # Siteye HTTP isteği gönderiyoruz
    response = requests.get(url)
    
    # Başarılı bir yanıt geldiyse içeriği işlemeye başlıyoruz
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Belirli bir sınıfa sahip div'i buluyoruz
        div_content = soup.find("div", class_="YMlKec fxKbKc")
        
        # İçerik varsa, içeriği alıyoruz, yoksa bir uyarı veriyoruz
        content = div_content.text if div_content else "Belirtilen sınıfa sahip div bulunamadı."
    else:
        content = "Siteye erişim sağlanamadı. HTTP Durum Kodu: " + str(response.status_code)
    
    # HTML içeriğini dinamik olarak gösteriyoruz
    html_content = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Div İçeriği Gösterici</title>
      </head>
      <body>
        <h1>Div İçeriği</h1>
        <p>{{ content }}</p>
      </body>
    </html>
    """
    
    # HTML içeriği ile birlikte Flask render işlemi
    return render_template_string(html_content, content=content)

if __name__ == "__main__":
    app.run(debug=True)
