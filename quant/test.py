import urllib2 as url
#Used to test values to see what characters correspond to which stock properties
def key(data):
	address='http://finance.yahoo.com/d/quotes.csv?s=goog&f='+data
	return url.urlopen(address).read().strip().strip('"')