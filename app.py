<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Aplikasi Kasir Sederhana</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Aplikasi Kasir POS</a>
            <div class="navbar-nav">
                <a class="nav-link active" href="/">Kasir & Produk</a>
                <a class="nav-link" href="/riwayat">Riwayat Penjualan</a>
            </div>
        </div>
    </nav>

    <div class="container">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="row">
            <!-- Kolom Input Produk & Transaksi Kasir -->
            <div class="col-md-4 mb-4">
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-primary text-white">Tambah Produk Baru</div>
                    <div class="card-body">
                        <form action="/tambah_produk" method="POST">
                            <div class="mb-3"><label>Nama Produk</label><input type="text" class="form-control" name="nama" required></div>
                            <div class="mb-3"><label>Harga (Rp)</label><input type="number" class="form-control" name="harga" required></div>
                            <div class="mb-3"><label>Stok Awal</label><input type="number" class="form-control" name="stok" required></div>
                            <button type="submit" class="btn btn-primary w-100">Simpan Produk</button>
                        </form>
                    </div>
                </div>

                <div class="card shadow-sm">
                    <div class="card-header bg-success text-white">Form Kasir (Transaksi)</div>
                    <div class="card-body">
                        <form action="/checkout" method="POST">
                            <div class="mb-3">
                                <label>Pilih Produk</label>
                                <select class="form-select" name="produk_id" required>
                                    <option value="">-- Pilih Barang --</option>
                                    {% for p in produk %}
                                        <option value="{{ p['id'] }}">{{ p['nama'] }} (Stok: {{ p['stok'] }} | Rp {{ p['harga'] }})</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label>Jumlah Beli</label>
                                <input type="number" class="form-control" name="jumlah" min="1" required>
                            </div>
                            <button type="submit" class="btn btn-success w-100">Bayar / Checkout</button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Kolom Daftar Produk -->
            <div class="col-md-8">
                <div class="card shadow-sm">
                    <div class="card-header bg-dark text-white">Daftar Produk & Harga</div>
                    <div class="card-body">
                        <table class="table table-bordered table-striped align-middle">
                            <thead class="table-dark">
                                <tr><th>No</th><th>Nama Produk</th><th>Harga</th><th>Stok</th></tr>
                            </thead>
                            <tbody>
                                {% for p in produk %}
                                    <tr>
                                        <td>{{ loop.index }}</td>
                                        <td>{{ p['nama'] }}</td>
                                        <td>Rp {{ "{:,}".format(p['harga']) }}</td>
                                        <td>{{ p['stok'] }}</td>
                                    </tr>
                                {% else %}
                                    <tr><td colspan="4" class="text-center">Belum ada produk tersedia.</td></tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Riwayat Penjualan - Kasir</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Aplikasi Kasir POS</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Kasir & Produk</a>
                <a class="nav-link active" href="/riwayat">Riwayat Penjualan</a>
            </div>
        </div>
    </nav>

    <div class="container">
        <div class="card shadow-sm">
            <div class="card-header bg-dark text-white">Laporan Riwayat Transaksi</div>
            <div class="card-body">
                <table class="table table-bordered table-striped align-middle">
                    <thead class="table-dark">
                        <tr><th>No</th><th>Waktu</th><th>Nama Produk</th><th>Jumlah Terjual</th><th>Total Pendapatan</th></tr>
                    </thead>
                    <tbody>
                        {% for t in transaksi %}
                            <tr>
                                <td>{{ loop.index }}</td>
                                <td>{{ t['tanggal'] }}</td>
                                <td>{{ t['nama_produk'] }}</td>
                                <td>{{ t['jumlah'] }}</td>
                                <td><strong>Rp {{ "{:,}".format(t['total_harga']) }}</strong></td>
                            </tr>
                        {% else %}
                            <tr><td colspan="5" class="text-center">Belum ada transaksi tercatat.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>
