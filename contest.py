import traceback
import bs4 as bs
import requests
import datetime 
import pytz
from pytz import timezone
from dateutil import tz
import json
import logging
import json
from urllib.parse import unquote

logger=logging.getLogger() 

logger.setLevel(logging.DEBUG) 

def make_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
    }
    return requests.get(url,headers=headers)

def codeforces_contest():
    url = 'https://codeforces.com/api/contest.list'
    r = make_request(url)
    contest_list = []
    # print(r)
    if r.status_code != 200:
        return []

    data = json.loads(r.text)
    contests =  data['result']
    live_contests = [n for n in contests if n["phase"]=="BEFORE" or n["phase"]=="CODING"]
    # print(live_contests)

    # to_zone = tz.gettz('Asia/Kolkata')
    tz = pytz.timezone('Asia/Kolkata')

    for contest in live_contests:
        ct = {}
        
        dt= datetime.datetime.utcfromtimestamp(contest['startTimeSeconds'])
        
        dt = pytz.UTC.localize(dt)
        ist = pytz.timezone('Asia/Kolkata')
        dt = dt.astimezone(ist)
        enddt= dt + datetime.timedelta(seconds=contest['durationSeconds'])
        
        date = dt.strftime('%d-%m-%y')
        time = dt.strftime('%H:%M')

        ct['date'] = str(date)
        ct['time'] = str(time)

        ct['enddate'] = enddt.strftime('%d-%m-%y')
        ct['endtime'] = enddt.strftime('%H:%M')


        ct['name'] = contest['name']
        ct['id'] = contest['id']
        ct['url'] = 'https://codeforces.com/contests'
        ct['platform'] = "CODEFORCES"
        ct['timestamp'] = dt.timestamp()
        ct['endtimestamp'] = enddt.timestamp()

        logger.info("{} @ {} {}".format(ct['name'], ct['date'], ct['time']  ))

        contest_list.append(ct)
    print(len(contest_list) , "data collected")
    return contest_list
  
def atcoder_contest():
    
    url = 'https://atcoder.jp/'
    r = make_request(url)

    source2 = r.text
    soup = bs.BeautifulSoup(source2,'lxml')

    table = soup.table
    table = soup.findAll('tbody')
    table = table[1]
    table_rows = table.findAll('tr')

    contest_list = []
    for tr in table_rows:
        ct = {}
        td = tr.findAll('td')
        
        row = [i.text for i in td]
        # print(  td[1].find('a').get('href'))
        
        link = tr.findAll('a')[0]['href']
        a =link.split("iso=")[1]
        a = a.split("&")[0] + '+0900'
        tm = datetime.datetime.strptime(a,'%Y%m%dT%H%M%z')
        
        ist = pytz.timezone('Asia/Kolkata')
        tm =tm.astimezone(ist)

        
        date = tm.strftime('%d-%m-%y')
        time = tm.strftime('%H:%M')

        ct['date'] = str(date)
        ct['time'] = str(time)

        td[1].find('a').get('href')
        ct['url'] = 'https://www.atcoder.jp' +  td[1].find('a').get('href')

        # print(ct['url'])

        ct['name'] = row[1]
        ct['platform'] = "ATCODER"
        ct['timestamp'] = tm.timestamp()

        logger.info("{} @ {} {}".format(ct['name'], ct['date'], ct['time']  ))

        
        contest_list.append(ct)
    print(len(contest_list) , "data collected")
    return contest_list

def codechef_contest():
    url = 'https://www.codechef.com/contests'
    r = make_request(url)

    source2 = r.text
    soup = bs.BeautifulSoup(source2,'lxml')

    table = soup.table
    table = soup.findAll('tbody')
    table = table[1]
    table_rows = table.findAll('tr')

    contest_list = []
    for tr in table_rows:
        ct = {}
        td = tr.findAll('td')

        row = [i.text for i in td]
        # print("++++++++++++++++++")
        # print('https://www.codechef.com' + td[1].find('a').get('href').split('?')[0])
        # print("++++++++++++++++++")

        # print(row[2]) 27 Jun 2020  19:30:00
        tm = datetime.datetime.strptime(row[2],'%d %b %Y  %H:%M:%S')
        date = tm.strftime('%d-%m-%y')
        time = tm.strftime('%H:%M')

        endtm = datetime.datetime.strptime(row[3],'%d %b %Y  %H:%M:%S')
        enddate = endtm.strftime('%d-%m-%y')
        endtime = endtm.strftime('%H:%M')

        ct['date'] = str(date)
        ct['time'] = str(time)

        ct['enddate'] = str(enddate)
        ct['endtime'] = str(endtime)

        
        ct['url'] = 'https://www.codechef.com' + td[1].find('a').get('href').split('?')[0] 

        ct['name'] = row[1].strip()
        ct['platform'] = "CODECHEF"
        ct['timestamp'] = tm.timestamp()
        ct['endtimestamp'] = endtm.timestamp()

        logger.info("{} @ {} {}".format(ct['name'], ct['date'], ct['time']  ))
        
        
        contest_list.append(ct)
    print(len(contest_list) , "data collected")
    return contest_list

