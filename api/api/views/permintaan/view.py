from flask import Blueprint, jsonify

from api.model import permintaan

permintaan = Blueprint("permintaan", __name__, url_prefix="/api")

@permintaan.route('/daftar', methods=["GET"])
def daftar():
    daftar = permintaan.daftar()

    # Muat template
    return jsonify(daftar), 200


@permintaan.rout("/tambah_data", methods=["POST"])
def tambah():
    # Pastikan parameter dalam JSON
    if request.is_json:
        # Ambil parameter
        permintaan_baru = request.get_json()
    else:
        return "Parameter salah", 415

    # Periksa parameter sudah benar
    if permintaan_baru is None:
        return "Parameter salah", 400
    if "nama" not in permintaan_baru.keys():
        return "Parameter salah", 400
    if "ulang" not in permintaan_baru.keys():
        return "Parameter salah", 400

    nama = escape(permintaan_baru["nama_lengkap"].strip())
    ulang = permintaan_baru["ulang"]

    # Tambah permintaan baru
    hasil = permintaan.tambah(nama, ulang)

    # Pastikan berhasil
    if (hasil is None):
        return "Gagal menambah data!", 500

    return "Berhasi", 200
