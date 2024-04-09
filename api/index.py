from flask import Flask, render_template, redirect, request
from instaloader import instaloader

app = Flask(__name__)

@app.route("/")
def index():
    # Yönlendirmeyi geçici olarak devre dışı bırakmak için yorum satırı ekleyinn
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
            return render_template("profile.html", profile_data=data)
        except Exception as e:
            # Handle errors gracefully
            return render_template("profile.html", message=f"Hata: {str(e)}")
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
