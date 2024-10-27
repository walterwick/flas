from flask import Flask, request, redirect, render_template_string
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    # Redirect to the data route with the specified card number
    return redirect("/data?no=0430207A8E6C80")

@app.route("/data", methods=["GET"])
def get_card_data():
    # Get the card number from URL parameters
    card_number = request.args.get("no")
    
    # Return an error if the card number is missing
    if not card_number:
        return render_template_string(ERROR_HTML, message="Kart numarası belirtilmemiş"), 400

    # Set the API URL based on the card number
    url = f"https://pv2api3.teknarteknoloji.com/api/Assistant/getCardBalance/{card_number}"
    
    # Required headers
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
    'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoie1wiaWRcIjo5MixcInVzZXJOYW1lXCI6XCJ0dXJcIixcIm5hbWVcIjpcIlR1ciBVc2VyXCIsXCJhcHBSb2xlXCI6MSxcInBhZ2VSb2xlXCI6MCxcIm90aGVyUm9sZVwiOlwie1xcXCJhbGxDb21wYW5pZXNcXFwiOmZhbHNlLFxcXCJhbGxMaW5lc1xcXCI6ZmFsc2UsXFxcImFsbFBsYXRlc1xcXCI6ZmFsc2UsXFxcImNvbXBhbmllc1xcXCI6W10sXFxcImxpbmVzXFxcIjpbXSxcXFwicGxhdGVzXFxcIjpbXSxcXFwidXNlclJvbGVcXFwiOjAsXFxcImRldmlhdGlvblxcXCI6MH1cIn0iLCJuYmYiOjE3MzAwMzEwMTcsImV4cCI6MTczMDAzNjQxNywiaWF0IjoxNzMwMDMxMDE3fQ.eMOVH4S_Y7VSmTxWiu9WqbzXrZUv_nDBy5y7-H8uXS0',
        'content-type': 'application/json',
        'origin': 'https://ulasim.urfakart.com',
        'referer': 'https://ulasim.urfakart.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
    }
    
    # Send API request and get the response
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data', {})
        error_info = response.json().get('error', {})
        if error_info.get('code') == 0:
            # Return an HTML response with the data
            return render_template_string(CARD_DATA_HTML, data=data)
        else:
            # Return an error message if the API returned an error code
            return render_template_string(ERROR_HTML, message=error_info.get('message', 'Bilinmeyen hata')), 400
    else:
        # Return an error if the API request failed
        return render_template_string(ERROR_HTML, message=f"API Hatası: {response.status_code}"), response.status_code

# HTML templates as strings
CARD_DATA_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kart Bilgileri</title>
</head>
<body>
    <h1>Kart Bilgileri</h1>
    <ul>
        <li>İsim: {{ data.name or "Bilinmiyor" }}</li>
        <li>TC Kimlik No: {{ data.tc or "Bilinmiyor" }}</li>
        <li>Kart Tipi: {{ data.typeDescription or "Bilinmiyor" }}</li>
        <li>Geçerlilik Tarihi: {{ data.validity or "Bilinmiyor" }}</li>
        <li>Son İşlem Tarihi: {{ data.lastOperation or "Bilinmiyor" }}</li>
        <li>Kart Durumu: {{ data.status or "Bilinmiyor" }}</li>
        <li>Mifare ID: {{ data.mifareId or "Bilinmiyor" }}</li>
        <li>Bakiye: {{ data.balance or '0.00' }} TL</li>
        <li>Toplam Biniş: {{ data.totalBoarding or 0 }}</li>
        <li>Kalan Biniş: {{ data.remainingBoarding or 0 }}</li>
        <li>Yükleme Bekleniyor: {{ data.waitingUpload }}</li>
        <li>Son Yükleme: {{ data.lastUpload }}</li>
    </ul>
</body>
</html>
"""

ERROR_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hata</title>
</head>
<body>
    <h1>Hata</h1>
    <p>{{ message }}</p>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
