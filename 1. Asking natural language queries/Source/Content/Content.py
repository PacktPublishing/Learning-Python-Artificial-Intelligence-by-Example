import sqlite3
from text_cleaning import text_cleaning

class Content:
    def __init__(self, db_file):
        """
        Intialise the crawl_wikipedia class, set up a
        lightweight database for storing content for later use
        :param db_file: string
        """
        self.categories = []
        # Connect to the DB db
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def get_page_urls(self):
        """
        Retrieve a list of urls from the database
        :return: list of urls
        """
        return [row for row in self.cursor.execute("SELECT url FROM content")]

    def get_page_ids(self):
        """
        Retrieve a list of page ids from the database
        :return: list of page id tuples
        """
        return [row for row in self.cursor.execute("SELECT pageid FROM content")]

    def get_page_by_id(self, pageid):
        """
        Retrieve the page with the specified pageid
        Note that this is of the format (pageid, ) for SQLite3 to work, for example
        to get the page with the id of 1 in our database, set pageid to ('1', )
        :pageid: tuple ('id', )
        :return: string
        """
        return str(self.cursor.execute("SELECT content FROM content WHERE pageid=?", pageid).fetchone()).lower()

    def get_page_url_by_id(self, pageid):
        """
        Retrieve the page with the specified pageid
        Note that this is of the format (pageid, ) for SQLite3 to work, for example
        to get the page with the id of 1 in our database, set pageid to ('1', )
        :pageid: tuple ('id', )
        :return: string
        """
        return self.cursor.execute("SELECT url FROM content WHERE pageid=?", pageid).fetchone()

    def __iter__(self):
        """
        Iterator for the document set stored in the database
        This is more efficient memory wise than loading the complete document set into memory
        and therefore will scale well for larger document sets (or those not available on local disk)
        :return: tuple (string, )
        """
        for pageid in self.get_page_ids():
            page = self.get_page_by_id(pageid)
            yield text_cleaning.get_cleaned_text(page).split()