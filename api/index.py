from flask import Flask, render_template, redirect, request, send_file, jsonify
from io import BytesIO
import requests
from instaloader import instaloader

app = Flask(__name__)

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
            insta = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(insta.context, username)

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

            return jsonify(data)

        except Exception as e:
            # Handle errors gracefully
            return jsonify({"error": f"Hata: {str(e)}"})
    else:
        return jsonify({"error": "Kullanıcı adı eksik."})

@app.route("/profile_pic")
def profile_pic():
    profile_pic_url = request.args.get("profile_pic_url")

    if profile_pic_url:
        response = requests.get(profile_pic_url)
        return send_file(BytesIO(response.content), mimetype=response.headers['Content-Type'])
    else:
        return "Profil resmi URL'si eksik."

if __name__ == "__main__":
    app.run(debug=True)
