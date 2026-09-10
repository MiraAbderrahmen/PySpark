import csv
import os
import random
from datetime import datetime, timedelta

TARGET_BYTES = 500 * 1024 * 1024
OUTPUT_PATH = '/app/data/sales_en.csv'

products = [
    ('Laptop', 'Electronics', 'Dell', 499.99), ('Phone', 'Electronics', 'Samsung', 899.0),
    ('Tablet', 'Electronics', 'Apple', 649.0), ('Gaming Console', 'Electronics', 'Sony', 1199.99),
    ('Monitor', 'Electronics', 'LG', 329.5), ('Keyboard', 'Accessories', 'Logitech', 79.99),
    ('Mouse', 'Accessories', 'Razer', 59.99), ('Chair', 'Furniture', 'IKEA', 199.0),
    ('Desk', 'Furniture', 'Steelcase', 749.0), ('Printer', 'Office', 'HP', 249.5),
    ('Coffee Machine', 'Home', 'Nespresso', 249.99), ('Air Conditioner', 'Home', 'LG', 999.0),
    ('Refrigerator', 'Home', 'Samsung', 1399.99), ('Washing Machine', 'Home', 'Bosch', 899.0),
    ('Smart TV', 'Electronics', 'Samsung', 1299.99), ('Camera', 'Electronics', 'Canon', 799.0),
    ('Headphones', 'Electronics', 'Sony', 149.99), ('Router', 'Electronics', 'TP-Link', 119.5),
    ('Projector', 'Electronics', 'Epson', 899.99), ('Backpack', 'Lifestyle', 'North Face', 149.0),
    ('Sneakers', 'Fashion', 'Nike', 189.99), ('Watch', 'Fashion', 'Casio', 249.0),
    ('Sunglasses', 'Fashion', 'Ray-Ban', 179.0), ('Bicycle', 'Sports', 'Trek', 799.0),
    ('Treadmill', 'Sports', 'ProForm', 1499.0), ('Yoga Mat', 'Sports', 'Manduka', 59.95),
    ('Notebook', 'Office', 'HP', 19.99), ('Water Bottle', 'Lifestyle', 'Hydro Flask', 39.99),
    ('Blender', 'Home', 'Vitamix', 249.0), ('Vacuum Cleaner', 'Home', 'Dyson', 499.0),
    ('Microwave', 'Home', 'Panasonic', 179.99), ('Lamp', 'Home', 'Philips', 89.0),
    ('Desk Organizer', 'Office', 'Staples', 19.0), ('Speaker', 'Electronics', 'JBL', 119.99),
    ('Smartwatch', 'Electronics', 'Apple', 399.0), ('Tablet Stylus', 'Accessories', 'Wacom', 59.0),
    ('External SSD', 'Electronics', 'Samsung', 129.99), ('USB Hub', 'Accessories', 'Anker', 39.99),
    ('Gaming Mouse', 'Accessories', 'Corsair', 69.99), ('Office Chair', 'Furniture', 'Herman Miller', 899.0),
    ('Standing Desk', 'Furniture', 'Flexispot', 599.0), ('Couch', 'Furniture', 'IKEA', 699.99),
    ('Dining Table', 'Furniture', 'Ashley', 999.0), ('Luggage', 'Travel', 'Samsonite', 229.0)
]

cities = [
    ('Riyadh', 'Central'), ('Jeddah', 'Western'), ('Dammam', 'Eastern'), ('Mecca', 'Western'),
    ('Medina', 'Western'), ('Tabuk', 'Northern'), ('Abha', 'Southern'), ('Khobar', 'Eastern'),
    ('Taif', 'Western'), ('Jazan', 'Southern'), ('Madinah', 'Western'), ('Najran', 'Southern'),
    ('Hail', 'Northern'), ('Alahsa', 'Eastern'), ('Buraydah', 'Central'), ('Qassim', 'Central'),
    ('Yanbu', 'Western'), ('Jubail', 'Eastern')
]

channels = ['Online', 'Retail Store', 'Marketplace', 'B2B', 'Mobile App']
payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer', 'Apple Pay', 'PayPal']
customer_segments = ['Retail', 'Corporate', 'Government', 'SME', 'Wholesale']
order_statuses = ['Completed', 'Pending', 'Shipped', 'Returned', 'Cancelled']
regions = ['North', 'South', 'East', 'West', 'Central']
warehouses = ['WH-01', 'WH-02', 'WH-03', 'WH-04', 'WH-05']


def random_date(start_year=2023, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta_days = (end - start).days
    random_day = random.randint(0, delta_days)
    return (start + timedelta(days=random_day)).strftime('%Y-%m-%d')


filename = OUTPUT_PATH
os.makedirs(os.path.dirname(filename), exist_ok=True)

fieldnames = [
    'sale_id', 'product_name', 'category', 'brand', 'customer_id', 'price', 'quantity_sold',
    'discount_pct', 'tax_rate', 'total_amount', 'date', 'city', 'region', 'country',
    'channel', 'payment_method', 'customer_segment', 'order_status', 'store_id', 'warehouse'
]

with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    sale_id = 1
    batch_size = 50000
    while os.path.getsize(filename) < TARGET_BYTES:
        batch_rows = []
        for _ in range(batch_size):
            product_name, category, brand, base_price = random.choice(products)
            city, region = random.choice(cities)
            quantity = random.randint(1, 15)
            price = round(base_price * random.uniform(0.9, 1.25), 2)
            discount_pct = round(random.uniform(0.0, 0.35), 4)
            tax_rate = round(random.uniform(0.05, 0.2), 4)
            subtotal = price * quantity
            discounted = subtotal * (1 - discount_pct)
            total_amount = round(discounted * (1 + tax_rate), 2)

            row = {
                'sale_id': sale_id,
                'product_name': product_name,
                'category': category,
                'brand': brand,
                'customer_id': random.randint(1000, 500000),
                'price': f'{price:.2f}',
                'quantity_sold': quantity,
                'discount_pct': f'{discount_pct:.4f}',
                'tax_rate': f'{tax_rate:.4f}',
                'total_amount': f'{total_amount:.2f}',
                'date': random_date(),
                'city': city,
                'region': region,
                'country': 'Saudi Arabia',
                'channel': random.choice(channels),
                'payment_method': random.choice(payment_methods),
                'customer_segment': random.choice(customer_segments),
                'order_status': random.choice(order_statuses),
                'store_id': f'ST-{random.randint(1, 200):04d}',
                'warehouse': random.choice(warehouses),
            }
            batch_rows.append(row)
            sale_id += 1

        writer.writerows(batch_rows)
        csvfile.flush()
        os.fsync(csvfile.fileno())

print(f'Generated sales data to {filename}')
print(f'File size: {os.path.getsize(filename) / (1024 * 1024):.2f} MB')
print(f'Estimated rows: {sale_id - 1}')
