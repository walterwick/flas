from flask import Flask, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def fetch_div_content():
    # Hedef site URL'leri
    url1 = "https://www.google.com/finance/quote/USD-TRY"
    url2 = "https://www.google.com/finance/quote/EUR-TRY"  # İkinci hedef site
    url3 = "https://www.google.com/finance/quote/GBP-TRY"  # Üçüncü hedef site
    url4 = "https://www.google.com/finance/quote/BTC-TRY"  # Dördüncü hedef site

    # İlk siteye HTTP isteği gönderiyoruz
    response1 = requests.get(url1)
    if response1.status_code == 200:
        soup1 = BeautifulSoup(response1.text, "html.parser")
        div_content1 = soup1.find("div", class_="YMlKec fxKbKc")
        content1 = div_content1.text if div_content1 else "Belirtilen sınıfa sahip div bulunamadı."
    else:
        content1 = "Siteye erişim sağlanamadı. HTTP Durum Kodu: " + str(response1.status_code)
    
    # İkinci siteye HTTP isteği gönderiyoruz
    response2 = requests.get(url2)
    if response2.status_code == 200:
        soup2 = BeautifulSoup(response2.text, "html.parser")
        div_content2 = soup2.find("div", class_="YMlKec fxKbKc")  # Düzgün sınıf adı ile bulma
        content2 = div_content2.text if div_content2 else "İkinci sitede div bulunamadı."
    else:
        content2 = "İkinci siteye erişim sağlanamadı. HTTP Durum Kodu: " + str(response2.status_code)

    # Üçüncü siteye HTTP isteği gönderiyoruz
    response3 = requests.get(url3)
    if response3.status_code == 200:
        soup3 = BeautifulSoup(response3.text, "html.parser")
        div_content3 = soup3.find("div", class_="YMlKec fxKbKc")  # Düzgün sınıf adı ile bulma
        content3 = div_content3.text if div_content3 else "Üçüncü sitede div bulunamadı."
    else:
        content3 = "Üçüncü siteye erişim sağlanamadı. HTTP Durum Kodu: " + str(response3.status_code)

    # Dördüncü siteye HTTP isteği gönderiyoruz
    response4 = requests.get(url4)
    if response4.status_code == 200:
        soup4 = BeautifulSoup(response4.text, "html.parser")
        div_content4 = soup4.find("div", class_="YMlKec fxKbKc")  # Düzgün sınıf adı ile bulma
        content4 = div_content4.text if div_content4 else "Dördüncü sitede div bulunamadı."
    else:
        content4 = "Dördüncü siteye erişim sağlanamadı. HTTP Durum Kodu: " + str(response4.status_code)

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
        <h1>usd</h1>
        <p>{{ content1 }}</p>
        <h1>eur</h1>
        <p>{{ content2 }}</p>
        <h1>gbp</h1>
        <p>{{ content3 }}</p>
        <h1>btc</h1>
        <p>{{ content4 }}</p>
      </body>
    </html>
    """
    
    # HTML içeriği ile birlikte Flask render işlemi
    return render_template_string(html_content, content1=content1, content2=content2, content3=content3, content4=content4)

if __name__ == "__main__":
    app.run(debug=True)
