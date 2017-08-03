#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import psycopg2

# 1. What are the most popular three articles of all time?
    # Which articles have been accessed the most?
    # Present this information as a sorted list with the most popular
    # article at the top.

    # Example:
        # "Princess Shellfish Marries Prince Handsome" — 1201 views
        # "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
        # "Political Scandal Ends In Political Scandal" — 553 views


def mostPopularArticles():
    """Print the three most popular articles of all times."""
    print ("1. What are the most popular three articles of all time?")

    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = '''select articles.title, logs.anz \
               from articles, \
                    (select right(path, -9) as slug, count(*) as anz \
                     from log \
                     where status like '%200%' and path like '%/article/%' \
                     group by path \
                     order by anz desc \
                     limit 3) as logs \
               where articles.slug = logs.slug \
               order by logs.anz desc;'''
    c.execute(query)
    articles = c.fetchall()
    db.close()
    for article in articles:
        print ('\t"{0}" - {1} views'.format(article[0], article[1]))

    print ('\n')
    return
mostPopularArticles()


# 2. Who are the most popular article authors of all time?
    # That is, when you sum up all of the articles each author has
    # written, which authors get the most page views?
    # Present this as a sorted list with the most popular author at the
    # top.

    # Example:
        # Ursula La Multa — 2304 views
        # Rudolf von Treppenwitz — 1985 views
        # Markoff Chaney — 1723 views
        # Anonymous Contributor — 1023 views

def mostPopularAuthors():
    """Print the three most popular article authors of all times."""
    print ("2. Who are the most popular article authors of all time?")

    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = '''select authors.name, artviews.gesamt \
               from authors, \
                   (select articles.author as author, sum(logs.anz) as gesamt \
                    from articles, \
                        (select right(path, -9) as slug, count(*) as anz \
                         from log \
                         where status like '%200%'
                               and path like '%/article/%' \
                         group by path \
                         order by anz desc) as logs \
                    where articles.slug = logs.slug \
                    group by articles.author) as artviews \
                where authors.id = artviews.author \
                order by artviews.gesamt desc;'''

    c.execute(query)
    articles = c.fetchall()
    db.close()

    for article in articles:
        print ('\t"{0}" - {1} views'.format(article[0], article[1]))

    print ('\n')
    return
mostPopularAuthors()


# 3. On which days did more than 1% of requests lead to errors?
    # The log table includes a column status that indicates the
    # HTTP status code that the news site sent to the user's browser.

    # Example:

        # July 29, 2016 — 2.5% errors

def highErrorDays():
    """Print the days on which more than 1% of the requests lead to errors."""
    print ("3. On which days did more than 1% of requests lead to errors?")

    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    query = '''select alllogs.day as aday, outs.out, alllogs.gesamt, \
                      ((outs.out * 1000) / alllogs.gesamt) as prom \
               from (select count(*) as gesamt, \
                            date_trunc('day', time) as day from log \
                     group by day) as alllogs, \
                    (select status, count(*) as out, \
                            date_trunc('day', time) as day from log \
                     where status not like '%200%' \
                     group by day, status ) as outs \
                where alllogs.day = outs.day \
                      and ((outs.out * 1000) / alllogs.gesamt) > 10 \
                order by aday;'''
    c.execute(query)
    articles = c.fetchall()
    db.close()

    for article in articles:
        print ('\t{:%B %d, %Y} - {:.1%}'.format(article[0],
                                                float(article[1]) /
                                                float(article[2])))

    print ('\n')
    return
highErrorDays()

