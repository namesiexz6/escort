from google.cloud import datastore

from .model import Permintaan, PERMINTAAN_KIND

# Tambah Permintaan
#
# Tambah obejct Permintaan ke datastore.
def tambah(nama, ulang):
    # Buat object hanya jika kedua data ada
    if nama != None and ulang != None:
        # Buat object baru
        permintaan_baru = Permintaan(nama=nama, ulang=ulang)

        # Sambung ke datastore
        client = datastore.Client()
        # Minta dibuatkan Key/Id baru untuk object baru
        key_baru = client.key(PERMINTAAN_KIND)
        # Minta dibuatkan entity di datastore memakai key baru
        entity_baru = datastore.Entity(key=key_baru)
        # Simpan object Permintaan ke entity baru
        entity_baru.update(permintaan_baru.ke_dictionary())
        # Simpan entity ke datastore
        client.put(entity_baru)

        # Kembalikan object Permintaan yang baru disimpan dengan id yang diberikan
        return Permintaan(id=entity_baru.id, 
                          nama=entity_baru["nama"],
                          ulang=entity_baru["ulang"])


# Ambil daftar Permintaan
#
# Ambil semua entity Permintaan yang ada di datastore.
def daftar():
    # Sambung ke datastore
    client = datastore.Client()

    # Buat query untuk meminta semua isi kind permintaan
    query = client.query(kind=PERMINTAAN_KIND)
    # Jalankan query
    hasil = query.fetch()

    # Ambil setiap entity yang dikembalikan query dan jadikan list dari 
    # object Permintaan.
    daftar_permintaan = []
    for satu_hasil in hasil:
        satu_permintaan = Permintaan(id=satu_hasil.id,
                                     nama=satu_hasil["nama"],
                                     ulang=satu_hasil["ulang"])
        daftar_permintaan.append(satu_permintaan)

    # Kembalikan list object permintaan
    return daftar_permintaan
