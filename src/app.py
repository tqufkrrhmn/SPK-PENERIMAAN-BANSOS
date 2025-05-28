from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import math
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_my_favorite_key_mama'

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'spk_bansos'

mysql = MySQL(app)

# Fungsi untuk menghitung SAW
def hitung_saw():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Ambil data kriteria
    cursor.execute("SELECT * FROM kriteria")
    kriteria = cursor.fetchall()
    
    # Ambil data alternatif
    cursor.execute("SELECT * FROM alternatif")
    alternatif = cursor.fetchall()
    
    # Ambil nilai alternatif
    cursor.execute("""
        SELECT a.id_alternatif, a.nama_kepala_keluarga, k.id_kriteria, k.nama_kriteria, k.atribut, k.bobot, n.nilai 
        FROM alternatif a
        JOIN nilai_alternatif n ON a.id_alternatif = n.id_alternatif
        JOIN kriteria k ON n.id_kriteria = k.id_kriteria
        ORDER BY a.id_alternatif, k.id_kriteria
    """)
    data_nilai = cursor.fetchall()
    
    # Struktur data untuk perhitungan
    matriks_keputusan = {}
    for alt in alternatif:
        matriks_keputusan[alt['id_alternatif']] = {
            'nama': alt['nama_kepala_keluarga'],
            'no_kk': alt['no_kk'],
            'alamat': alt['alamat'],
            'nilai': {}
        }
    
    for row in data_nilai:
        matriks_keputusan[row['id_alternatif']]['nilai'][row['id_kriteria']] = row['nilai']
    
    # Normalisasi matriks
    max_min = {}
    for k in kriteria:
        values = [matriks_keputusan[alt]['nilai'][k['id_kriteria']] for alt in matriks_keputusan if k['id_kriteria'] in matriks_keputusan[alt]['nilai']]
        if values:
            if k['atribut'] == 'benefit':
                max_min[k['id_kriteria']] = max(values)
            else:
                max_min[k['id_kriteria']] = min(values)
        else:
            # Handle kasus jika tidak ada nilai untuk kriteria ini
            max_min[k['id_kriteria']] = 1.0 if k['atribut'] == 'benefit' else 1.0 # Nilai default jika tidak ada data

    matriks_normalisasi = {}
    hasil_saw = []

    for alt_id, alt_data in matriks_keputusan.items():
        matriks_normalisasi[alt_id] = {
            'nama': alt_data['nama'],
            'no_kk': alt_data['no_kk'],
            'alamat': alt_data['alamat'],
            'nilai': {},
            'total': 0
        }
        total_nilai_tertimbang = 0
        for k in kriteria:
            nilai_ternormalisasi = 0
            if k['id_kriteria'] in alt_data['nilai']:
                nilai_mentah = alt_data['nilai'][k['id_kriteria']]
                if max_min[k['id_kriteria']] != 0 and max_min[k['id_kriteria']] != float('inf') and max_min[k['id_kriteria']] != -float('inf'): # Tambahkan pengecekan infiniti
                    if k['atribut'] == 'benefit':
                        nilai_ternormalisasi = nilai_mentah / max_min[k['id_kriteria']] if max_min[k['id_kriteria']] != 0 else 0
                    else:
                        nilai_ternormalisasi = max_min[k['id_kriteria']] / nilai_mentah if nilai_mentah != 0 else 0
                # else: # Handle kasus jika max_min adalah 0 atau infiniti
                #     nilai_ternormalisasi = 0 # Atau nilai default lainnya
            
            matriks_normalisasi[alt_id]['nilai'][k['id_kriteria']] = nilai_ternormalisasi
            total_nilai_tertimbang += nilai_ternormalisasi * k['bobot']
        
        matriks_normalisasi[alt_id]['total'] = total_nilai_tertimbang
        hasil_saw.append((alt_id, matriks_normalisasi[alt_id]))
    
    # Urutkan berdasarkan total nilai tertinggi
    hasil_saw = sorted(hasil_saw, key=lambda x: x[1]['total'], reverse=True)
    
    return kriteria, alternatif, hasil_saw

# Routing
@app.route('/')
def home():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['role'] = account['role']
            return redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah!', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = 'admin'  # Atur role sesuai kebutuhan
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                      (username, password, role))
        mysql.connection.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT COUNT(*) as total FROM alternatif")
        total_alternatif = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM kriteria")
        total_kriteria = cursor.fetchone()['total']
        
        return render_template('dashboard.html', 
                            username=session['username'],
                            role=session['role'],
                            total_alternatif=total_alternatif,
                            total_kriteria=total_kriteria)
    return redirect(url_for('login'))

