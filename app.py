from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  # Penting untuk session

# ------------------------ KONEKSI DB ------------------------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ------------------------ LOGIN ------------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

# ------------------------ BERANDA ------------------------
@app.route('/home')
def home():
    descriptions = {
        'Ford Mustang': 'Muscle car legendaris asal Amerika, dikenal dengan mesin bertenaga dan desain ikonik.',
        'Duesenberg SJ': 'Mobil mewah Amerika tahun 1930-an dengan performa luar biasa.',
        'GAZ-13 Chaika': 'Sedan mewah dari Uni Soviet, digunakan oleh pejabat tinggi.',
        'Dodge Charger': 'Simbol mobil cepat era 60-an, sering muncul di film.',
        'Nissan Fairlady Z': 'Sport car Jepang dengan desain aerodinamis dan performa handal.',
        'Subaru 360': 'Mobil mungil dari Jepang, ekonomis dan populer pada masanya.'
        # Tambahkan deskripsi lainnya di sini
    }
    return render_template('home.html', descriptions=descriptions)

# ------------------------ TENTANG ------------------------
@app.route('/about')
def about():
    return render_template('about.html')

# ------------------------ TAMBAH MOBIL ------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        conn = get_db_connection()
        conn.execute('INSERT INTO cars (brand, model) VALUES (?, ?)', (brand, model))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_car.html')

# ------------------------ EDIT MOBIL ------------------------
@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    conn = get_db_connection()
    car = conn.execute('SELECT * FROM cars WHERE id = ?', (car_id,)).fetchone()
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        conn.execute('UPDATE cars SET brand = ?, model = ? WHERE id = ?', (brand, model, car_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    conn.close()
    return render_template('edit_car.html', car=car)

# ------------------------ KELUAR ------------------------
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

# ------------------------ BELI (TAMBAH KE KERANJANG) ------------------------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    car_name = request.form['car']
    year = request.form['year']
    
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({'name': car_name, 'year': year})
    return redirect(url_for('home'))

# ------------------------ LIHAT KERANJANG ------------------------
@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    return render_template('cart.html', cart_items=cart_items)

# ------------------------ CHECKOUT ------------------------
@app.route('/checkout', methods=['POST'])
def checkout():
    buyer_name = request.form['buyer_name']
    buyer_phone = request.form['buyer_phone']
    cart = session.get('cart', [])

    if not cart:
        return "Keranjang kosong!"

    conn = get_db_connection()
    for item in cart:
        conn.execute("INSERT INTO purchases (buyer_name, buyer_phone, car_name, car_year) VALUES (?, ?, ?, ?)",
                     (buyer_name, buyer_phone, item['name'], item['year']))
    conn.commit()
    conn.close()

    session.pop('cart', None)
    return f"Terima kasih {buyer_name}, pembelian Anda telah diproses!"

# ------------------------ JALANKAN APP ------------------------
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))  # Gunakan PORT dari Railway
    app.run(host='0.0.0.0', port=port)        # Penting: host 0.0.0.0