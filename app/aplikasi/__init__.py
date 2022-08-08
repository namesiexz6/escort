from flask import Flask
from flask_login import LoginManager
import requests

# Buat object Flask
app = Flask(__name__, template_folder="templates", instance_relative_config=True)

# Muat konfigurasi global
app.config.from_object('config')
# Muat konfigurasi instance
app.config.from_pyfile('config.py')

# Set server untuk development
app.config["ENV"] = "development"
# Hidupkan debugger di server
app.config["DEBUG"] = True

# Periksa apakah ada didefisinikan mode dimana kode dijalankan
if "MODE_LINGKUNGAN" in app.config:
    if app.config["MODE_LINGKUNGAN"] == "DEV":
        # Kode dijalankan dalam lingkungan pengembangan
        app.config["ENV"] = "development"
        app.config["DEBUG"] = True
    elif app.config["MODE_LINGKUNGAN"] == "PROD":
        # Kode dijalankan dalam lingkungan produksi
        app.config["ENV"] = "production"
        app.config["DEBUG"] = False
    elif app.config["MODE_LINGKUNGAN"] == "TEST":
        # Kode dijalankan dalam lingkungan pengembangan
        app.config["ENV"] = "development"
        app.config["DEBUG"] = True

# Jadikan template bisa auto reload
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Buat session
app.secret_key = app.config["SESSION_SECRET_KEY"]


#
# Daftarkan semua blueprint
#

# Blueprint untuk utama
from .views import utama
app.register_blueprint(utama)

# Blueprint untuk login
from .views import login
app.register_blueprint(login)