def hackerearth():

    url = 'https://www.hackerearth.com/challenges'
    r = make_request(url)
    source = r.text
    soup = bs.BeautifulSoup(source,'html.parser')
    upcoming = soup.find('div',{'class':'upcoming challenge-list'})
    events = upcoming.findAll('div',{'class':'challenge-card-modern'})

    contest_list = []
    for event in events:
        raw_date = event.find('div',{'class':'date'}).text.strip()
        name = event.find('span',{'class':'challenge-list-title'}).text.strip()
        types = event.find('div',{'class':'challenge-type'}).text.strip()
         
        print(raw_date)
        tm = datetime.datetime.strptime(raw_date,'%b %d, %I:%M %p %Z')
        tm = tm.replace(year = datetime.datetime.now().year)
        ist = pytz.timezone('Asia/Kolkata')
        tm = tm.astimezone(ist)
        
        date = tm.strftime('%d-%m-%y')
        time = tm.strftime('%H:%M')
        ct = {}
        ct['date'] = str(date)
        ct['time'] = str(time)

        ct['name'] = name
        ct['platform'] = "HACKEREARTH"
        ct['type'] = types
        ct['timestamp'] = tm.timestamp()
        
        contest_list.append(ct)

    return contest_list

def mlh():
    url = 'https://mlh.io/seasons/2021/events'
    r = make_request(url)
    source = r.text
    soup = bs.BeautifulSoup(source,'html.parser')

    container  = soup.find_all(class_="container feature")[1]
    # print(len(container))
    row = container.find_all(class_="row")[0]
    # print(row[0])

    events = row.find_all(class_="event")

    print(len(events))

    event_list = []

    for event in events:
        ct = {}

        ct['name'] = event.find(class_="event-name").get_text()


        ct['date'] = event.find(attrs={"itemprop":"startDate"}).attrs["content"]
        dt = datetime.datetime.strptime(ct['date'], '%Y-%m-%d')
        ct['time'] = str(dt.time())

        ct['enddate'] =  event.find(attrs={"itemprop":"endDate"}).attrs["content"]
        enddt = datetime.datetime.strptime(ct['date'], '%Y-%m-%d')
        ct['endtime'] = str(enddt.time())
    
        ct['url'] = event.find(class_="event-link")['href']
        ct['platform'] = "MLH"

        ct['timestamp'] = dt.timestamp()
        ct['endtimestamp'] = enddt.timestamp()

        event_list.append(ct)

    return event_list

def format_date(string):
    part1 = string[0:4]
    part2 = string[4:6]
    part3 = string[6:]
    temp = [part1, part2, part3]
    s="-".join(temp)
    s+=" 00:00"
    return s 


def devpost_contest():

    url = 'https://devpost.com/hackathons?page=2'
    r = make_request(url)

    source2 = r.text
    soup = bs.BeautifulSoup(source2,'lxml')
    s=soup.find('div','challenge-results')
    contest_list=[]
    for contest in s.find_all('div','row'):
        
        u=contest.find('a')['href']
        r=make_request(u).content
        r = bs.BeautifulSoup(r,'lxml')
        print(".", end="")
        qw=[]
        qw=r.find('ul','no-bullet').find_all('li')
        x=qw[1].find('a')['href']
        r = requests.get(x).url
        r=unquote(r)

        x=r.split("dates=")
        y=x[1].split('T')
        date_str=format_date(y[0])
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M').date()
        date = date_obj.strftime('%d-%m-%y')
        time= date_obj.strftime('%H:%M')
        #enddt= next_day(date_str)
        #edate_end = datetime.datetime.strptime(enddt, '%Y-%m-%d %H:%M').date()
        #edate = edate_obj.strftime('%d-%m-%y')
        #etime= edate_obj.strftime('%H:%M')
        ct = {}
        ct['name'] = contest.h2.text.strip()
        #ct['id'] = contest['id']
        ct['url'] =contest.a['href']
        ct['platform'] = "DEVPOST"
        ct['date'] = str(date)
        ct['time'] = str(time)

        
        ct['endtime'] = str(time)
        dt = datetime.datetime.strptime(ct['date'], '%d-%m-%y')
        ct['timestamp'] = dt.timestamp()
        enddt= dt + datetime.timedelta(days=1)
        ct['enddate'] = str(enddt)
        ct['endtimestamp'] = enddt.timestamp()
        # print(ct)

        contest_list.append(ct)

    return contest_list








def get_contest():
    contests = []
    try:

        # print("codechef")
        logger.info("fetching codechef contest ")
        contests +=  codechef_contest()
    except Exception as e:
        # contests['codechef'] += []
        print(e)
        logger.error(e, exc_info=True)

    try:
        logger.info("fetching codeforces contest ")
        

        contests +=  codeforces_contest()
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)
        

    try:
        
        logger.info("fetching atcoder contest ")
        
        contests +=  atcoder_contest()
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)

    try:
        
        logger.info("fetching hackerearth contest ")
        
        contests +=  hackerearth()
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)

    try:
        
        logger.info("fetching MLH contest ")
        
        contests +=  mlh()
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)
    
    try:
        
        logger.info("fetching Devpost contest ")
        
        contests +=  devpost_contest()
    except Exception as e:
        print(e)
        logger.error(e, exc_info=True)



    def sort_param(x):    
        return x['timestamp']
    contests.sort(key=sort_param )

    logger.info("{} contest details found".format(len(contests)))

    data = {}
    data['updated'] = datetime.datetime.now().strftime('%d-%m-%Y')
    data['time'] = datetime.datetime.now().strftime('%H:%M %Z')
    data['contests'] = contests

    with open("data.json", "w") as outfile: 
        json_object = json.dumps(data, indent=4)
        outfile.write(json_object) 

    return contests

# print(json.dumps(get_contest(), indent=4))
