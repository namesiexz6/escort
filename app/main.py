from aplikasi import app

# Periksa apakah dipanggil dari command prompt (i.e. python main.py)
if __name__ == "__main__":
    # Benar dijalankan dari command prompt maka server belum  belum dijalankan.
    # Jalankan server
    app.run(host="127.0.0.1", port=8080, ssl_context="adhoc")
