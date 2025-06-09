## 🔐 Security Controls

1. **Secrets Management**
   - Menggunakan `.env` file untuk menyimpan `SECRET_KEY` agar tidak hardcoded.
   - Menggunakan `os.getenv()` di dalam `__init__.py` untuk membaca environment variable secara aman.

2. **Input Validation**
   - Validasi form register:
     - Username dan password tidak boleh kosong.
     - Password minimal 6 karakter.
     - Username tidak boleh duplikat.

3. **SAST (Static Application Security Testing)**
   - Menggunakan `Bandit` dalam pipeline CI/CD.
   - Pipeline akan gagal jika ditemukan vulnerability dengan level `HIGH`.

