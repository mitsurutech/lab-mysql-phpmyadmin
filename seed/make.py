#!/usr/bin/env python3
"""Writes the shop database's SQL to standard output.

The data is made from a fixed seed, so running this again gives the same rows. The
output is pasted into compose.yaml by seed/splice.py, which is how the lab carries its
data without an image of its own.
"""
import datetime
import random

rng = random.Random(411)

CATEGORIES = [
    ('Books', 'Paperbacks and hardbacks'),
    ('Games', 'Board games and puzzles'),
    ('Garden', 'Tools, seeds and pots'),
    ('Kitchen', 'Cookware and utensils'),
    ('Music', 'Instruments and accessories'),
    ('Outdoors', 'Camping and walking'),
    ('Stationery', 'Paper, pens and notebooks'),
    ('Toys', 'For ages three and up'),
]

SUPPLIERS = [
    ('Northwind Traders', 'Leeds', 'United Kingdom'),
    ('Riverside Crafts', 'Bristol', 'United Kingdom'),
    ('Sakura Goods', 'Osaka', 'Japan'),
    ('Atelier Lumiere', 'Lyon', 'France'),
    ('Casa Verde', 'Valencia', 'Spain'),
    ('Maple Supply Co', 'Toronto', 'Canada'),
]

# name, category (None = not yet sorted), supplier, price, stock, discontinued
PRODUCTS = [
    ('The Little Prince', 'Books', 4, 7.99, 40, 0),
    ('Pride and Prejudice', 'Books', 1, 6.50, 25, 0),
    ('A Short History of Nearly Everything', 'Books', 1, 10.99, 12, 0),
    ('Learn SQL in a Weekend', 'Books', 2, 19.99, 30, 0),
    ('Japanese Cooking at Home', 'Books', 3, 22.00, 8, 0),
    ('Chess Set, Wooden', 'Games', 2, 34.95, 15, 0),
    ('1000-Piece Jigsaw: Harbour', 'Games', 1, 14.99, 22, 0),
    ('Go Board and Stones', 'Games', 3, 49.00, 5, 0),
    ('Card Game: Dragons', 'Games', 6, 12.50, 0, 1),
    ('Trowel', 'Garden', 2, 8.75, 60, 0),
    ('Tomato Seeds', 'Garden', 5, 2.49, 200, 0),
    ('Terracotta Pot, Large', 'Garden', 5, 18.00, 14, 0),
    ('Watering Can', 'Garden', 1, 15.99, 9, 0),
    ('Cast Iron Pan', 'Kitchen', 6, 39.99, 11, 0),
    ('Chef Knife', 'Kitchen', 3, 64.00, 7, 0),
    ('Wooden Spoon Set', 'Kitchen', 2, 9.99, 45, 0),
    ('Teapot', 'Kitchen', 3, 27.50, 0, 0),
    ('Coffee Grinder', 'Kitchen', 4, 45.00, 6, 0),
    ('Ukulele', 'Music', 6, 59.99, 4, 0),
    ('Guitar Strings', 'Music', 6, 7.25, 80, 0),
    ('Harmonica', 'Music', 1, 18.50, 16, 0),
    ('Metronome', 'Music', 4, 24.99, 0, 1),
    ('Tent, Two Person', 'Outdoors', 6, 129.00, 3, 0),
    ('Sleeping Bag', 'Outdoors', 6, 54.99, 10, 0),
    ('Head Torch', 'Outdoors', 1, 16.99, 33, 0),
    ('Water Bottle', 'Outdoors', 5, 11.00, 70, 0),
    ('Walking Poles', 'Outdoors', 2, 42.00, 0, 0),
    ('Fountain Pen', 'Stationery', 3, 28.00, 18, 0),
    ('A5 Notebook', 'Stationery', 4, 5.99, 120, 0),
    ('Coloured Pencils, 24', 'Stationery', 2, 11.49, 50, 0),
    ('Desk Calendar', 'Stationery', 1, 8.00, 0, 1),
    ('Wooden Train Set', 'Toys', 2, 44.99, 6, 0),
    ('Kite', 'Toys', 5, 19.99, 13, 0),
    ('Building Blocks, 100', 'Toys', 4, 24.00, 20, 0),
    ('Spinning Top', 'Toys', 3, 4.50, 90, 0),
    ('Gift Card', None, 1, 25.00, 999, 0),
    ('Mystery Box', None, 2, 30.00, 12, 0),
]

FIRST = ['Amelia', 'Oliver', 'Isla', 'Noah', 'Ava', 'Leo', 'Mia', 'Arthur', 'Sofia',
         'Jack', 'Yuki', 'Haruto', 'Chloe', 'Lucas', 'Ines', 'Mateo', 'Priya', 'Arjun',
         'Fatima', 'Omar', 'Grace', 'Ethan', 'Zara', 'Daniel', 'Emma', 'Hugo', 'Aiko',
         'Lucia', 'Samuel', 'Nadia', 'Tom', 'Ruby', 'Kenji', 'Elena', 'Ben', 'Freya']
