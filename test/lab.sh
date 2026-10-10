#!/usr/bin/env bash
# What the README promises, checked from inside the lab's own network: run by check.sh.
set -euo pipefail
: "${NET:?run through test/check.sh}" "${PROJECT:?}"
# The README's first step, as a student takes it, in every probe.
probe() { docker run --rm --network "$NET" lab-check-probe \
  sh -c 'printf "[client]\nssl-verify-server-cert=0\n" > ~/.my.cnf; exec "$@"' sh "$@"; }

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
  | grep -q 'fruit' || { echo "phpMyAdmin did not list shop.fruit" >&2; exit 1; }

echo "- what is saved fits under the platform's 200 MB"
size=$(docker run --rm -v "${PROJECT}_mysqldata:/v:ro" alpine:3.21 du -sm /v | cut -f1)
echo "  mysqldata is ${size} MB"
[ "$size" -lt 150 ] || { echo "mysqldata is ${size} MB, too close to 200" >&2; exit 1; }
