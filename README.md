# MySQL and phpMyAdmin with Docker Compose: a lab and sample database for teaching SQL

[![check](https://github.com/mitsurutech/lab-mysql-phpmyadmin/actions/workflows/check.yml/badge.svg)](https://github.com/mitsurutech/lab-mysql-phpmyadmin/actions/workflows/check.yml)

A ready-made **MySQL + phpMyAdmin** lab for classrooms, from the
[MitsuruTech Learning Platform](https://mitsurutech.co.uk/learning), where schools and
colleges give every student their own databases, containers and terminal in the browser.
Each student gets their own [MySQL](https://dev.mysql.com/doc/refman/8.4/en/) server and
their own [phpMyAdmin](https://www.phpmyadmin.net), already signed in, so the same tables
can be changed with SQL in a terminal and looked at in a browser. The terminal beside them
has MariaDB's `mariadb` client and `curl`.

It starts with **a sample database to practise SQL on**, `shop`: a small online shop's
customers, products, orders and reviews, a few hundred rows in eight tables, with
[exercises below](#sql-exercises) from a first `SELECT` to self-joins and subqueries.
On the platform it comes free with every account, as the lab in the **Database (Sample)**
module and on the Container tab of a personal account.

It is one `docker-compose` file, `compose.yaml`, and it runs the same on your own machine:
add `ports: ["8080:8080"]` to `phpmyadmin`, run `docker compose up` and open
<http://localhost:8080>. On the platform nothing is published on the machine and the lab's
page gives the link instead.

## Using it on the platform

Make a task of type **Lab**, choose **In a GitHub repository** and give
`https://github.com/mitsurutech/lab-mysql-phpmyadmin` with the branch `main`; the compose
file is the default, `compose.yaml`. Fork it first to change it. Publish, and every
student's copy starts from the commit you published. The help manual's
[guide to container labs](https://mitsurutech.co.uk/help/labs) covers the rest: what a
compose file may say, how much memory a copy gets, and how teachers watch and take over a
student's terminal.

No college account yet? [Your first year is free](https://mitsurutech.co.uk/pricing) for up
to 50 students, and [signing up](https://mitsurutech.co.uk/signup) takes an email address.

## The lesson it was written for

Students who have not used a shell before can start with the
[Linux terminal guide](https://mitsurutech.co.uk/help/linux-terminal).

1. **Open phpMyAdmin.** On the lab's page, under **In your browser**, press
   **phpMyAdmin**. It opens signed in. Choose `shop` on the left to see its eight tables,
   and **Browse** any of them.

2. **Talk to the database by name** from the lab's terminal. The terminal's client is
   MariaDB's, and MySQL signs its own TLS certificate, which a client rightly refuses to
   trust until told to. Tell it once; your home folder is saved, so it stays told:

   ```
   printf '[client]\nssl-verify-server-cert=0\n' > ~/.my.cnf
   mariadb -h db -u student -pstudent shop
   ```

   The connection is still encrypted, `SHOW STATUS LIKE 'Ssl_cipher';` says with what. What
   is skipped is checking *who* is at the other end, which inside a lab's own network is
   nobody else; in production a server's certificate is signed by somebody the client trusts.

   Make a table and put something in it:

   ```sql
   CREATE TABLE fruit (id INT PRIMARY KEY, name VARCHAR(40) NOT NULL);
   INSERT INTO fruit VALUES (1, 'apple'), (2, 'pear');
   ```

   Reload phpMyAdmin and `fruit` is there, with both rows under **Browse**. Add a row in
   phpMyAdmin and `SELECT * FROM fruit;` shows it in the terminal: the two are clients of
   one server.

3. **See who you are.** phpMyAdmin signs in as `student`, who owns `shop` and any database
   whose name starts `student_`, and nothing else. `CREATE DATABASE student_notes;` works,
   in the terminal or under phpMyAdmin's **Databases**; `CREATE DATABASE other;` is refused.
   `SHOW GRANTS;` says why. Sign in as `root` (password `root`) and nothing is refused:

   ```
   mariadb -h db -u root -proot -e 'SHOW DATABASES'
   ```

4. **See what lasts.** Stop the lab and start it again. `fruit` is still there, because
   MySQL keeps its files in the named volume `mysqldata`, and that is what the platform
   saves. Anything written outside a volume goes when a container stops, which is how
   containers behave in production too.

5. **Back it up and restore it.**

   ```
   mariadb-dump -h db -u student -pstudent --no-tablespaces shop > ~/shop.sql
   mariadb -h db -u student -pstudent shop -e 'DROP TABLE fruit'
   mariadb -h db -u student -pstudent shop < ~/shop.sql
   ```

   Your home folder is saved too, so `~/shop.sql` is still there next time.

## The shop database

| Table | Rows | What is in it |
| --- | --- | --- |
| `categories` | 8 | Books, Games, Garden, Kitchen, Music, Outdoors, Stationery, Toys |
| `suppliers` | 6 | who supplies each product, and from where |
| `products` | 37 | name, price, stock, `discontinued`; two have no category yet |
| `customers` | 40 | name, email, city, country, when they joined; some have no phone |
| `employees` | 10 | job titles and `manager_id`, which points back at `employees` |
| `orders` | 120 | who ordered, which employee took it, when, `status`, when it shipped |
| `order_items` | 250 | what each order held: product, quantity and the price paid |
| `reviews` | 46 | one to five stars, sometimes with a comment |

Every table has its keys and foreign keys, so phpMyAdmin's **Designer** (under **More**
on the database's page) draws how they connect. The data was written so the lessons have
something to find: four customers have never ordered, six products have never been sold,
some phones and comments are `NULL`, and one employee has no manager.

`seed/make.py` writes the data from a fixed seed and `seed/splice.py` puts it into
`compose.yaml`, which carries it as SQL the image runs the first time it starts: a lab's
compose file may not mount a file of its own. Change `make.py` and run `splice.py` rather
than editing `compose.yaml` by hand. The SQL runs only into an empty volume, so on your
own machine `docker compose down -v` starts the data over.

## SQL exercises

Each can be answered in the terminal or in phpMyAdmin's **SQL** tab. Answers are left to
you; the first two say what to expect.

1. Every product over £50, dearest first. *(Four: the tent is £129.)*
2. How many customers there are in each country, most first. *(The United Kingdom has 14.)*
3. The products with nothing in stock, and which of those are discontinued.
4. Each order's total: `SUM(quantity * unit_price)` from `order_items`, grouped by order.
5. Takings per category, leaving out cancelled orders: three tables joined.
6. The customers who have never ordered. A plain `JOIN` cannot find them; a `LEFT JOIN`
   and `IS NULL` can.
7. The products never sold, the same way round from `order_items`.
8. Products with at least three reviews and their average stars, best first: `GROUP BY`
   with `HAVING`.
9. Every employee beside their manager's name: `employees` joined to itself.
10. Products dearer than the average product: a subquery.
11. Orders per month, for a chart: `YEAR(ordered_at)` and `MONTH(ordered_at)`.
12. Make a view, `order_totals`, from exercise 4, and find the biggest order through it.
13. In a transaction, mark every `pending` order `cancelled`, look, then `ROLLBACK` and
    look again.

## What the file shows

| In `compose.yaml` | Why it is there |
| --- | --- |
| `volumes: mysqldata` | the only part of `db` that lasts |
| `entrypoint` on `db` | writes the `shop` database and lets `student` make databases named `student_…`, then starts MySQL sized for a lab, see below |
| `healthcheck` on `db` | so phpMyAdmin starts once MySQL answers, not merely once it has started |
| `depends_on: condition: service_healthy` | the other half of that |
| `PMA_HOST`, `PMA_USER`, `PMA_PASSWORD` | which server phpMyAdmin talks to, and who it signs in as, so there is no login form |
| `APACHE_PORT: "8080"` and `expose` | phpMyAdmin's port, inside the lab's network; nothing is published on the machine |
| `deploy.resources.limits.memory` | each service's share of the memory one copy may have |
| `labels: lab.title` | what the lab's page calls each service |
| `labels: lab.open` | a port the lab's page links to, so it opens in a browser |

### MySQL, sized for a lab

A lab's volumes are saved only while they total under 200 MB, and MySQL's own defaults
would use most of that before any data went in. So the redo log is 8 MB rather than 100,
the buffer pool is 64 MB, and there is no binary log or performance schema. An empty
database is then about 115 MB on disk, most of it files MySQL makes at a fixed size, which
leaves about 85 MB for a student's own data.

`mysql_native_password` is switched back on because MariaDB's client has no plugin for
MySQL 8.4's default sign-in method, `caching_sha2_password`. The connection is TLS either
way; on a server of your own, keep the default and use MySQL's own client.

## How it is checked

On every push, `seed/splice.py --check` fails if `compose.yaml` does not carry exactly
what `seed/make.py` writes, and `test/check.sh` starts the lab the way the platform's runner does: every
capability dropped but the few an image's own entrypoint needs as root, no new privileges,
256 processes, a memory limit with no swap, and a network with no way out. Then
`test/lab.sh` checks every table of `shop` holds what `seed/make.py` wrote and the gaps
the exercises find are there, takes the lesson's steps from inside that network with the
same clients the platform's terminal has, checks phpMyAdmin opens signed in and shows the
tables, measures
the saved volume, and removes the containers and starts them again to see the table kept.

```
test/check.sh
```

## More labs

- [lab-git-gitea](https://github.com/mitsurutech/lab-git-gitea): Git and Gitea, to clone,
  commit and push to a Git server of your own and see it in the web interface.
- [lab-sample](https://github.com/mitsurutech/lab-sample): Postgres, with PostgREST turning
  its tables into a web API.

## About

Made by [Mitsuru Technologies](https://mitsurutech.co.uk) for the
[MitsuruTech Learning Platform](https://mitsurutech.co.uk/learning): Python, Java, Go,
Node, SQL and Linux in the browser for schools and colleges, with container labs, web apps
deployed from GitHub, AWS's S3, DynamoDB and SQS with no AWS account, and quizzes that mark
themselves. Try code with no account in the
[playground](https://mitsurutech.co.uk/playground).

## Licence

MIT. Copy it, change it, teach with it.
