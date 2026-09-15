from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3

app = Flask(__name__)
app.secret_key = 'rahasia'

def get_db():
    conn = sqlite3.connect('kasir.db')
    conn.row_factory = sqlite3.Row
    return conn

# Buat database otomatis jika belum ada
with get_db() as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS produk (id INTEGER PRIMARY KEY AUTOINCREMENT, nama TEXT, harga INTEGER, stok INTEGER)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS transaksi (id INTEGER PRIMARY KEY AUTOINCREMENT, barang TEXT, jumlah INTEGER, total INTEGER, waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Aplikasi Kasir Simple</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="container py-4 bg-light">
    <h2 class="mb-4">🛒 Aplikasi Kasir Sederhana</h2>

    <!-- Form Tambah Produk -->
    <div class="card mb-4 shadow-sm"><div class="card-body">
        <h5>Tambah Produk</h5>
        <form method="POST" action="/tambah" class="row g-2">
            <div class="col-md-4"><input type="text" name="nama" class="form-control" placeholder="Nama Barang" required></div>
            <div class="col-md-3"><input type="number" name="harga" class="form-control" placeholder="Harga (Rp)" required></div>
            <div class="col-md-3"><input type="number" name="stok" class="form-control" placeholder="Stok Awal" required></div>
            <div class="col-md-2"><button type="submit" class="btn btn-primary w-100">Simpan</button></div>
        </form>
    </div></div>

    <!-- Form Transaksi Kasir -->
    <div class="card mb-4 shadow-sm"><div class="card-body">
        <h5>Kasir / Penjualan</h5>
        <form method="POST" action="/beli" class="row g-2">
            <div class="col-md-6">
                <select name="produk_id" class="form-select" required>
                    <option value="">-- Pilih Barang --</option>
                    {% for p in produk %}
                    <option value="{{ p['id'] }}">{{ p['nama'] }} (Stok: {{ p['stok'] }} | Rp {{ p['harga'] }})</option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-4"><input type="number" name="jumlah" class="form-control" placeholder="Jumlah Beli" min="1" required></div>
            <div class="col-md-2"><button type="submit" class="btn btn-success w-100">Bayar</button></div>
        </form>
    </div></div>

    <!-- Tabel Stok -->
    <div class="card mb-4 shadow-sm"><div class="card-body">
        <h5>Daftar Produk</h5>
        <table class="table table-bordered">
            <thead class="table-dark"><tr><th>Nama</th><th>Harga</th><th>Stok</th></tr></thead>
            <tbody>
                {% for p in produk %}
                <tr><td>{{ p['nama'] }}</td><td>Rp {{ "{:,}".format(p['harga']) }}</td><td>{{ p['stok'] }}</td></tr>
                {% else %}
                <tr><td colspan="3" class="text-center">Belum ada produk.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div></div>

    <!-- Riwayat -->
    <div class="card shadow-sm"><div class="card-body">
        <h5>Riwayat Transaksi</h5>
        <table class="table table-striped">
            <thead class="table-secondary"><tr><th>Waktu</th><th>Barang</th><th>Jumlah</th><th>Total</th></tr></thead>
            <tbody>
                {% for t in riwayat %}
                <tr><td>{{ t['waktu'] }}</td><td>{{ t['barang'] }}</td><td>{{ t['jumlah'] }}</td><td>Rp {{ "{:,}".format(t['total']) }}</td></tr>
                {% else %}
                <tr><td colspan="4" class="text-center">Belum ada transaksi.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div></div>
</body>
</html>
"""

@app.route('/')
def index():
    with get_db() as conn:
        produk = conn.execute('SELECT * FROM produk').fetchall()
        riwayat = conn.execute('SELECT * FROM transaksi ORDER BY id DESC').fetchall()
    return render_template_string(HTML_TEMPLATE, produk=produk, riwayat=riwayat)

@app.route('/tambah', methods=['POST'])
def tambah():
    with get_db() as conn:
        conn.execute('INSERT INTO produk (nama, harga, stok) VALUES (?, ?, ?)',
                     (request.form['nama'], int(request.form['harga']), int(request.form['stok'])))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/beli', methods=['POST'])
def beli():
    pid = int(request.form['produk_id'])
    jumlah = int(request.form['jumlah'])
    with get_db() as conn:
        p = conn.execute('SELECT * FROM produk WHERE id = ?', (pid,)).fetchone()
        if p and p['stok'] >= jumlah:
            total = p['harga'] * jumlah
            conn.execute('UPDATE produk SET stok = ? WHERE id = ?', (p['stok'] - jumlah, pid))
            conn.execute('INSERT INTO transaksi (barang, jumlah, total) VALUES (?, ?, ?)', (p['nama'], jumlah, total))
            conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
