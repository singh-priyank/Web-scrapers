import bs4 as bs
import requests 
import time
import csv

def request(url):
	headers = {
    	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	return requests.get(url,headers=headers)

lis = []
f3= open("1800","w+")
f2= open("1700","w+")
f1= open("1600","w+")
f= open("1500","w+")
for p in range(13):
	url = "https://codeforces.com/problemset/page/{}?tags=1500-1800&order=BY_RATING_DESC".format(p+1)

	try:
   		r = request(url)
	except:
   		print("Error opening the URL")

	source1 = r.text
	soup = bs.BeautifulSoup(source1,'lxml')

	table = soup.table
	table = soup.find('table')

	table_rows = table.findAll('tr')


	for tr in table_rows:
		row = []
		
		td = tr.findAll('td')
		if(len(td)==0): continue
		y = td[0].a.text.split()
		x = td[3].text.split()
		#print(*td[3].text.split())
		#print(x)
		if(x==['1500']):
			f.write("{}\n".format(*y))
			#print(*y)
		elif(x==['1600']):
			f1.write("{}\n".format(*y))
			#print(*y)
		elif(x==['1700']):
			f2.write("{}\n".format(*y))
			print(*y)
		elif(x==['1800']):
			f3.write("{}\n".format(*y))
			#print(*y)

f.close()
f1.close() 
f2.close() 
f3.close() 