@app.route('/kriteria', methods=['GET', 'POST'])
def kriteria():
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        nama = request.form['nama']
        atribut = request.form['atribut']
        bobot = float(request.form['bobot'])
        
        cursor.execute("INSERT INTO kriteria (nama_kriteria, atribut, bobot) VALUES (%s, %s, %s)", 
                      (nama, atribut, bobot))
        mysql.connection.commit()
        flash('Kriteria berhasil ditambahkan!', 'success')
        return redirect(url_for('kriteria'))
    
    cursor.execute("SELECT * FROM kriteria")
    data = cursor.fetchall()
    
    # Hitung total bobot untuk validasi
    cursor.execute("SELECT SUM(bobot) as total FROM kriteria")
    total_bobot = cursor.fetchone()['total'] or 0
    
    return render_template('kriteria.html', kriteria=data, total_bobot=total_bobot)

@app.route('/kriteria/edit/<int:id>', methods=['GET', 'POST'])
def edit_kriteria(id):
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        nama = request.form['nama']
        atribut = request.form['atribut']
        bobot = float(request.form['bobot'])
        
        cursor.execute("UPDATE kriteria SET nama_kriteria=%s, atribut=%s, bobot=%s WHERE id_kriteria=%s", 
                      (nama, atribut, bobot, id))
        mysql.connection.commit()
        flash('Kriteria berhasil diupdate!', 'success')
        return redirect(url_for('kriteria'))
    
    cursor.execute("SELECT * FROM kriteria WHERE id_kriteria = %s", (id,))
    data = cursor.fetchone()
    
    return render_template('edit_kriteria.html', kriteria=data)

@app.route('/kriteria/delete/<int:id>')
def delete_kriteria(id):
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM kriteria WHERE id_kriteria = %s", (id,))
    mysql.connection.commit()
    flash('Kriteria berhasil dihapus!', 'success')
    return redirect(url_for('kriteria'))

@app.route('/alternatif', methods=['GET', 'POST'])
def alternatif():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        no_kk = request.form['no_kk']
        nama = request.form['nama']
        alamat = request.form['alamat']
        
        cursor.execute("INSERT INTO alternatif (no_kk, nama_kepala_keluarga, alamat) VALUES (%s, %s, %s)", 
                      (no_kk, nama, alamat))
        mysql.connection.commit()
        flash('Alternatif berhasil ditambahkan!', 'success')
        return redirect(url_for('alternatif'))
    
    cursor.execute("SELECT * FROM alternatif")
    data = cursor.fetchall()
    
    return render_template('alternatif.html', alternatif_list=data)

