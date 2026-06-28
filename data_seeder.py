import os
from app import app, db, Product, PriceHistory

def seed():
    # List of initial products
    products = [
        {
            'name': 'Sony WH-1000XM5',
            'brand': 'Sony',
            'description': 'Industry-leading noise canceling wireless headphones with 30-hour battery life.',
            'price': 348.00,
            'original_price': 399.99,
            'state': 'In Stock',
            'image_url': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=600&h=600&fit=crop',
            'category': 'Audio',
            'url': 'https://www.sony.com/headphones'
        },
        {
            'name': 'MacBook Pro 14" M3',
            'brand': 'Apple',
            'description': 'Supercharged by M3 chip. Up to 22 hours battery life. Stunning Liquid Retina XDR display.',
            'price': 1599.00,
            'original_price': 1799.00,
            'state': 'In Stock',
            'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=600&h=600&fit=crop',
            'category': 'Laptops',
            'url': 'https://www.apple.com/macbook-pro'
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'brand': 'Samsung',
            'description': 'AI-powered smartphone with 200MP camera and S Pen built-in.',
            'price': 1099.99,
            'original_price': 1299.99,
            'state': 'In Stock',
            'image_url': 'https://imgs.search.brave.com/-qgIwzxyJYea4V-VbkyYdHZF6g6XCVtQ1ouDRzTz-yg/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pbWFn/ZXMtbmEuc3NsLWlt/YWdlcy1hbWF6b24u/Y29tL2ltYWdlcy9J/LzUxSUoyNm5lYVVM/LmpwZw',
            'category': 'Phones',
            'url': 'https://www.samsung.com/galaxy-s24-ultra'
        },
        {
            'name': 'Steam Deck OLED',
            'brand': 'Valve',
            'description': 'Handheld gaming console with HDR OLED display. 512GB storage.',
            'price': 549.00,
            'original_price': 549.00,
            'state': 'out of stock',
            'image_url': 'https://images.unsplash.com/photo-1592840496694-26d035b52b48?w=600&h=600&fit=crop',
            'category': 'Gaming',
            'url': 'https://www.steamdeck.com'
        },
        {
            'name': 'Vision Pro',
            'brand': 'Apple',
            'description': 'Spatial computer that seamlessly blends digital content with your physical space.',
            'price': 3499.00,
            'original_price': 3499.00,
            'state': 'coming soon',
            'image_url': 'https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=600&h=600&fit=crop',
            'category': 'VR/AR',
            'url': 'https://www.apple.com/vision-pro'
        },
        {
            'name': 'Canon EOS R5',
            'brand': 'Canon',
            'description': 'Professional mirrorless camera with 45MP full-frame sensor and 8K video.',
            'price': 2899.00,
            'original_price': 3899.00,
            'state': 'discontinued',
            'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600&h=600&fit=crop',
            'category': 'Cameras',
            'url': 'https://www.canon.com/eos-r5'
        },
        {
            'name': 'DJI Mini 4 Pro',
            'brand': 'DJI',
            'description': 'Lightweight drone with 4K/60fps HDR video and omnidirectional obstacle sensing.',
            'price': 759.00,
            'original_price': 799.00,
            'state': 'In Stock',
            'image_url': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=600&h=600&fit=crop',
            'category': 'Drones',
            'url': 'https://www.dji.com/mini-4-pro'
        },
        {
            'name': 'PlayStation 5 Pro',
            'brand': 'Sony',
            'description': 'The most powerful PlayStation ever. 8K gaming support. Wi-Fi 7.',
            'price': 699.99,
            'original_price': 699.99,
            'state': 'coming soon',
            'image_url': 'https://images.unsplash.com/photo-1606813907291-d86efa9b94db?w=600&h=600&fit=crop',
            'category': 'Gaming',
            'url': 'https://www.playstation.com/ps5-pro'
        },
        {
            'name': 'iPad Pro 12.9" M2',
            'brand': 'Apple',
            'description': 'The ultimate iPad experience with M2 chip and Liquid Retina XDR display.',
            'price': 1099.00,
            'original_price': 1299.00,
            'state': 'In Stock',
            'image_url': 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=600&h=600&fit=crop',
            'category': 'Tablets',
            'url': 'https://www.apple.com/ipad-pro'
        },
        {
            'name': 'NVIDIA RTX 4090',
            'brand': 'NVIDIA',
            'description': 'The ultimate GeForce GPU. 24GB G6X memory for extreme gaming and creating.',
            'price': 1599.00,
            'original_price': 1999.00,
            'state': 'out of stock',
            'image_url': 'https://images.unsplash.com/photo-1591488320449-011701bb6704?w=600&h=600&fit=crop',
            'category': 'Components',
            'url': 'https://www.nvidia.com/rtx-4090'
        },
        {
            'name': 'Logitech MX Master 3S',
            'brand': 'Logitech',
            'description': 'Ultra-fast and precise wireless mouse with 8K DPI sensor.',
            'price': 89.99,
            'original_price': 99.99,
            'state': 'In Stock',
            'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=600&h=600&fit=crop',
            'category': 'Peripherals',
            'url': 'https://www.logitech.com/mx-master-3s'
        },
        {
            'name': 'Keychron Q1 Pro',
            'brand': 'Keychron',
            'description': 'Wireless custom mechanical keyboard with QMK/VIA support and aluminum body.',
            'price': 199.00,
            'original_price': 219.00,
            'state': 'In Stock',
            'image_url': 'https://images.unsplash.com/photo-1595225476474-87563907a212?w=600&h=600&fit=crop',
            'category': 'Peripherals',
            'url': 'https://www.keychron.com/q1-pro'
        }
    ]

    with app.app_context():
        # Recreate tables to start clean
        db.create_all()
        
        # Check if already seeded to prevent duplication
        if Product.query.first() is not None:
            print("Database already has data. Skipping seeding.")
            return

        for p_data in products:
            p = Product(
                name=p_data['name'],
                brand=p_data['brand'],
                description=p_data['description'],
                price=p_data['price'],
                original_price=p_data['original_price'],
                state=p_data['state'],
                image_url=p_data['image_url'],
                category=p_data['category'],
                url=p_data['url']
            )
            db.session.add(p)
            db.session.flush() # Get ID for foreign key
            
            if p.price is not None:
                # Add initial price history log
                db.session.add(PriceHistory(product_id=p.id, price=p.price))
                
        db.session.commit()
        print("Database successfully seeded with initial products.")

if __name__ == '__main__':
    seed()
