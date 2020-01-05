import bs4 as bs
import requests

def request(url):
	headers = {
    	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	return requests.get(url,headers=headers)


print("-------------------CODEFORCES------------------")
url = 'https://codeforces.com/contests'
r = request(url)

source1 = r.text
soup = bs.BeautifulSoup(source1,'lxml')

table = soup.table
table = soup.find('table')

#print(table)

table_rows = table.findAll('tr')

for tr in table_rows:
	td = tr.findAll('td')
	row = [i.text for i in td]
	if len(row)>1:
		name,time = row[0].strip(' '),row[2][2:-2]
		time = time.split(' ')
		time = '   '.join(time)
		time = time+' + 2:30'
		print(time,'  ',name[2:-2])

print()

print("-------------------AT CODER--------------------")
url = 'https://atcoder.jp/'
r = request(url)

source2 = r.text
soup = bs.BeautifulSoup(source2,'lxml')

table = soup.table
table = soup.findAll('tbody')
table = table[1]
table_rows = table.findAll('tr')

for tr in table_rows:
    td = tr.findAll('td')
    row = [i.text for i in td]
    row[0] = row[0].split(' ')
    row[0][1] = row[0][1][:-8]+' -- 3:30'
    row[0] = '   '.join(row[0])
    row[0] = row[0][::-1]
    print(row)
    print()
'''
print("-------------------CodeChef--------------------")

url = 'https://www.codechef.com/contests'
r = request(url)

source2 = r.text
soup = bs.BeautifulSoup(source2,'lxml')

table = soup.table
table = soup.findAll('tbody')
table = table[1]
table_rows = table.findAll('tr')

for tr in table_rows:
    td = tr.findAll('td')
    row = [i.text for i in td]
    print(row[2],"   ",row[1])

'''
