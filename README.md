# MySQL and phpMyAdmin with Docker Compose: a lab for teaching SQL

[![check](https://github.com/mitsurutech/lab-mysql-phpmyadmin/actions/workflows/check.yml/badge.svg)](https://github.com/mitsurutech/lab-mysql-phpmyadmin/actions/workflows/check.yml)

A ready-made **MySQL + phpMyAdmin** lab for classrooms, from the
[MitsuruTech Learning Platform](https://mitsurutech.co.uk/learning), where schools and
colleges give every student their own databases, containers and terminal in the browser.
Each student gets their own [MySQL](https://dev.mysql.com/doc/refman/8.4/en/) server and
their own [phpMyAdmin](https://www.phpmyadmin.net), already signed in, so the same tables
can be changed with SQL in a terminal and looked at in a browser. The terminal beside them
has MariaDB's `mariadb` client and `curl`.

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
   **phpMyAdmin**. It opens signed in, on the database `shop`, which is empty.

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

3. **See who you are.** phpMyAdmin signs in as `student`, who owns `shop` and nothing else.
   Try `CREATE DATABASE other;` and it is refused. Sign in as `root` (password `root`) and
   it is not:

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

## What the file shows

| In `compose.yaml` | Why it is there |
| --- | --- |
| `volumes: mysqldata` | the only part of `db` that lasts |
| `command` on `db` | MySQL sized for a lab, see below |
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

On every push, `test/check.sh` starts the lab the way the platform's runner does: every
capability dropped but the few an image's own entrypoint needs as root, no new privileges,
256 processes, a memory limit with no swap, and a network with no way out. Then
`test/lab.sh` takes the lesson's steps from inside that network with the same clients the
platform's terminal has, checks phpMyAdmin opens signed in and shows the table, measures
the saved volume, and removes the containers and starts them again to see the table kept.

```
test/check.sh
```

## More labs

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
