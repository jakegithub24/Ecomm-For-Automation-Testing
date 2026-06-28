import os
import json
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from argon2 import PasswordHasher

ph = PasswordHasher()
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD_HASH = '$argon2id$v=19$m=65536,t=3,p=4$/pCil7SDH0jbWFyr0lHhVA$/NKMJ+Vr+5R9/sOkNbrKaMU5buNY2l7OT/QKZrFX2/A'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), 401
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///price_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ─── Models ───

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=True)
    original_price = db.Column(db.Float, nullable=True)
    state = db.Column(db.String(50), default='coming soon')  # coming soon, In Stock, out of stock, discontinued
    image_url = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(100), default='Tech')
    url = db.Column(db.String(500), nullable=True)  # e-commerce page URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    price_history = db.relationship('PriceHistory', backref='product', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'brand': self.brand,
            'description': self.description,
            'price': self.price,
            'original_price': self.original_price,
            'state': self.state,
            'image_url': self.image_url,
            'category': self.category,
            'url': self.url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'discount_percent': round((1 - self.price / self.original_price) * 100, 1) if self.price and self.original_price and self.original_price > 0 else 0
        }

class PriceHistory(db.Model):
    __tablename__ = 'price_history'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'price': self.price,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

# ─── Seed Data ───

def seed_data():
    if Product.query.first() is None:
        sample_products = [
            Product(
                name='Sony WH-1000XM5',
                brand='Sony',
                description='Industry-leading noise canceling wireless headphones with 30-hour battery life.',
                price=348.00,
                original_price=399.99,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&h=600&fit=crop',
                category='Audio',
                url='https://www.sony.com/headphones'
            ),
            Product(
                name='MacBook Pro 14" M3',
                brand='Apple',
                description='Supercharged by M3 chip. Up to 22 hours battery life. Stunning Liquid Retina XDR display.',
                price=1599.00,
                original_price=1799.00,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&h=600&fit=crop',
                category='Laptops',
                url='https://www.apple.com/macbook-pro'
            ),
            Product(
                name='Samsung Galaxy S24 Ultra',
                brand='Samsung',
                description='AI-powered smartphone with 200MP camera and S Pen built-in.',
                price=1099.99,
                original_price=1299.99,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1610792516320-2d1261a04f11?w=600&h=600&fit=crop',
                category='Phones',
                url='https://www.samsung.com/galaxy-s24-ultra'
            ),
            Product(
                name='Steam Deck OLED',
                brand='Valve',
                description='Handheld gaming console with HDR OLED display. 512GB storage.',
                price=549.00,
                original_price=549.00,
                state='out of stock',
                image_url='https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=600&h=600&fit=crop',
                category='Gaming',
                url='https://www.steamdeck.com'
            ),
            Product(
                name='Vision Pro',
                brand='Apple',
                description='Spatial computer that seamlessly blends digital content with your physical space.',
                price=3499.00,
                original_price=3499.00,
                state='coming soon',
                image_url='https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=600&h=600&fit=crop',
                category='VR/AR',
                url='https://www.apple.com/vision-pro'
            ),
            Product(
                name='Canon EOS R5',
                brand='Canon',
                description='Professional mirrorless camera with 45MP full-frame sensor and 8K video.',
                price=2899.00,
                original_price=3899.00,
                state='discontinued',
                image_url='https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&h=600&fit=crop',
                category='Cameras',
                url='https://www.canon.com/eos-r5'
            ),
            Product(
                name='DJI Mini 4 Pro',
                brand='DJI',
                description='Lightweight drone with 4K/60fps HDR video and omnidirectional obstacle sensing.',
                price=759.00,
                original_price=799.00,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=600&h=600&fit=crop',
                category='Drones',
                url='https://www.dji.com/mini-4-pro'
            ),
            Product(
                name='PlayStation 5 Pro',
                brand='Sony',
                description='The most powerful PlayStation ever. 8K gaming support. Wi-Fi 7.',
                price=699.99,
                original_price=699.99,
                state='coming soon',
                image_url='https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600&h=600&fit=crop',
                category='Gaming',
                url='https://www.playstation.com/ps5-pro'
            ),
            Product(
                name='iPad Pro 12.9" M2',
                brand='Apple',
                description='The ultimate iPad experience with M2 chip and Liquid Retina XDR display.',
                price=1099.00,
                original_price=1299.00,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&h=600&fit=crop',
                category='Tablets',
                url='https://www.apple.com/ipad-pro'
            ),
            Product(
                name='NVIDIA RTX 4090',
                brand='NVIDIA',
                description='The ultimate GeForce GPU. 24GB G6X memory for extreme gaming and creating.',
                price=1599.00,
                original_price=1999.00,
                state='out of stock',
                image_url='https://images.unsplash.com/photo-1591488320449-011701bb6704?w=600&h=600&fit=crop',
                category='Components',
                url='https://www.nvidia.com/rtx-4090'
            ),
            Product(
                name='Logitech MX Master 3S',
                brand='Logitech',
                description='Ultra-fast and precise wireless mouse with 8K DPI sensor.',
                price=89.99,
                original_price=99.99,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&h=600&fit=crop',
                category='Peripherals',
                url='https://www.logitech.com/mx-master-3s'
            ),
            Product(
                name='Keychron Q1 Pro',
                brand='Keychron',
                description='Wireless custom mechanical keyboard with QMK/VIA support and aluminum body.',
                price=199.00,
                original_price=219.00,
                state='In Stock',
                image_url='https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&h=600&fit=crop',
                category='Peripherals',
                url='https://www.keychron.com/q1-pro'
            )
        ]

        for p in sample_products:
            db.session.add(p)
            db.session.flush()  # Get ID without committing
            if p.price:
                db.session.add(PriceHistory(product_id=p.id, price=p.price))

        db.session.commit()
        print("Database seeded with sample products.")

