import sqlite3

# Nama file database
old_db = "db.sqlite3"  # Database Django
new_db = "expenses_track.db"  # Database Flask

# Koneksi ke database lama (Django)
conn_old = sqlite3.connect(old_db)
cursor_old = conn_old.cursor()

# Koneksi ke database baru (Flask)
conn_new = sqlite3.connect(new_db)
cursor_new = conn_new.cursor()

# Buat tabel di database baru sesuai dengan model Flask
cursor_new.execute("""
CREATE TABLE IF NOT EXISTS expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal DATE NOT NULL,
    kategori TEXT NOT NULL,
    nominal NUMERIC(10, 2) NOT NULL,
    catatan TEXT,
    prioritas TEXT NOT NULL,
    dompet TEXT NOT NULL
);
""")

# Menampilkan semua tabel yang ada di database lama untuk debugging
cursor_old.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor_old.fetchall()

print("Tabel-tabel yang ada di database lama:")
for table in tables:
    print(table)

# Coba untuk mengambil data dari tabel yang benar (sesuaikan dengan nama tabel Django Anda)
# Misalnya, jika tabelnya bernama 'expense_expense', sesuaikan nama tabelnya di sini.
# Periksa nama tabel yang benar di hasil print sebelumnya
cursor_old.execute("SELECT tanggal, kategori, nominal, catatan, prioritas, dompet FROM expense_expense")
expenses = cursor_old.fetchall()

# Masukkan data ke database baru
cursor_new.executemany("""
INSERT INTO expense (tanggal, kategori, nominal, catatan, prioritas, dompet)
VALUES (?, ?, ?, ?, ?, ?);
""", expenses)

# Commit perubahan dan tutup koneksi
conn_new.commit()
conn_old.close()
conn_new.close()

print("Data berhasil dikonversi ke expenses.db")
