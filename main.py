"""
PIPELINE

Sitemaps
1)  Add the domains and names
2)  Run the sitemap indexer -> creates a csv with all the links in the sitemaps directory

Crawl
1)  Create a date parser for the specific newspaper
2)  Run find_pages_in_daterange() -> finds all pages with articles in the specified date range
3)  Save the list as a serialized pickle file in the crawled-pages directory with save_crawled_pages()

Parser
1)  Define the target words
2)  Create a text parser for the specific newspaper
3)  Load the serialized pages from the crawled-pages directory
4)  Parse every page
5)  Merge the output per day
6)  Safe the merged results in the results directory
"""
from parsers.run_20min import parse_20min

parse_20min()
