from flask import Flask, render_template, redirect, request, jsonify
from io import BytesIO
import requests
from instaloader import Instaloader, Profile
import base64

app = Flask(__name__)

# Instaloader ile oturum açma
insta = Instaloader()

@app.route("/")
def index():
    # Yönlendirmeyi geçici olarak devre dışı bırakmak için yorum satırı ekleyin
    # return render_template("index.html")

    # Kullanıcıyı doğrudan profile yönlendir
    return redirect("/profile?username=emineey41")

@app.route("/profile")
def profile():
    username = request.args.get("username")

    if username:
        try:
            profile = Profile.from_username(insta.context, username)

            # Profile information dictionary
            data = {
                "username": profile.username,
                "post_count": profile.mediacount,
                "followers": profile.followers,
                "followees": profile.followees,
                "bio": profile.biography,
                "profile_pic_url": profile.profile_pic_url,
                "full_name": profile.full_name,  # Might not always be available
            }

            # Profil resmini Base64 formatına çevirerek HTML içinde görüntülemek için
            response = requests.get(data["profile_pic_url"])
            profile_pic_base64 = base64.b64encode(response.content).decode('utf-8')

            # HTML olarak parse ederek profil bilgilerini ve resmi göster
            html_content = f"""
            <p>{data['full_name']}</p>
            <p>Kullanıcı Adı: {data['username']}</p>
            <p>Gönderi Sayısı: {data['post_count']}</p>
            <p>Takipçiler: {data['followers']}</p>
            <p>Takip Edilenler: {data['followees']}</p>
            <p>Biyografi: {data['bio']}</p>
            <img src="data:image/jpeg;base64,{profile_pic_base64}" alt="Profil Resmi">
            """

            return html_content

        except Exception as e:
            # Handle errors gracefully
            return f"Hata: {str(e)}"
    else:
        return "Kullanıcı adı eksik."

if __name__ == "__main__":
    app.run(debug=True)
