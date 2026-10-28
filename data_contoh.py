"""DATA CONTOH (dummy) skala UTS: 20 mata kuliah, 8 dosen, 5 ruang, 5 hari x 5 slot.
Dipakai untuk uji skala dengan: python main.py --data contoh

Skala UTS: 20 mata kuliah, 8 dosen, 5 ruang, 5 hari x 5 slot waktu.
Satu mata kuliah dapat memiliki 1 atau 2 sesi per minggu; setiap sesi
menjadi satu gen pada kromosom.
"""

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
SLOT = ["07:30-09:10", "09:20-11:00", "11:10-12:50", "13:30-15:10", "15:20-17:00"]

# (nama ruang, kapasitas)
RUANG = [
    ("R-101", 40),
    ("R-102", 35),
    ("R-103", 30),
    ("Lab-A", 25),
    ("Lab-B", 25),
]

DOSEN = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]

# Kendala lunak: hari yang dihindari dosen (indeks hari, 0 = Senin)
PREFERENSI_DOSEN_HINDARI_HARI = {
    "D1": {4},        # tidak mau Jumat
    "D2": {0},        # tidak mau Senin
    "D3": {2},
    "D5": {4},
    "D6": {0, 1},
    "D8": {3},
}

# (kode, nama, dosen, kelas, jumlah sesi, jumlah mahasiswa)
MATA_KULIAH = [
    ("TI101", "Algoritma dan Pemrograman", ["D1"], "TI-1A", 2, 30),
    ("TI102", "Kalkulus",                  ["D2"], "TI-1A", 1, 30),
    ("TI103", "Pengantar Teknologi Informasi", ["D3"], "TI-1A", 1, 30),
    ("TI104", "Bahasa Inggris",            ["D4"], "TI-1A", 1, 30),
    ("TI105", "Matematika Diskrit",        ["D2"], "TI-1A", 2, 30),

    ("TI301", "Struktur Data",             ["D1"], "TI-3A", 2, 28),
    ("TI302", "Basis Data",                ["D5"], "TI-3A", 2, 28),
    ("TI303", "Jaringan Komputer",         ["D6"], "TI-3A", 1, 28),
    ("TI304", "Organisasi dan Arsitektur Komputer", ["D7"], "TI-3A", 1, 28),
    ("TI305", "Statistika",                ["D2"], "TI-3A", 1, 28),

    ("TI501", "Kecerdasan Buatan",         ["D3"], "TI-5A", 2, 25),
    ("TI502", "Rekayasa Perangkat Lunak",  ["D8"], "TI-5A", 1, 25),
    ("TI503", "Pemrograman Web",           ["D5"], "TI-5A", 2, 25),
    ("TI504", "Sistem Operasi",            ["D6"], "TI-5A", 1, 25),
    ("TI505", "Keamanan Informasi",        ["D7"], "TI-5A", 1, 25),

    ("TI701", "Data Mining",               ["D4"], "TI-7A", 2, 22),
    ("TI702", "Komputasi Paralel",         ["D8"], "TI-7A", 1, 22),
    ("TI703", "Etika Profesi",             ["D3"], "TI-7A", 1, 22),
    ("TI704", "Metodologi Penelitian",     ["D4"], "TI-7A", 1, 22),
    ("TI705", "Sistem Terdistribusi",      ["D7"], "TI-7A", 1, 22),
]


def bangun_sesi():
    """Mengembang mata kuliah menjadi daftar sesi (1 sesi = 1 gen)."""
    sesi = []
    for kode, nama, dosen, kelas, n_sesi, mhs in MATA_KULIAH:
        for k in range(n_sesi):
            sesi.append({
                "kode": kode, "nama": nama, "dosen": list(dosen),
                "kelas": kelas, "sesi_ke": k + 1, "mhs": mhs,
            })
    return sesi