# ─── Routes ───

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=[p.to_dict() for p in products])

@app.route('/admin')
@login_required
def admin():
    products = Product.query.all()
    return render_template('admin.html', products=[p.to_dict() for p in products])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('admin'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME:
            try:
                ph.verify(ADMIN_PASSWORD_HASH, password)
                session['logged_in'] = True
                flash('Successfully logged in!', 'success')
                return redirect(request.args.get('next') or url_for('admin'))
            except Exception:
                pass

        flash('Invalid username or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Successfully logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    history = PriceHistory.query.filter_by(product_id=product_id).order_by(PriceHistory.timestamp.desc()).limit(30).all()
    return render_template('product_detail.html', product=product.to_dict(), history=[h.to_dict() for h in history])

# ─── API Routes ───

@app.route('/api/products', methods=['GET'])
def api_products():
    state = request.args.get('state')
    category = request.args.get('category')
    query = Product.query
    if state:
        query = query.filter_by(state=state)
    if category:
        query = query.filter_by(category=category)
    products = query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def api_product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())

@app.route('/api/products', methods=['POST'])
@login_required
def api_create_product():
    data = request.get_json()

    product = Product(
        name=data.get('name'),
        brand=data.get('brand'),
        description=data.get('description'),
        price=data.get('price'),
        original_price=data.get('original_price'),
        state=data.get('state', 'coming soon'),
        image_url=data.get('image_url'),
        category=data.get('category', 'Tech'),
        url=data.get('url')
    )
    db.session.add(product)
    db.session.flush()

    if product.price:
        db.session.add(PriceHistory(product_id=product.id, price=product.price))

    db.session.commit()
    return jsonify(product.to_dict()), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def api_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    old_price = product.price

    product.name = data.get('name', product.name)
    product.brand = data.get('brand', product.brand)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.original_price = data.get('original_price', product.original_price)
    product.state = data.get('state', product.state)
    product.image_url = data.get('image_url', product.image_url)
    product.category = data.get('category', product.category)
    product.url = data.get('url', product.url)
    product.updated_at = datetime.utcnow()

    # Track price change
    if data.get('price') is not None and data.get('price') != old_price:
        db.session.add(PriceHistory(product_id=product.id, price=data.get('price')))

    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def api_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

@app.route('/api/products/<int:product_id>/history', methods=['GET'])
def api_price_history(product_id):
    product = Product.query.get_or_404(product_id)
    history = PriceHistory.query.filter_by(product_id=product_id).order_by(PriceHistory.timestamp.asc()).all()
    return jsonify([h.to_dict() for h in history])

@app.route('/api/categories', methods=['GET'])
def api_categories():
    categories = db.session.query(Product.category).distinct().all()
    return jsonify([c[0] for c in categories])

# ─── Price Alert Webhook (for automation script) ───

@app.route('/api/price-alert', methods=['POST'])
def price_alert():
    """Webhook endpoint for automation script to send price drop alerts."""
    data = request.get_json()
    product_id = data.get('product_id')
    new_price = data.get('new_price')
    old_price = data.get('old_price')
    threshold = data.get('threshold')

    # In a real app, you would send email/push notifications here
    return jsonify({
        'status': 'alert_received',
        'product_id': product_id,
        'new_price': new_price,
        'old_price': old_price,
        'threshold': threshold,
        'message': f'Price dropped from ${old_price} to ${new_price} (below threshold ${threshold})'
    }), 200

# ─── Health Check ───

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'ok', 'timestamp': datetime.utcnow().isoformat()})

# ─── Initialize ───

with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
