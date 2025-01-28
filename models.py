from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    nominal = db.Column(db.Numeric(10, 2), nullable=False)
    catatan = db.Column(db.Text, nullable=True)
    prioritas = db.Column(db.String(10), nullable=False)
    dompet = db.Column(db.String(10), nullable=False)

    CATEGORY_CHOICES = [
        "Makanan/Minuman",
        "Komunikasi",
        "Transportasi",
        "Pendidikan/Ilmu",
        "Hiburan",
        "Kesehatan",
        "Kebersihan",
        "Belanja",
        "Darurat",
        "Tempat tinggal",
        "Produktivitas",
        "Lainnya",
    ]

    PRIORITY_CHOICES = ["Butuh", "Harus", "Ingin"]

    WALLET_CHOICES = [
        "Cash",
        "OVO",
        "BJB",
        "Livin",
        "ShopeePay",
        "Lainnya",
    ]

    def __repr__(self):
        return f"<Expense {self.tanggal} - {self.kategori} - Rp {self.nominal}>"
