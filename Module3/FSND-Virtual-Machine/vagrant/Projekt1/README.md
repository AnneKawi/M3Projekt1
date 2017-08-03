# Reporting Tool

This repository writes a small report on an news database.
1. It filters and lists the three most-read articles with their view-count.
2. It sorts and lists the authors according to their total view-count.
3. Finds and lists the days, where more than 1% of the requests on the website led to errors.

## Prerequisites
- python3
- psycopg2

## Usage
Download the repository and run M3Projekt1.py. The results are written into the Terminal.
The M3P1Results.txt-File shows the results according to the training-database.


## the database tables this program tailored to
database: news
tables:
- articles
    author | integer                  | not null
    title  | text                     | not null
    slug   | text                     | not null
    lead   | text                     |
    body   | text                     |
    time   | timestamp with time zone | default now()
    id     | integer                  | not null default nextval('articles_id_seq'::regclass)
    Indexes:
        "articles_pkey" PRIMARY KEY, btree (id)
        "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
    Foreign-key constraints:
        "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

- authors
     name   | text    | not null
     bio    | text    |
     id     | integer | not null default nextval('authors_id_seq'::regclass)
    Indexes:
        "authors_pkey" PRIMARY KEY, btree (id)
    Referenced by:
        TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)

- log
     path   | text                     |
     ip     | inet                     |
     method | text                     |
     status | text                     |
     time   | timestamp with time zone | default now()
     id     | integer                  | not null default nextval('log_id_seq'::regclass)
    Indexes:
        "log_pkey" PRIMARY KEY, btree (id)
