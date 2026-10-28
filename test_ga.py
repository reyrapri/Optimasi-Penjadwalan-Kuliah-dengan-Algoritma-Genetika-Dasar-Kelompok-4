"""Unit test sederhana untuk fungsi fitness dan operator. Jalankan: python -m unittest -v"""
import unittest
import numpy as np
import data
from ga import (Masalah, Parameter, jalankan_ga, crossover_satu_titik,
                crossover_uniform, mutasi_acak, seleksi_roulette, seleksi_turnamen)


def kromosom_tanpa_bentrok(m):
    """Setiap sesi di slot berbeda, ruang 0 -> tidak ada bentrok apa pun."""
    return np.arange(m.N) * m.R


class TestFitness(unittest.TestCase):
    def setUp(self):
        self.m = Masalah(data)

    def test_jadwal_bersih_fitness_satu(self):
        k = kromosom_tanpa_bentrok(self.m)
        self.assertEqual(self.m.pelanggaran_keras(k), 0)
        self.assertEqual(self.m.fitness(k), 1.0)

    def test_dosen_bentrok(self):
        # PCD dan JST sama-sama diajar Nahumi -> taruh di slot sama, ruang beda
        kode = [s["kode"] for s in self.m.sesi]
        i, j = kode.index("PCD"), kode.index("JST")
        k = kromosom_tanpa_bentrok(self.m)
        k[i] = 0 * self.m.R + 0
        k[j] = 0 * self.m.R + 1
        self.assertGreaterEqual(self.m.rincian_pelanggaran(k)["dosen"], 1)

    def test_ruang_bentrok(self):
        k = kromosom_tanpa_bentrok(self.m)
        k[1] = k[0]                                  # slot dan ruang identik
        self.assertGreaterEqual(self.m.rincian_pelanggaran(k)["ruang"], 1)

    def test_kelas_bentrok(self):
        k = kromosom_tanpa_bentrok(self.m)
        k[1] = k[0] // self.m.R * self.m.R + 1       # slot sama, ruang beda
        self.assertGreaterEqual(self.m.rincian_pelanggaran(k)["kelas"], 1)

    def test_kapasitas(self):
        self.m.mhs = self.m.mhs * 0 + 1000           # kelas lebih besar dari semua ruang
        k = kromosom_tanpa_bentrok(self.m)
        self.assertEqual(self.m.rincian_pelanggaran(k)["kapasitas"], self.m.N)

    def test_fitness_rentang(self):
        rng = np.random.default_rng(0)
        k = rng.integers(0, self.m.n_gen_nilai, self.m.N)
        self.assertTrue(0 < self.m.fitness(k) <= 1)

    def test_ga_menemukan_jadwal_valid(self):
        h = jalankan_ga(self.m, Parameter(generasi=100), seed=1)
        self.assertEqual(h.fitness_terbaik, 1.0)
        self.assertEqual(self.m.pelanggaran_keras(h.terbaik), 0)


class TestOperator(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(1)

    def test_crossover_panjang_dan_asal_gen(self):
        a, b = np.zeros(20, int), np.ones(20, int)
        for f in (crossover_satu_titik, crossover_uniform):
            c1, c2 = f(self.rng, a, b)
            self.assertEqual(len(c1), 20)
            self.assertTrue(set(c1) <= {0, 1})
            self.assertEqual(int(c1.sum() + c2.sum()), 20)   # gen hanya dipertukarkan

    def test_mutasi_rentang(self):
        k = mutasi_acak(self.rng, np.zeros(50, int), 1.0, 125)
        self.assertTrue(((k >= 0) & (k < 125)).all())

    def test_seleksi_ukuran(self):
        pop = self.rng.integers(0, 10, (30, 5)); fit = self.rng.random(30) + 0.01
        self.assertEqual(seleksi_roulette(self.rng, pop, fit, 12).shape, (12, 5))
        self.assertEqual(seleksi_turnamen(self.rng, pop, fit, 12).shape, (12, 5))


if __name__ == "__main__":
    unittest.main()
