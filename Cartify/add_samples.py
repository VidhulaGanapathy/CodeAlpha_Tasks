import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop.settings')   # tell Python which settings file to use
django.setup()                                                      # start Django so we can use our models

from store.models import Product                                    # import the Product table

# Each product is one tuple: (name, description, price)
# A tuple is like one row of a table: three values in a fixed order.
products = [
    # ---------- ELECTRONICS ----------
    ('Wireless Headphones', 'Over-ear Bluetooth headphones with deep bass, noise isolation and 30 hours of battery life. Comes with a carry pouch.', 2499),
    ('Smart Watch', 'Fitness smartwatch with heart-rate monitor, step counter and sleep tracking. Water resistant, works with Android and iOS.', 3999),
    ('Bluetooth Speaker', 'Portable speaker with 360 degree sound, strong bass and 12 hours of playtime. Splash proof for outdoor use.', 1499),
    ('Mechanical Keyboard', 'Compact keyboard with blue switches, RGB backlight and a sturdy metal frame. Great for coding and gaming.', 2799),
    ('Wireless Mouse', 'Slim silent-click mouse with adjustable DPI and a 12 month battery life. Works on any surface.', 699),
    ('Power Bank 20000mAh', 'High-capacity power bank with dual USB ports and fast charging. Charges a phone 4 to 5 times.', 1799),
    ('USB-C Fast Charger', '30W fast charger with a compact design and overheat protection. Suits phones, tablets and earbuds.', 999),
    ('Webcam Full HD', '1080p webcam with a built-in microphone and auto light correction. Ideal for online classes and meetings.', 1899),
    ('Laptop Stand', 'Foldable aluminium stand with 6 height levels. Improves posture and keeps your laptop cool.', 1099),
    ('Earbuds with Mic', 'Lightweight in-ear earbuds with clear calling, comfortable fit and 20 hours of total playtime.', 1299),
    ('Portable SSD 1TB', 'Pocket-sized external drive with fast read speeds and a shock-resistant body. Perfect for backups.', 7499),
    ('Smart LED Bulb', 'Wi-Fi bulb with 16 million colours and voice control. Set schedules from your phone.', 499),

    # ---------- FASHION ----------
    ('Backpack', 'Spacious 30 litre laptop backpack with padded straps, USB charging port and water-resistant fabric.', 1299),
    ('Running Shoes', 'Lightweight breathable running shoes with a cushioned sole and anti-slip grip.', 1999),
    ('Cotton T-Shirt', 'Soft 100 percent cotton round-neck t-shirt. Comfortable for daily wear and available in many colours.', 499),
    ('Denim Jacket', 'Classic blue denim jacket with a regular fit and sturdy stitching. Easy to pair with anything.', 2299),
    ('Leather Wallet', 'Slim genuine leather wallet with 6 card slots, a coin pocket and a note compartment.', 799),
    ('Sunglasses', 'UV400 protection sunglasses with a lightweight frame and scratch-resistant lenses.', 999),
    ('Formal Shirt', 'Wrinkle-resistant full sleeve formal shirt. Perfect for office and interviews.', 1199),
    ('Sports Cap', 'Breathable adjustable cap with a moisture-wicking band. Great for running and travel.', 349),
    ('Analog Wrist Watch', 'Elegant stainless steel watch with a date display and water resistance up to 30 metres.', 1799),
    ('Canvas Sneakers', 'Everyday canvas sneakers with a rubber sole and cushioned insole. Simple, comfortable and stylish.', 1499),

    # ---------- HOME AND KITCHEN ----------
    ('Stainless Steel Water Bottle', 'Double-wall insulated 1 litre bottle. Keeps drinks cold for 24 hours and hot for 12 hours. Leak-proof and BPA free.', 599),
    ('Table Lamp', 'LED desk lamp with 3 brightness levels, touch control and a flexible neck. Gentle on the eyes.', 899),
    ('Electric Kettle', '1.5 litre stainless steel kettle with auto shut-off. Boils water in minutes.', 1199),
    ('Non-Stick Frying Pan', 'Durable non-stick pan with a heat-resistant handle. Needs little oil and cleans easily.', 899),
    ('Mixer Grinder', '750W mixer grinder with 3 jars and strong blades. Handles wet and dry grinding.', 3499),
    ('Air Fryer', '4 litre air fryer that cooks crispy food with very little oil. Digital controls and 8 preset modes.', 5999),
    ('Lunch Box Set', 'Set of 3 leak-proof containers with a carry bag. Microwave safe and easy to clean.', 649),
    ('Cotton Bedsheet', 'Soft double bedsheet with 2 pillow covers. Fade resistant and gentle on the skin.', 1099),
    ('Wall Clock', 'Silent non-ticking wall clock with a modern round design. Suits living rooms and offices.', 749),
    ('Vacuum Cleaner', 'Powerful bagless vacuum cleaner with a HEPA filter and 3 attachments. Cleans floors, sofas and corners.', 8999),
    ('Dinner Set 24 Pieces', 'Elegant ceramic dinner set for 6 people. Dishwasher and microwave safe.', 2499),
    ('Storage Containers Set', 'Set of 6 airtight containers for rice, pulses and snacks. Keeps food fresh for longer.', 799),

    # ---------- FITNESS ----------
    ('Yoga Mat', 'Extra thick anti-slip yoga mat with a carry strap. Comfortable for yoga, stretching and workouts.', 799),
    ('Dumbbell Set', 'Pair of adjustable dumbbells with a non-slip grip. Great for home strength training.', 2199),
    ('Skipping Rope', 'Tangle-free speed rope with foam handles and an adjustable length. Good for cardio.', 249),
    ('Resistance Bands Set', 'Set of 5 bands with different resistance levels and a carry bag. Works for the whole body.', 599),
    ('Gym Gloves', 'Padded gym gloves with wrist support and a breathable back. Protect your hands while lifting.', 399),
    ('Fitness Tracker Band', 'Slim band that tracks steps, calories and sleep. Alerts for calls and messages, 10 day battery.', 1999),

    # ---------- STATIONERY ----------
    ('Spiral Notebook Pack', 'Pack of 5 ruled notebooks with 200 pages each. Smooth paper that does not bleed.', 299),
    ('Gel Pen Set', 'Set of 20 smooth gel pens in assorted colours. Quick drying and comfortable to hold.', 199),
    ('Study Desk Organizer', 'Wooden desk organizer with compartments for pens, notes and a phone. Keeps your table tidy.', 549),
    ('Scientific Calculator', 'Calculator with 240 functions and a two-line display. Allowed in most school and college exams.', 899),
    ('Sketchbook A4', 'A4 sketchbook with 100 thick pages. Suitable for pencil, charcoal and light colours.', 349),

    # ---------- PERSONAL CARE AND TOYS ----------
    ('Electric Trimmer', 'Cordless trimmer with 3 length settings and a 60 minute run time. Washable blades.', 1399),
    ('Hair Dryer', '1600W hair dryer with 2 speed settings and a cool shot button. Foldable and travel friendly.', 1299),
    ('Face Wash', 'Gentle daily face wash with neem and aloe vera. Cleans oil and dirt without drying the skin.', 249),
    ('Perfume Spray', 'Long-lasting fresh fragrance with citrus and woody notes. 100 ml bottle.', 1499),
    ('Chess Set', 'Wooden foldable chess board with storage for the pieces. Great for beginners and players.', 699),
    ('Remote Control Car', 'Rechargeable 2.4GHz remote car with strong grip tyres and LED lights. Fun for kids and adults.', 1299),
    ('Jigsaw Puzzle 500 Pieces', 'Colourful 500 piece puzzle that improves focus and patience. Packed in a sturdy box.', 399),
]

added = 0                                                           # counter for new products

for name, description, price in products:                           # take each tuple and split it into 3 variables
    image_url = 'https://placehold.co/400x300.png?text=' + name.replace(' ', '+')
    # placeholder picture with the product name on it; spaces become '+' so the link stays valid

    obj, created = Product.objects.get_or_create(                   # look for a product with this name; create it only if missing
        name=name,
        defaults={                                                  # these values are used only when creating
            'description': description,
            'price': price,
            'image_url': image_url,
        },
    )
    if created:                                                     # True only when a new row was made
        added += 1                                                  # count it

print(f'Done! {added} new products added. Total products in store: {Product.objects.count()}')