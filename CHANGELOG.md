# Changelog

Semua perubahan penting pada project ini akan didokumentasikan di file ini.

---

## [2026-09-08]

### `multiFile.py`
- **Fix:** Hapus hardcoded credentials (`username`, `password`, `host`, `dbDefault`)
- **Fix:** Tambah `from dotenv import load_dotenv` dan `load_dotenv()` untuk membaca kredensial dari `.env`
- **Fix:** Tambah decorator `@st.cache_resource` pada fungsi `connectDatabase` untuk mencegah koneksi dibuat ulang setiap re-render
- **Fix:** Hapus kondisi `if 'newEngine' not in st.session_state` — engine sekarang selalu diperbarui saat tombol "Ganti Database" diklik

### `singleFile.py`
- **Fix:** Pindahkan logika `namaFile`, `namaTable`, `disableButton`, dan tombol Submit ke dalam blok `if uploaded_file is not None` untuk mencegah crash saat file belum diupload
- **Fix:** Tambah decorator `@st.cache_resource` pada fungsi `connectDatabase` untuk mencegah koneksi dibuat ulang setiap re-render
- **Fix:** Hapus kondisi `if 'newEngine' not in st.session_state` — engine sekarang selalu diperbarui saat tombol "Ganti Database" diklik
- **Fix:** Perbaiki typo komentar `# Upload FIle` → `# Upload File`

---

## [2026-09-08] — Tambah Fitur XLSX & SAV Transformer

### `xlsxFile.py` (baru)
- **Feat:** Transformer untuk file `.xlsx` — support single dan multiple file
- **Feat:** Pemilihan sheet per file sebelum preview dan submit
- **Feat:** Preview data sebelum diinputkan ke database
- **Feat:** Submit per file (sheet yang dipilih) atau submit semua file (sheet pertama tiap file)

### `savFile.py` (baru)
- **Feat:** Transformer untuk file `.SAV` (SPSS) — support single dan multiple file
- **Feat:** Preview data sebelum diinputkan ke database
- **Feat:** Tampilkan variable labels dari metadata SPSS via expander
- **Feat:** Submit per file atau submit semua file sekaligus

### `streamlit_app.py`
- **Refactor:** Rename group page `.DBF Converter` → `Transformer Tools`
- **Feat:** Tambah halaman `XLSX Converter` → `xlsxFile.py`
- **Feat:** Tambah halaman `SAV Converter` → `savFile.py`

---