LAST = ['Smith', 'Jones', 'Patel', 'Brown', 'Taylor', 'Wilson', 'Tanaka', 'Sato',
        'Martin', 'Bernard', 'Garcia', 'Lopez', 'Khan', 'Evans', "O'Brien", 'Walker',
        'Suzuki', 'Dubois', 'Fernandez', 'Hughes', 'Ali', 'Clarke', 'Murphy', 'Moreau']
PLACES = [('London', 'United Kingdom'), ('Manchester', 'United Kingdom'),
          ('Leeds', 'United Kingdom'), ('Glasgow', 'United Kingdom'),
          ('Cardiff', 'United Kingdom'), ('Belfast', 'United Kingdom'),
          ('Paris', 'France'), ('Lyon', 'France'), ('Tokyo', 'Japan'),
          ('Osaka', 'Japan'), ('Madrid', 'Spain'), ('Seville', 'Spain'),
          ('Dublin', 'Ireland'), ('Toronto', 'Canada')]

EMPLOYEES = [
    # first, last, job, manager (row number), hired, salary
    ('Margaret', 'Hale', 'Managing Director', None, '2015-03-02', 72000),
    ('David', 'Okafor', 'Sales Manager', 1, '2017-06-12', 52000),
    ('Hana', 'Kobayashi', 'Warehouse Manager', 1, '2018-01-08', 48000),
    ('Claire', 'Dupont', 'Sales Assistant', 2, '2020-09-14', 29000),
    ('Rafael', 'Moreno', 'Sales Assistant', 2, '2021-04-19', 28500),
    ('Sian', 'Price', 'Sales Assistant', 2, '2023-02-01', 27000),
    ('George', 'Mills', 'Packer', 3, '2019-11-25', 24500),
    ('Mei', 'Lin', 'Packer', 3, '2022-07-04', 24000),
    ('Patrick', 'Doyle', 'Driver', 3, '2021-10-11', 26000),
    ('Laura', 'Becker', 'Accountant', 1, '2019-05-20', 45000),
]

REVIEW_WORDS = {
    5: ['Exactly as described.', 'Lovely quality, would buy again.', 'Brilliant.',
        'Arrived quickly and well packed.'],
    4: ['Very good, a little pricey.', 'Does the job well.', 'Happy with it.'],
    3: ['It is fine.', 'Smaller than I expected.', 'Average.'],
    2: ['Not great, it broke after a month.', 'Took a long time to arrive.'],
    1: ['Arrived damaged.', 'Not what the picture showed.'],
}


def q(value):
    if value is None:
        return 'NULL'
    if isinstance(value, (int, float)):
        return f'{value:.2f}' if isinstance(value, float) else str(value)
    return "'" + str(value).replace("'", "''") + "'"


def rows(table, columns, values):
    out = [f'INSERT INTO {table} ({", ".join(columns)}) VALUES']
    out.append(',\n'.join('  (' + ', '.join(q(v) for v in row) + ')' for row in values) + ';')
    return '\n'.join(out)


