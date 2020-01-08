import bs4 as bs
import requests
import datetime
import pytz

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
        h = time[-5:-3]
        m = time[-2:]
        tim = datetime.timedelta(hours=int(h), minutes=int(m))
        tim = tim + datetime.timedelta(hours = 2,minutes = 30)
        print(time[:-6],'  ',tim,'  ',name[2:-2])

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
    #Converting to Indian time zone
    tm = row[0]
    tm = datetime.datetime.strptime(tm,'%Y-%m-%d %H:%M:%S%z')
    tz = pytz.timezone('Asia/Kolkata')
    tim = str(tm.astimezone(tz))
    tim = tim.split(' ')
    #Date formating
    dat = tim[0]
    dat = dat.split('-')
    dat = '-'.join(dat[::-1])
    print(dat,' ',tim[1][:-6],'  ',row[1])
print()


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


