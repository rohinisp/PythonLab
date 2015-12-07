# Assumes DB Drivers are installed correctly

import json
import requests
import pyodbc
from bs4 import BeautifulSoup
from random import shuffle


# SQL Server Example
# db007 = {
#     "Driver": "{SQL Server}",
#     "Server": "server.domain.site.com",
#     "Database": "DatabaseName",
#     "Trusted_Connection": "yes"
# }

#MySQL example -- requires listed driver to be installed
# data001 = {
#     "Driver": "{MySQL ODBC 5.3 Unicode Driver}",
#     "Server": "server.domain.site.com'",
#     "Database": "databasename",
#     "UID": "uid",
#     "PASSWORD": "password"
# }

# Local SQL Server example
db007 = {
    "Driver": "{SQL Server}",
    "Server": "localhost",
    "Database": "DatabaseName",
    "Trusted_Connection": "yes"
}


def get_market_list():
	""" Query a database for a set of URLs and return those in a randomly sorted list """
	#Establish a database connection and create a cursor
	db_connection = pyodbc.connect(**db007)
	db_cursor = db_connection.cursor()

	# Make a list and fill it with URIs from a database table
	markets = []
	for row in db_cursor.execute("select uri from dbo.URIList where status = 0"):
		market = row.uri
		markets.append(market)

	# Randomly sort that list before returning it
	shuffle(markets)
	db_connection.close()

	return(markets)




def get_web_page(market):
	""" For a single market, scrape the HTML, removing all javascript and style elements. Returns all the visible text on the web page """
	r = requests.get(market)

	soup = BeautifulSoup(r.content.decode("utf-8"))
	for i in soup.find_all(['script', 'style', 'a']):
		i.extract()

	htmltext = soup.get_text().replace('\n','\n\n')

	return(htmltext)




# Get list of all URLs we want to scrape
markets = get_market_list()

# Open a persistent DB connection
db_connection = pyodbc.connect(**db007)
db_cursor = db_connection.cursor()

# For each URL in the list of markets, retrieve the text contents and write to a database
for market in markets:
	htmltext = get_web_page(market)
	print(market)
	db_cursor.execute("update dbo.URIList set status = 1, htmltext = ? where uri = ?", htmltext, market)
	db_cursor.commit()

db_cursor.close()