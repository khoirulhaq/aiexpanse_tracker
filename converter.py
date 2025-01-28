import sqlite3

# Nama file database
old_db = "db.sqlite3"  # Database Django
new_db = "expenses.db"  # Database Flask

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

# Ambil data dari tabel Expense di database lama
cursor_old.execute("SELECT id, tanggal, kategori, nominal, catatan, prioritas, dompet FROM expense_expense")  # Nama tabel Django
expenses = cursor_old.fetchall()

# Masukkan data ke database baru
cursor_new.executemany("""
INSERT INTO expense (id, tanggal, kategori, nominal, catatan, prioritas, dompet)
VALUES (?, ?, ?, ?, ?, ?, ?);
""", expenses)

# Commit perubahan dan tutup koneksi
conn_new.commit()
conn_old.close()
conn_new.close()

print("Data berhasil dikonversi ke expenses.db")
