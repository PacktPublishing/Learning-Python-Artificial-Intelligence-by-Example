"""
Download content for a specified category on Wikipedia into a local database
This text corpus will be used for topic modelling
"""

import sqlite3
import wptools
import re
from bs4 import BeautifulSoup


class CrawlWikipedia:
    def __init__(self, db_file):
        """
        Intialise the crawl_wikipedia class, set up a
        lightweight database for storing content for later use
        :param db_file:
        """
        self.categories = []
        # Create db
        self.conn = sqlite3.connect(db_file)
        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS content \
            (pageid text, category text, url text, content text)')
        self.conn.commit()
        self.cursor = self.conn.cursor()

    def _save_page_content(self, category, pageid, url, content):
        self.cursor.execute('INSERT INTO content VALUES (?, ?, ?, ?)', (pageid, category, url, content))
        self.conn.commit()

    def get_page_urls(self):
        """
        Retrieve a list of urls from the database
        :return: list of urls
        """
        return [url for url in self.cursor.execute('SELECT url FROM content')]

    def get_page_ids(self):
        """
        Retrieve a list of page ids from the database
        :return: list of page ids
        """
        return [pageid for pageid in self.cursor.execute('SELECT pageid FROM content')]

    def get_categories_and_members(self, category, depth):
        """
        Start with the defined category and download Wikipedia content
        up to the specific depth of categories
        :param category:
        :param depth:
        :return:
        """
        print(u'Checking for subcategories of {} at depth {}'.format(category, depth))
        if depth:
            # Get details of this category
            # Members are pages related to this category
            cat = wptools.category(category)
            cat_members = cat.get_members()

            # First let's save any members (pages) for this category
            if 'members' in cat_members.data.keys():
                for cat_member in cat_members.data['members']:
                    # Check to see if we have this page already, ignore if we do
                    if cat_member['pageid'] not in self.get_page_ids():

                        # If we don't have this page, then get the page content
                        page = wptools.page(pageid=cat_member['pageid']).get_parse()

                        # Get URL in wikipedia
                        url = page.get_query().data['url']

                        # Remove <ref> and other HTML syntax
                        text = BeautifulSoup(page.data['wikitext'], 'html.parser').get_text()

                        # Remove other markup such as [[...]] and {{...}}
                        clean_content = re.sub(r'\s*{.*}\s*|\s*\[.*\]\s*', '', text)

                        # Now store
                        print('Saving pageid {} / url {}'.format(cat_member['pageid'], url))
                        self._save_page_content(category, cat_member['pageid'], url, clean_content)

            # Now iterate through any subcategories
            if 'subcategories' in cat_members.data.keys():
                subcats = cat_members.data['subcategories']
                for subcat in subcats:
                    self.categories.append(subcat)

                    # Recursively call this function until we've explored Wikipedia up to the specified depth
                    self.get_categories_and_members(subcat['title'], depth - 1)
