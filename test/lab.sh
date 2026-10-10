#!/usr/bin/env bash
# What the README promises, checked from inside the lab's own network: run by check.sh.
set -euo pipefail
: "${NET:?run through test/check.sh}" "${PROJECT:?}"
# The README's first step, as a student takes it, in every probe.
probe() { docker run --rm --network "$NET" lab-check-probe \
  sh -c 'printf "[client]\nssl-verify-server-cert=0\n" > ~/.my.cnf; exec "$@"' sh "$@"; }

echo "- the shop database is there, every table filled"
counts=$(probe mariadb -h db -u student -pstudent shop -N -e "
  SELECT 'categories', COUNT(*) FROM categories UNION ALL SELECT 'suppliers', COUNT(*) FROM suppliers
  UNION ALL SELECT 'products', COUNT(*) FROM products UNION ALL SELECT 'employees', COUNT(*) FROM employees
  UNION ALL SELECT 'customers', COUNT(*) FROM customers UNION ALL SELECT 'orders', COUNT(*) FROM orders
  UNION ALL SELECT 'order_items', COUNT(*) FROM order_items UNION ALL SELECT 'reviews', COUNT(*) FROM reviews")
echo "$counts" | sed 's/^/  /'
diff <(echo "$counts" | tr '\t' ' ') - <<'COUNTS' || { echo "the shop database is not what seed/make.py writes" >&2; exit 1; }
categories 8
suppliers 6
products 37
employees 10
customers 40
orders 120
order_items 250
reviews 46
COUNTS

echo "- with the gaps the README's lessons find"
# Four customers who never ordered (LEFT JOIN), two products with no category (NULL),
# and one employee with no manager (the self-join's top).
probe mariadb -h db -u student -pstudent shop -N -e "
  SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.customer_id = c.id WHERE o.id IS NULL" | grep -qx 4 \
  || { echo "expected four customers with no orders" >&2; exit 1; }
probe mariadb -h db -u student -pstudent shop -N -e "SELECT COUNT(*) FROM products WHERE category_id IS NULL" | grep -qx 2 \
  || { echo "expected two products with no category" >&2; exit 1; }
probe mariadb -h db -u student -pstudent shop -N -e "
  SELECT e.first_name FROM employees e LEFT JOIN employees m ON m.id = e.manager_id WHERE m.id IS NULL" | grep -qx Margaret \
  || { echo "expected Margaret alone at the top" >&2; exit 1; }

echo "- the terminal's client signs in and writes a table"
probe mariadb -h db -u student -pstudent shop -e \
  "CREATE TABLE fruit (id INT PRIMARY KEY, name VARCHAR(40)); INSERT INTO fruit VALUES (1,'apple'),(2,'pear');"
probe mariadb -h db -u student -pstudent shop -N -e "SELECT COUNT(*) FROM fruit" | grep -qx 2
probe mariadb -h db -u student -pstudent -N -e "SHOW STATUS LIKE 'Ssl_cipher'" | grep -q 'TLS\|AES\|CHACHA' \
  || { echo "the terminal's connection is not encrypted" >&2; exit 1; }

echo "- the student owns shop and student_*, and nothing else; root may do more"
probe mariadb -h db -u student -pstudent -e "CREATE DATABASE student_mine; CREATE TABLE student_mine.t (id INT); DROP DATABASE student_mine"
if probe mariadb -h db -u student -pstudent -e "CREATE DATABASE other" 2>/dev/null; then
  echo "student could create a database outside student_*" >&2; exit 1; fi
probe mariadb -h db -u root -proot -N -e "SHOW DATABASES" | grep -qx shop

echo "- a backup restores"
probe sh -c 'mariadb-dump -h db -u student -pstudent --no-tablespaces shop > /tmp/s.sql \
  && mariadb -h db -u student -pstudent shop -e "DROP TABLE fruit" \
  && mariadb -h db -u student -pstudent shop < /tmp/s.sql'
probe mariadb -h db -u student -pstudent shop -N -e "SELECT COUNT(*) FROM fruit" | grep -qx 2

echo "- phpMyAdmin opens already signed in"
page=$(probe curl -fsS -c /tmp/j -b /tmp/j http://phpmyadmin:8080/)
if grep -q 'name="pma_username"' <<<"$page"; then echo "phpMyAdmin showed a login form" >&2; exit 1; fi

echo "- and offers to create a database"
probe bash -c 'curl -fsS -c /tmp/j -b /tmp/j http://phpmyadmin:8080/ >/dev/null
  curl -fsS -c /tmp/j -b /tmp/j "http://phpmyadmin:8080/index.php?route=/server/databases"' > /tmp/pma-dbs.html
if grep -q 'No privileges' /tmp/pma-dbs.html; then echo "phpMyAdmin says No privileges" >&2; exit 1; fi
grep -q 'name="new_db"' /tmp/pma-dbs.html || { echo "phpMyAdmin has no Create database form" >&2; exit 1; }

echo "- and shows the table written from the terminal"
probe bash -c 'curl -fsS -c /tmp/j -b /tmp/j http://phpmyadmin:8080/ >/dev/null
  curl -fsS -c /tmp/j -b /tmp/j "http://phpmyadmin:8080/index.php?route=/database/structure&db=shop"' \
  > /tmp/pma-shop.html
for table in fruit customers orders order_items products reviews; do
  grep -q "$table" /tmp/pma-shop.html || { echo "phpMyAdmin did not list shop.$table" >&2; exit 1; }
done

echo "- what is saved fits under the platform's 200 MB"
size=$(docker run --rm -v "${PROJECT}_mysqldata:/v:ro" alpine:3.21 du -sm /v | cut -f1)
echo "  mysqldata is ${size} MB"
[ "$size" -lt 150 ] || { echo "mysqldata is ${size} MB, too close to 200" >&2; exit 1; }
