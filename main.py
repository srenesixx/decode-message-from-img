import cv2
import numpy as np

# ============================================================
# PEMUATAN CITRA
# ============================================================

# Membaca citra dalam mode grayscale
# Secara matematis, citra grayscale dapat direpresentasikan sebagai
# matriks I(x,y) dengan nilai intensitas 0–255
img = cv2.imread("ti_unusia.jpg", cv2.IMREAD_GRAYSCALE)

# Validasi keberadaan file
if img is None:
    raise FileNotFoundError("Citra tidak ditemukan")

# Mengubah tipe data uint8 → float32
# DCT melibatkan operasi cosinus dan perkalian bilangan real
# sehingga memerlukan presisi floating point
img = img.astype(np.float32)

# Mengambil dimensi citra
# h = jumlah baris (tinggi), w = jumlah kolom (lebar)
h, w = img.shape

# ============================================================
# INISIALISASI VARIABEL PESAN
# ============================================================

# Menyimpan pesan hasil ekstraksi karakter demi karakter
message = ""

# Menyimpan bit sementara (8 bit = 1 byte)
current_byte = ""

# ============================================================
# ITERASI BLOK 8x8
# ============================================================

# Citra dibagi menjadi blok 8×8 sesuai standar DCT (seperti JPEG)
# Setiap blok diasumsikan sebagai fungsi f(x,y) berukuran 8×8
for y in range(0, h - 7, 8):
    for x in range(0, w - 7, 8):

        # Mengambil satu blok 8×8 dari citra
        block = img[y:y+8, x:x+8]

        # ====================================================
        # DISCRETE COSINE TRANSFORM (DCT)
        # ====================================================

        # cv2.dct() mengimplementasikan rumus ini secara internal
        dct = cv2.dct(block)

        # ====================================================
        # PEMILIHAN KOEFISIEN DCT
        # ====================================================

        # Koefisien (4,4) berada pada frekuensi menengah
        # - DC (0,0): terlalu dominan secara visual
        # - Frekuensi tinggi: rentan noise
        #
        # Secara teori, frekuensi menengah adalah lokasi ideal
        # untuk steganografi DCT
        coef = dct[4, 4]

        # ====================================================
        # EKSTRAKSI BIT
        # ====================================================

        # Aturan ekstraksi (sesuai soal):
        # Jika F(u,v) > 0  → bit = 1
        # Jika F(u,v) ≤ 0  → bit = 0
        #
        # Secara matematis:
        # bit = sign(F(u,v))
        bit = '1' if coef > 0 else '0'

        # Menambahkan bit ke dalam buffer byte
        current_byte += bit

        # ====================================================
        # KONVERSI BINER → ASCII
        # ====================================================

        # 1 karakter ASCII direpresentasikan oleh 8 bit
        if len(current_byte) == 8:

            # Konversi:
            # biner → bilangan desimal → karakter ASCII
            #
            # Contoh:
            # "01001000" → 72 → 'H'
            char = chr(int(current_byte, 2))
            message += char

            # Reset buffer bit untuk karakter berikutnya
            current_byte = ""

            # ====================================================
            # DETEKSI DELIMITER
            # ====================================================

            # Pesan diakhiri dengan delimiter "###"
            # Ketika delimiter terdeteksi, proses dihentikan
            if message.endswith("###"):
                message = message[:-3]  # hapus delimiter
                print("Pesan Rahasia:")
                print(message)
                exit()

# Jika delimiter tidak ditemukan, tetap tampilkan hasil
print("Pesan Rahasia:")
print(message)
