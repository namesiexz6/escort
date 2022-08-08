from flask import Blueprint, render_template, request, session, escape

from flask_login import login_required

from aplikasi.model import permintaan

utama = Blueprint("utama", __name__, url_prefix="/utama")

# Endpoint untuk URL: / dengan HTTP GET
#
# Hanya tampilkan template utama.j2
@utama.route('/', methods=["GET"])
def halaman_utama_get():
    # Muat template
    return render_template("utama/utama.j2", nama="Rahmad Dawood", ulang=4)

# Endpoint untuk URL: / dengan HTTP POST
#
# Hanya tampilkan template utama.j2
@utama.route('/', methods=["POST"])
def halaman_utama_post():
    # Session jumlah_jalan untuk ingat form sudah berapa kali di submit
    if "jumlah_jalan" not in session:
        # Session belum ada, buat dan inisiasi dengan 1
        session["jumlah_jalan"] = 1
    else:
        # Sudah pernah dibuat sebelumnya, naikkan satu
        session["jumlah_jalan"] = session["jumlah_jalan"] + 1

    # Insialisasi isian form
    nama = None
    ulang = None

    # Ambil isian form untuk nama
    if "txt_nama" in request.form:
        nama = escape(request.form["txt_nama"].strip())
    # Ambil isian form untuk ulang
    if "txt_ulang" in request.form:
        ulang_str = escape(request.form["txt_ulang"].strip())
        if ulang_str == "":
            ulang = 0
        else:
            ulang = int(ulang_str)

    # Muat template
    return render_template("utama/utama.j2", nama=nama, ulang=ulang)


# Endpoint untuk URL: /lindungi
#
# Tampilkan halaman jika sudah login
@utama.route('/lindungi', methods=["GET"])
@login_required
def halaman_lindungi():
    # Tambahkan data ke datastore
    permintaan.tambah("Aa", 1)
    # Ambil daftar data yang telah disimpan
    daftar = permintaan.daftar()

    # Muat template
    return render_template("utama/lindungi.j2", daftar=daftar)