def main():
    out = ['USE shop;', '', SCHEMA.strip(), '']
    out.append(rows('categories', ['name', 'description'], CATEGORIES))
    out.append(rows('suppliers', ['name', 'city', 'country'], SUPPLIERS))
    category_ids = {name: i + 1 for i, (name, _) in enumerate(CATEGORIES)}
    out.append(rows('products', ['name', 'category_id', 'supplier_id', 'price', 'stock',
                                 'discontinued'],
                    [(n, category_ids.get(c), s, p, st, d) for n, c, s, p, st, d in PRODUCTS]))
    out.append(rows('employees', ['first_name', 'last_name', 'job_title', 'manager_id',
                                  'hired_on', 'salary'], EMPLOYEES))

    customers, seen = [], set()
    while len(customers) < 40:
        first, last = rng.choice(FIRST), rng.choice(LAST)
        if (first, last) in seen:
            continue
        seen.add((first, last))
        city, country = rng.choice(PLACES)
        email = f"{first}.{last}".lower().replace("'", '') + '@example.com'
        phone = None if rng.random() < 0.25 else f'0{rng.randint(1000, 9999)} {rng.randint(100000, 999999)}'
        joined = datetime.date(2023, 1, 1) + datetime.timedelta(days=rng.randint(0, 700))
        customers.append((first, last, email, phone, city, country, joined.isoformat()))
    out.append(rows('customers', ['first_name', 'last_name', 'email', 'phone', 'city',
                                  'country', 'joined_on'], customers))

    # Customers 37 to 40 never order, and the last few products are never ordered, so a
    # LEFT JOIN has something to find.
    orderable = [i + 1 for i, p in enumerate(PRODUCTS) if not p[5]][:-3]
    orders, items = [], []
    # Every one of the first 36 orders at least once, the rest more than once.
    buyers = list(range(1, 37)) + [rng.randint(1, 36) for _ in range(120 - 36)]
    rng.shuffle(buyers)
    for order_id, customer in enumerate(buyers, start=1):
        joined = datetime.date.fromisoformat(customers[customer - 1][6])
        when = datetime.datetime.combine(joined, datetime.time(8)) + datetime.timedelta(
            days=rng.randint(0, 400), minutes=rng.randint(0, 13 * 60))
        status = rng.choices(['delivered', 'shipped', 'pending', 'cancelled'],
                             [70, 12, 10, 8])[0]
        employee = rng.choice([4, 5, 6, 2])
        shipped = None if status in ('pending', 'cancelled') else \
            (when + datetime.timedelta(days=rng.randint(1, 5))).date().isoformat()
        orders.append((customer, employee, when.strftime('%Y-%m-%d %H:%M:00'), status, shipped))
        for product in rng.sample(orderable, rng.choices([1, 2, 3, 4], [35, 35, 20, 10])[0]):
            items.append((order_id, product, rng.choices([1, 2, 3, 5], [60, 25, 10, 5])[0],
                          PRODUCTS[product - 1][3]))
    out.append(rows('orders', ['customer_id', 'employee_id', 'ordered_at', 'status',
                               'shipped_on'], orders))
    out.append(rows('order_items', ['order_id', 'product_id', 'quantity', 'unit_price'], items))

    reviews, reviewed = [], set()
    for order_id, product, _, _ in items:
        if len(reviews) >= 60 or rng.random() > 0.3:
            continue
        customer, _, when, status, _ = orders[order_id - 1]
        if status != 'delivered' or (customer, product) in reviewed:
            continue
        reviewed.add((customer, product))
        stars = rng.choices([5, 4, 3, 2, 1], [40, 30, 15, 10, 5])[0]
        words = None if rng.random() < 0.2 else rng.choice(REVIEW_WORDS[stars])
        day = (datetime.datetime.fromisoformat(when) + datetime.timedelta(days=rng.randint(4, 30)))
        reviews.append((product, customer, stars, words, day.date().isoformat()))
    out.append(rows('reviews', ['product_id', 'customer_id', 'stars', 'comment',
                                'reviewed_on'], reviews))
    print('\n\n'.join(out))


SCHEMA = """
CREATE TABLE categories (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(40) NOT NULL UNIQUE,
  description VARCHAR(200)
);
CREATE TABLE suppliers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(80) NOT NULL,
  city VARCHAR(60) NOT NULL,
  country VARCHAR(60) NOT NULL
);
CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  category_id INT NULL,
  supplier_id INT NOT NULL,
  price DECIMAL(8,2) NOT NULL CHECK (price >= 0),
  stock INT NOT NULL DEFAULT 0,
  discontinued BOOLEAN NOT NULL DEFAULT FALSE,
  FOREIGN KEY (category_id) REFERENCES categories(id),
  FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
CREATE TABLE employees (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  job_title VARCHAR(60) NOT NULL,
  manager_id INT NULL,
  hired_on DATE NOT NULL,
  salary INT NOT NULL,
  FOREIGN KEY (manager_id) REFERENCES employees(id)
);
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(40) NOT NULL,
  last_name VARCHAR(40) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  phone VARCHAR(20) NULL,
  city VARCHAR(60) NOT NULL,
  country VARCHAR(60) NOT NULL,
  joined_on DATE NOT NULL
);
CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT NOT NULL,
  employee_id INT NOT NULL,
  ordered_at DATETIME NOT NULL,
  status ENUM('pending', 'shipped', 'delivered', 'cancelled') NOT NULL,
  shipped_on DATE NULL,
  FOREIGN KEY (customer_id) REFERENCES customers(id),
  FOREIGN KEY (employee_id) REFERENCES employees(id)
);
CREATE TABLE order_items (
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL CHECK (quantity > 0),
  unit_price DECIMAL(8,2) NOT NULL,
  PRIMARY KEY (order_id, product_id),
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (product_id) REFERENCES products(id)
);
CREATE TABLE reviews (
  id INT AUTO_INCREMENT PRIMARY KEY,
  product_id INT NOT NULL,
  customer_id INT NOT NULL,
  stars TINYINT NOT NULL CHECK (stars BETWEEN 1 AND 5),
  comment VARCHAR(200) NULL,
  reviewed_on DATE NOT NULL,
  UNIQUE (product_id, customer_id),
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (customer_id) REFERENCES customers(id)
);
"""

if __name__ == '__main__':
    main()
