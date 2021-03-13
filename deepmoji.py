import requests
import bs4 as bs

def request(url):
	headers = {
    	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	return requests.get(url,headers=headers)

s = input()


url = 'https://deepmoji.mit.edu/api/?q='+s
r = request(url)

source1 = r.text
soup = bs.BeautifulSoup(source1,'lxml')

print(soup)

