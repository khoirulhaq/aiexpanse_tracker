from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Expense
from datetime import datetime, timedelta
from sqlalchemy import extract, func
import pandas as pd
from calendar import monthrange
from sqlalchemy.exc import SQLAlchemyError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses_track.db'  # Gunakan SQLite sebagai database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'exptrackerai'  # Ganti dengan string yang lebih aman
db.init_app(app)


# ====== ANALYTICS =======
@app.route("/analytics")
def analytics():
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    description = request.args.get("description", "")
    page = request.args.get("page", 1, type=int)
    
    # Menentukan query dengan filter
    query = Expense.query
    if start_date:
        query = query.filter(Expense.tanggal >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(Expense.tanggal <= datetime.strptime(end_date, "%Y-%m-%d"))
    if description:
        query = query.filter(Expense.catatan.like(f"%{description}%"))

    # Menambahkan pengurutan berdasarkan tanggal secara descending
    query = query.order_by(Expense.tanggal.desc())

    # Pagination
    expenses = query.paginate(page=page, per_page=5, error_out=False)  # 10 item per halaman
    total_pages = expenses.pages

    return render_template(
        "analytics.html", 
        expenses=expenses.items, 
        page=page, 
        total_pages=total_pages, 
        start_date=start_date, 
        end_date=end_date, 
        description=description
    )
# API untuk Line Chart (Last 12-Months Expenses)
@app.route('/api/analytics-line-chart-data', methods=['GET'])
def get_line_chart_data():
    try:
        # Ambil parameter filter dari query string
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        description = request.args.get("description")

        # Default ke 1 tahun terakhir jika start_date atau end_date kosong
        today = datetime.today()
        if not start_date:
            start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")  # 1 tahun sebelum hari ini
        if not end_date:
            end_date = today.strftime("%Y-%m-%d")  # Hari ini

        # Query untuk mengambil total pengeluaran per bulan
        query = db.session.query(
            extract('year', Expense.tanggal).label('year'),
            extract('month', Expense.tanggal).label('month'),
            func.sum(Expense.nominal).label('total')
        )

        # Filter berdasarkan tanggal
        query = query.filter(Expense.tanggal >= datetime.strptime(start_date, "%Y-%m-%d"))
        query = query.filter(Expense.tanggal <= datetime.strptime(end_date, "%Y-%m-%d"))

        # Filter berdasarkan deskripsi (jika ada)
        if description:
            query = query.filter(Expense.catatan.like(f"%{description}%"))

        monthly_data = (
            query.group_by(extract('year', Expense.tanggal), extract('month', Expense.tanggal))
            .order_by(extract('year', Expense.tanggal), extract('month', Expense.tanggal))
            .all()
        )

        # Proses data untuk format JSON
        labels = [f"{int(entry.year)}-{int(entry.month):02d}" for entry in monthly_data]  # Format YYYY-MM
        values = [float(entry.total) for entry in monthly_data]  # Nilai nominal

        return jsonify({
            "labels": labels,
            "values": values
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API untuk Doughnut Chart (Dompet)
@app.route('/api/analytics-doughnut-chart-data', methods=['GET'])
def get_doughnut_chart_data():
    try:
        # Ambil parameter filter dari query string
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        description = request.args.get("description")

        # Default ke 1 tahun terakhir jika start_date atau end_date kosong
        today = datetime.today()
        if not start_date:
            start_date = (today - timedelta(days=365)).strftime("%Y-%m-%d")  # 1 tahun sebelum hari ini
        if not end_date:
            end_date = today.strftime("%Y-%m-%d")  # Hari ini

        # Query untuk mengambil total pengeluaran per dompet
        query = db.session.query(
            Expense.dompet,
            func.sum(Expense.nominal).label('total')
        )

        # Filter berdasarkan tanggal
        query = query.filter(Expense.tanggal >= datetime.strptime(start_date, "%Y-%m-%d"))
        query = query.filter(Expense.tanggal <= datetime.strptime(end_date, "%Y-%m-%d"))

        # Filter berdasarkan deskripsi (jika ada)
        if description:
            query = query.filter(Expense.catatan.like(f"%{description}%"))

        wallet_data = (
            query.group_by(Expense.dompet)
            .order_by(func.sum(Expense.nominal).desc())
            .all()
        )

        # Proses data untuk format JSON
        labels = [entry.dompet for entry in wallet_data]  # Nama dompet
        values = [float(entry.total) for entry in wallet_data]  # Nilai nominal

        return jsonify({
            "labels": labels,
            "values": values
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====== DATA =======

@app.route("/data", methods=["GET", "POST"])
def data():
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")
    description = request.args.get("description", "")
    page = request.args.get("page", 1, type=int)
    
    # Menentukan query dengan filter
    query = Expense.query
    if start_date:
        query = query.filter(Expense.tanggal >= datetime.strptime(start_date, "%Y-%m-%d"))
    if end_date:
        query = query.filter(Expense.tanggal <= datetime.strptime(end_date, "%Y-%m-%d"))
    if description:
        query = query.filter(Expense.catatan.like(f"%{description}%"))

    # Menambahkan pengurutan berdasarkan tanggal secara descending
    query = query.order_by(Expense.tanggal.desc())

    # Pagination
    expenses = query.paginate(page=page, per_page=10, error_out=False)  # 10 item per halaman
    total_pages = expenses.pages

    return render_template(
        "data.html", 
        expenses=expenses.items, 
        page=page, 
        total_pages=total_pages, 
        start_date=start_date, 
        end_date=end_date, 
        description=description
    )


@app.route("/edit/<int:expense_id>", methods=["GET", "POST"])
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    
    if request.method == "POST":
        expense.catatan = request.form['description']
        expense.nominal = float(request.form['amount'])  # Pastikan amount adalah float
        # Konversi string date ke objek datetime.date
        expense.tanggal = datetime.strptime(request.form['date'], "%Y-%m-%d").date()
        expense.kategori = request.form['category']  # Update kategori
        expense.prioritas = request.form['priority']  # Update prioritas
        expense.dompet = request.form['wallet']  # Update dompet

        db.session.commit()

        flash('Expense updated successfully', 'success')  # Menambahkan pesan flash
        return redirect(url_for('data'))
    
    return render_template('edit_expense.html', expense=expense)


# Route untuk menghapus data expense
@app.route("/delete/<int:expense_id>")
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()

    flash('Expense deleted successfully', 'success')  # Menambahkan pesan flash
    return redirect(url_for('data'))


@app.route("/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        description = request.form['description']
        amount = float(request.form['amount'])  # Pastikan amount adalah float
        date = datetime.strptime(request.form['date'], "%Y-%m-%d").date()  # Konversi ke objek date
        category = request.form['category']  # Mengambil nilai kategori dari form
        priority = request.form['priority']  # Mengambil nilai prioritas dari form
        wallet = request.form['wallet']  # Mengambil nilai dompet dari form

        # Membuat objek expense baru
        new_expense = Expense(
            tanggal=date,
            kategori=category,
            nominal=amount,
            catatan=description,
            prioritas=priority,
            dompet=wallet
        )
        
        # Menyimpan ke database
        db.session.add(new_expense)
        db.session.commit()

        flash('Expense added successfully', 'success')  # Menambahkan pesan flash
        return redirect(url_for('data'))
    
    # Mengirimkan pilihan ke template untuk dropdown
    category_choices = [
        "Makanan/Minuman", "Komunikasi", "Transportasi", "Pendidikan/Ilmu",
        "Hiburan", "Kesehatan", "Kebersihan", "Belanja", "Darurat",
        "Tempat tinggal", "Produktivitas", "Lainnya"
    ]
    priority_choices = ["Butuh", "Harus", "Ingin"]
    wallet_choices = ["Cash", "OVO", "BJB", "Livin", "ShopeePay", "Lainnya"]
    
    return render_template(
        'add_expense.html',
        category_choices=category_choices,
        priority_choices=priority_choices,
        wallet_choices=wallet_choices
    )


# ====== HOME =======

def format_currency(value):
    # Format angka menjadi format keuangan Indonesia
    return f"{value:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

@app.route("/",methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    try:
        # Ambil data dari database
        expenses_query = db.session.query(Expense.nominal, Expense.tanggal).all()
        
        # Ubah data menjadi pandas DataFrame
        df = pd.DataFrame(expenses_query, columns=["nominal", "tanggal"])
        
        # Pastikan kolom tanggal hanya berisi tanggal (tanpa jam)
        df['tanggal'] = pd.to_datetime(df['tanggal']).dt.date

        # Mendapatkan tanggal hari ini
        today = datetime.today().date()

        # Bulan ini
        start_of_this_month = today.replace(day=1)
        filtered_this_month = df[df['tanggal'] >= start_of_this_month]

        # Bulan kemarin
        start_of_last_month = (start_of_this_month - timedelta(days=1)).replace(day=1)
        end_of_last_month = start_of_this_month - timedelta(days=1)
        filtered_last_month = df[(df['tanggal'] >= start_of_last_month) & (df['tanggal'] <= end_of_last_month)]

        # Group by tanggal untuk bulan ini
        grouped_this_month = (
            filtered_this_month.groupby('tanggal')['nominal']
            .sum()
            .reset_index()
        )

        avg_daily = (grouped_this_month['nominal'].sum()) / ((today - grouped_this_month['tanggal'].min()).days + 1)
        avg_daily_rounded = round(avg_daily, 2)

        # Hitung total nominal untuk bulan ini
        total_this_month = filtered_this_month['nominal'].sum()

        # Hitung total nominal untuk bulan sebelumnya
        total_last_month = filtered_last_month['nominal'].sum()

        # Hitung perubahan persentase dari bulan sebelumnya ke bulan ini
        change_in_month = ((total_this_month - total_last_month) / total_last_month) * 100 if total_last_month != 0 else float('inf')
        change_in_month = round(change_in_month, 2)

        # Tanggal awal minggu ini dan minggu sebelumnya
        start_of_this_week = today - timedelta(days=today.weekday())  # Senin minggu ini
        end_of_this_week = start_of_this_week + timedelta(days=6)    # Minggu minggu ini
        start_of_last_week = start_of_this_week - timedelta(days=7)  # Senin minggu sebelumnya
        end_of_last_week = start_of_this_week - timedelta(days=1)    # Minggu minggu sebelumnya

        # Filter data untuk minggu ini dan minggu sebelumnya
        filtered_this_week = df[(df['tanggal'] >= start_of_this_week) & (df['tanggal'] <= end_of_this_week)]
        filtered_last_week = df[(df['tanggal'] >= start_of_last_week) & (df['tanggal'] <= end_of_last_week)]

        # Hitung total nominal untuk minggu ini dan minggu sebelumnya
        total_this_week = filtered_this_week['nominal'].sum()
        total_last_week = filtered_last_week['nominal'].sum()

        # Hitung perubahan persentase dari minggu sebelumnya ke minggu ini
        change_in_week = ((total_this_week - total_last_week) / total_last_week) * 100 if total_last_week != 0 else float('inf')
        change_in_week = round(change_in_week, 2)

        # Pengeluaran hari ini
        today_expenses = df[df['tanggal'] == today]['nominal'].sum()

        # Grouping berdasarkan bulan (tanpa jam)
        df['year_month'] = pd.to_datetime(df['tanggal']).dt.to_period('M')

        # Group by per bulan dengan agregasi sum
        monthly_data = df.groupby('year_month')['nominal'].sum().reset_index()

        # Konversi kembali 'year_month' menjadi datetime untuk perhitungan waktu
        monthly_data['year_month'] = monthly_data['year_month'].dt.to_timestamp().dt.date

        # Filter data 12 bulan terakhir
        last_12_months = monthly_data[monthly_data['year_month'] >= (max(monthly_data['year_month']) - timedelta(days=365))]

        # Hitung rata-rata dan median dari total nominal per bulan
        average_12_months = last_12_months['nominal'].mean()
        median_12_months = last_12_months['nominal'].median()
        total_12_months = last_12_months['nominal'].sum()

        # Data untuk dikembalikan ke frontend
        expenses = {
            "month": total_this_month,
            "today": today_expenses,
            "this_week": total_this_week,
            "change_in_week": change_in_week,
            "change_in_month": change_in_month,
            "avg_daily_month": avg_daily_rounded,
            "average_12_months": average_12_months,
            "median_12_months": median_12_months,
            "total_12_months": total_12_months
        }

        # Format setiap nilai menggunakan fungsi format_currency dan format persen
        formatted_expenses = {
            "month": format_currency(expenses["month"]),
            "today": format_currency(expenses["today"]),
            "this_week": format_currency(expenses["this_week"]),
            "change_in_week": f"{expenses['change_in_week']}%",
            "change_in_month": f"{expenses['change_in_month']}%",
            "avg_daily_month": format_currency(expenses["avg_daily_month"]),
            "average_12_months": format_currency(expenses["average_12_months"]),
            "median_12_months": format_currency(expenses["median_12_months"]),
            "total_12_months": format_currency(expenses["total_12_months"])
        }

        return jsonify(formatted_expenses)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route('/api/sales-data', methods=['GET'])
def get_sales_data():
    # Hitung 12 bulan terakhir
    today = datetime.today()
    twelve_months_ago = today - timedelta(days=365)

    # Query untuk menghitung total pengeluaran per bulan
    monthly_expenses = (
        db.session.query(
            extract('year', Expense.tanggal).label('year'),     # Ambil tahun
            extract('month', Expense.tanggal).label('month'),  # Ambil bulan
            func.sum(Expense.nominal).label('total')           # Totalkan nominal
        )
        .filter(Expense.tanggal >= twelve_months_ago)          # Filter 12 bulan terakhir
        .group_by(extract('year', Expense.tanggal), extract('month', Expense.tanggal))  # Grup berdasarkan bulan dan tahun
        .order_by(extract('year', Expense.tanggal), extract('month', Expense.tanggal))  # Urutkan bulan
        .all()
    )

    # Siapkan data untuk API
    categories = []  # Menyimpan nama bulan + tahun
    sales = []       # Menyimpan total nominal

    for entry in monthly_expenses:
        year = int(entry.year)   # Tahun
        month = int(entry.month) # Bulan dalam bentuk angka
        total = entry.total      # Total pengeluaran bulan tersebut

        # Format nama bulan dengan tahun, misal: "Jan 24"
        formatted_date = datetime(year, month, 1).strftime('%b %y')
        categories.append(formatted_date)
        sales.append(total)

    return jsonify({
        "categories": categories,
        "sales": sales
    })


@app.route('/api/revenue-data', methods=['GET'])
def get_revenue_data():
    try:
        # Ambil parameter opsional
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")

        # Validasi tanggal
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d") if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d") if end_date_str else None
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

        # Default ke bulan ini jika tidak ada parameter
        today = datetime.today()
        first_day_of_month = datetime(today.year, today.month, 1)
        _, last_day = monthrange(today.year, today.month)
        last_day_of_month = datetime(today.year, today.month, last_day)

        # Mundurkan start_date sehari untuk memastikan mencakup seluruh data di tanggal 1
        start_date = start_date or (first_day_of_month - timedelta(days=1))
        end_date = end_date or (last_day_of_month + timedelta(days=1))

        print(f"Start Date: {start_date}, End Date: {end_date}")

        # Query untuk mengambil semua data expense dalam rentang tanggal
        query_result = (
            db.session.query(Expense.dompet, Expense.nominal)
            .filter(Expense.tanggal >= start_date, Expense.tanggal < end_date)
            .all()
        )
        print(f"Query Result: {query_result}")

        # Debugging: Cetak query SQL
        print(str(db.session.query(Expense.dompet, Expense.nominal)
                  .filter(Expense.tanggal >= start_date, Expense.tanggal < end_date).statement.compile(dialect=db.engine.dialect)))

        # Konversi hasil query ke Pandas DataFrame
        data = [{"dompet": row.dompet, "nominal": float(row.nominal)} for row in query_result]
        df = pd.DataFrame(data)

        # Jika tidak ada data, kembalikan list kosong
        if df.empty:
            return jsonify({"revenue": []})

        # Menghitung total nominal untuk setiap dompet
        wallet_totals = df.groupby('dompet', as_index=False)['nominal'].sum()

        # Konversi hasil ke format JSON
        revenue_data = [
            {"value": row['nominal'], "name": row['dompet']}
            for _, row in wallet_totals.iterrows()
        ]

        return jsonify({"revenue": revenue_data})

    except SQLAlchemyError as e:
        # Handle error database
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        # Handle error lainnya
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500
    

@app.route('/api/monthly-category-data', methods=['GET'])
def get_monthly_category_data():
    try:
        # Hitung tanggal awal dan akhir bulan ini
        today = datetime.today()
        print(f"Today: {today}")
        first_day_of_month = datetime(today.year, today.month, 1)  # Awal bulan ini
        _, last_day = monthrange(today.year, today.month)
        last_day_of_month = datetime(today.year, today.month, last_day)  # Akhir bulan ini

        # Mundurkan start_date sehari untuk memastikan mencakup seluruh data di tanggal 1
        start_date = first_day_of_month - timedelta(days=1)
        end_date = last_day_of_month + timedelta(days=1)

        # Query untuk mengambil semua data expense bulan ini
        query_result = (
            db.session.query(Expense.kategori, Expense.nominal, Expense.tanggal)
            .filter(Expense.tanggal >= start_date, Expense.tanggal < end_date)
            .all()
        )
        print(f"start_date: {start_date}, end_date: {end_date}")
        print(f"Query Result: {query_result}")

        # Konversi hasil query ke Pandas DataFrame
        data = [{"kategori": row.kategori, "nominal": float(row.nominal), "tanggal": row.tanggal} for row in query_result]
        df = pd.DataFrame(data)

        # Jika tidak ada data, kembalikan list kosong
        if df.empty:
            return jsonify({
                "categories": [],
                "values": [],
                "colors": []
            })

        # Filter dan proses data menggunakan Pandas
        # Menghitung total nominal untuk setiap kategori
        monthly_data = df.groupby('kategori', as_index=False)['nominal'].sum()

        # Urutkan berdasarkan nominal tertinggi
        monthly_data = monthly_data.sort_values(by='nominal', ascending=False)

        # Daftar warna statis untuk setiap kategori
        colors = ['#007BFF', '#28A745', '#FFC107', '#DC3545', '#6C757D', 
                  '#17A2B8', '#6610F2', '#E83E8C', '#FD7E14', '#20C997']

        # Proses data untuk format JSON
        categories = monthly_data['kategori'].tolist()  # Nama kategori
        values = monthly_data['nominal'].tolist()  # Nilai nominal
        category_colors = colors[:len(categories)]  # Warna sesuai jumlah kategori

        # Format output JSON
        return jsonify({
            "categories": categories,
            "values": values,
            "colors": category_colors  # Tambahkan warna ke respons
        })

    except Exception as e:
        # Handle error jika terjadi masalah
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True, port=5111)