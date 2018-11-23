"""
Learning Python AI by Example: Asking Natural Language Queries

Using Wikipedia Artificial Intelligence content to create a model
that we can query using natural language to get rich information
and responses from.


"""

# Imports
from Crawler.CrawlWikipedia import CrawlWikipedia

# Configuration:
# Start with the top level Artificial Intelligence category on Wikipedia
category = 'Category:Artificial_intelligence'

# Process 2 levels in subcategories
# Note that a depth of 1 provides circa 280 pages which is sufficient for dev / test purposes
# and is quicker than depth=2 which has significantly more Wikipedia pages in scope
depth = 2

# Set up a simple database so we can use this data later
crawler = CrawlWikipedia('data/content.db')

# Now use the Wikipedia API to populate our database
crawler.get_categories_and_members(category, depth)



