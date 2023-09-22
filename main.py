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
6)  Safe the merged parser-results in the parser-results directory


NEW:
1) Create a text parser for the specific newspaper
2) Parse crawled pages and safe them one after the other to the crawler-parser-results directory (unsorted and unmerged)
3) Sort and merge the crawler parser-results and safe them to the parser-results directory
4) Visualize and save the png to the plots directory

"""
from parsers.run_solothurner_zeitung import parse_solothurner_zeitung

parse_solothurner_zeitung()
