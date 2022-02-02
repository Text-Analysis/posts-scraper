import psycopg2

from posts_scraper.configs import DATABASE


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(user=DATABASE['USER'], password=DATABASE['PASSWORD'])
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()
        self.cur.close()
