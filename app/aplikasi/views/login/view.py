import json
import requests

from flask import Blueprint, render_template, request, session, escape, redirect, url_for

from flask_login import  login_user, logout_user, login_required, LoginManager

from oauthlib.oauth2 import WebApplicationClient

from aplikasi import app

from .user import User


# OAuth Client ke Google
oauth2_client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])

# Flask Login Manager
login_manager = LoginManager(app)

# Buat blueprint login
login = Blueprint("login", __name__)


# Lakukan proses login memakai Google
@login.route('/login', methods=["GET"])
def halaman_login():
    # Ambil URL untuk halaman login Google
    google_provider_cfg = requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Buat URI untuk memanggil halaman login Google, harus memakai OAuth 2.0
    request_uri = oauth2_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.url_root + "login_callback",
        scope=["openid", "email", "profile"],
    )

    # Alihkan ke halaman Login Google
    return redirect(request_uri)


# Callback yang dipanggil oleh Google jika login berhasil
@login.route('/login_callback', methods=["GET"])
def login_callback():
    # Code untuk meminta token, token dipakai untuk meminta informasi yang diperlukan
    code = request.args.get("code")

    # Ambil URL untuk meminta token
    google_provider_cfg = requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Buat URI untuk meminta token, harus memakai OAuth 2.0
    token_url, headers, body = oauth2_client.prepare_token_request(token_endpoint,
                                                                   authorization_response=request.url,
                                                                   redirect_url=request.base_url,
                                                                   code=code)
    # Panggil URL untuk meminta token
    token_response = requests.post(token_url,
                                   headers=headers,
                                   data=body,
                                   auth=(app.config["GOOGLE_CLIENT_ID"], app.config["GOOGLE_CLIENT_SECRET"]))    
    # Parse kembalian pemanggilan URL untuk meminta token
    oauth2_client.parse_request_body_response(json.dumps(token_response.json()))    

    # Ambil URL untuk meminta informasi user yang login
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    # Buat URI untuk meminta informasi user, memakai token yang kita dapat, harus memakai OAuth 2.0
    uri, headers, body = oauth2_client.add_token(userinfo_endpoint)
    # Panggil URL untuk meminta informasi user
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Amnil informasi yang kita minta
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        email = userinfo_response.json()["email"]
        url_gambar_profil = userinfo_response.json()["picture"]
        nama_lengkap = userinfo_response.json()["name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Buat object User yang akan disimpan di session sebagai pertanda sudah login
    user = User(unique_id=unique_id, nama_lengkap=nama_lengkap, email=email, url_gambar_profil=url_gambar_profil)
    session["user_google"] = json.dumps(user.__dict__)

    # Informasikan ke Flask-Login bawah sudah berhasil login
    login_user(user)

    # Pergi ke halaman jika login sukses
    return redirect(url_for("utama.halaman_lindungi"))


# Logout user dari aplikasi
@login.route('/logout', methods=["GET", "POST"])
def logout():
    # Hapus object user dari session
    session.pop("user_google")

    # Informasikan ke Flask-Login bawah sudah berhasil logout
    logout_user()

    # Pergi ke halaman jika logout sukses
    return redirect(url_for("utama.halaman_utama_get"))


# Dipakai oleh Flask-Login untuk memeriksa seorang user
#
# Parameter:
# * user_id : ID dari user yang hendak diperiksa
#
# Return: Object user yang diminta
@login_manager.user_loader
def load_user(user_id):
    # Kita tidak ada database, ambil dari session
    if "user_google" not in session:
        return None

    # Ambil object user dari session
    user_json = json.loads(session["user_google"])

    # Buat dan kembalikan object user 
    return User(unique_id=user_json["id"], 
                nama_lengkap=user_json["nama_lengkap"], 
                email=user_json["email"], 
                url_gambar_profil=user_json["url_gambar_profil"])