@app.route('/alternatif/edit/<int:id>', methods=['GET', 'POST'])
def edit_alternatif(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        no_kk = request.form['no_kk']
        nama = request.form['nama']
        alamat = request.form['alamat']
        
        cursor.execute("UPDATE alternatif SET no_kk=%s, nama_kepala_keluarga=%s, alamat=%s WHERE id_alternatif=%s", 
                      (no_kk, nama, alamat, id))
        mysql.connection.commit()
        flash('Alternatif berhasil diupdate!', 'success')
        return redirect(url_for('alternatif'))
    
    cursor.execute("SELECT * FROM alternatif WHERE id_alternatif = %s", (id,))
    data = cursor.fetchone()
    
    return render_template('edit_alternatif.html', alternatif=data)

@app.route('/alternatif/delete/<int:id>')
def delete_alternatif(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM alternatif WHERE id_alternatif = %s", (id,))
    mysql.connection.commit()
    flash('Alternatif berhasil dihapus!', 'success')
    return redirect(url_for('alternatif'))

@app.route('/nilai', methods=['GET', 'POST'])
def nilai():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        alternatif_id = request.form['alternatif']
        
        # Hapus nilai lama jika ada
        cursor.execute("DELETE FROM nilai_alternatif WHERE id_alternatif = %s", (alternatif_id,))
        
        # Insert nilai baru
        cursor.execute("SELECT * FROM kriteria")
        kriteria = cursor.fetchall()
        
        for k in kriteria:
            nilai = request.form.get(f"nilai_{k['id_kriteria']}")
            if nilai:
                cursor.execute("INSERT INTO nilai_alternatif (id_alternatif, id_kriteria, nilai) VALUES (%s, %s, %s)", 
                             (alternatif_id, k['id_kriteria'], float(nilai)))
        
        mysql.connection.commit()
        flash('Nilai alternatif berhasil disimpan!', 'success')
        return redirect(url_for('nilai'))
    
    cursor.execute("SELECT * FROM alternatif")
    alternatif_data = cursor.fetchall()
    
    cursor.execute("SELECT * FROM kriteria")
    kriteria_data = cursor.fetchall()
    
    # Ambil data nilai yang sudah ada
    cursor.execute("SELECT * FROM nilai_alternatif")
    nilai_data = cursor.fetchall()
    
    # Struktur data untuk memudahkan pencarian nilai
    nilai_dict = {}
    for n in nilai_data:
        if n['id_alternatif'] not in nilai_dict:
            nilai_dict[n['id_alternatif']] = {}
        nilai_dict[n['id_alternatif']][n['id_kriteria']] = n['nilai']
    
    return render_template('nilai.html', 
                         alternatif=alternatif_data, 
                         kriteria=kriteria_data,
                         nilai=nilai_dict)

@app.route('/perhitungan')
def perhitungan():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    kriteria_list, alternatif_list, hasil_perhitungan = hitung_saw()
    
    # Hitung max dan min untuk normalisasi
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id_kriteria, atribut FROM kriteria")
    kriteria_data = cursor.fetchall()
    
    max_values = {}
    min_values = {}
    
    for k in kriteria_data:
        cursor.execute("SELECT MAX(nilai) as max_val, MIN(nilai) as min_val FROM nilai_alternatif WHERE id_kriteria = %s", (k['id_kriteria'],))
        result = cursor.fetchone()
        if result:
            max_values[k['id_kriteria']] = result['max_val'] or 0
            min_values[k['id_kriteria']] = result['min_val'] if result and result['min_val'] is not None else float('inf')

    # Ambil nilai_dict untuk Matriks Keputusan dan Normalisasi Matriks
    cursor.execute("SELECT id_alternatif, id_kriteria, nilai FROM nilai_alternatif")
    nilai_data = cursor.fetchall()

    nilai_dict = {}
    for n in nilai_data:
        if n['id_alternatif'] not in nilai_dict:
            nilai_dict[n['id_alternatif']] = {}
        nilai_dict[n['id_alternatif']][n['id_kriteria']] = n['nilai']
    
    return render_template('perhitungan.html', 
                         kriteria_list=kriteria_list, 
                         alternatif_list=alternatif_list, 
                         hasil_perhitungan=hasil_perhitungan,
                         max_values=max_values,
                         min_values=min_values,
                         nilai_dict=nilai_dict)

@app.route('/laporan', methods=['GET', 'POST'])
def laporan():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        judul = request.form['judul']
        deskripsi = request.form['deskripsi']
        # Asumsikan Anda ingin menyimpan hasil perhitungan saat laporan dibuat
        kriteria, alternatif, hasil_saw = hitung_saw() # Hitung SAW saat membuat laporan
        # Di sini Anda perlu menyimpan hasil_saw atau ringkasannya ke tabel laporan
        # Untuk contoh ini, kita hanya menyimpan judul dan deskripsi
        cursor.execute("INSERT INTO laporan (judul, deskripsi) VALUES (%s, %s)", (judul, deskripsi))
        mysql.connection.commit()
        flash('Laporan berhasil dibuat!', 'success')
        return redirect(url_for('laporan'))

    # Tampilkan daftar laporan yang sudah ada
    cursor.execute("SELECT * FROM laporan ORDER BY tanggal DESC")
    laporan_list = cursor.fetchall()

    return render_template('laporan.html', 
                           laporan_list=laporan_list)

@app.route('/laporan/cetak/<int:id>') # Tambahkan route untuk cetak laporan spesifik
def cetak_laporan(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM laporan WHERE id = %s", (id,))
    laporan_data = cursor.fetchone()

    if not laporan_data:
        flash('Laporan tidak ditemukan!', 'danger')
        return redirect(url_for('laporan'))

    # Untuk mencetak laporan, Anda mungkin perlu mengambil kembali hasil SAW yang relevan atau
    # jika hasil SAW disimpan di tabel laporan, ambil dari sana.
    # Untuk contoh sederhana, kita akan hitung ulang SAW (ini mungkin tidak efisien untuk data besar)
    kriteria, alternatif, hasil_saw = hitung_saw()

    return render_template('cetak_laporan.html', 
                           laporan=laporan_data,
                           kriteria=kriteria,
                           alternatif=alternatif,
                           hasil_saw=hasil_saw)

@app.route('/laporan/edit/<int:id>', methods=['GET', 'POST'])
def edit_laporan(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        judul = request.form['judul']
        deskripsi = request.form['deskripsi']
        cursor.execute("UPDATE laporan SET judul = %s, deskripsi = %s WHERE id = %s", (judul, deskripsi, id))
        mysql.connection.commit()
        flash('Laporan berhasil diupdate!', 'success')
        return redirect(url_for('laporan'))

    cursor.execute("SELECT * FROM laporan WHERE id = %s", (id,))
    laporan_data = cursor.fetchone()

    if not laporan_data:
        flash('Laporan tidak ditemukan!', 'danger')
        return redirect(url_for('laporan'))

    return render_template('edit_laporan.html', laporan=laporan_data)

@app.route('/laporan/delete/<int:id>', methods=['POST'])
def delete_laporan(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM laporan WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Laporan berhasil dihapus!', 'success')
    return redirect(url_for('laporan'))

@app.route('/users', methods=['GET', 'POST'])
def users():
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                      (username, password, role))
        mysql.connection.commit()
        flash('User berhasil ditambahkan!', 'success')
        return redirect(url_for('users'))
    
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    
    return render_template('users.html', users=data)

@app.route('/users/delete/<int:id>')
def delete_user(id):
    if 'loggedin' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('User berhasil dihapus!', 'success')
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)