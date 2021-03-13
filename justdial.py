from bs4 import BeautifulSoup
import urllib
import csv
import requests

maping = {
	"mobilesv icon-ac":'0',
"mobilesv icon-yz":'1',
"mobilesv icon-wx":'2',
"mobilesv icon-vu":'3',
"mobilesv icon-ts":'4',
"mobilesv icon-rq":'5',
"mobilesv icon-po":'6',
"mobilesv icon-nm":'7',
"mobilesv icon-lk":'8',
"mobilesv icon-ji":'9',
}

def innerHTML(element):
    return element.decode_contents(formatter="html")

def get_name(body):
	return body.find('span', {'class':'jcn'}).a.string

def get_phone_number(body):
	try:
		number = body.find('p', {'class':'contact-info'}).span.a.b
		number1 = body.find('p', {'class':'contact-info'}).span.a
		res=''
		if number==None and number1==None:
			return ''
		if number==None:
			number=number1
		for i in number:
			s = str(i)
			if s[13:29] in maping:
				res+=maping[s[13:29]]
			else:
				res+=' '
		return res
	except AttributeError:
		return ''

def get_rating(body):
	rating = 0.0
	text = body.find('span', {'class':'star_m'})
	if text is not None:
		for item in text:
			rating += float(item['class'][0][1:])/10

	return rating

def get_rating_count(body):
	text = body.find('span', {'class':'rt_count'}).string

	# Get only digits
	rating_count =''.join(i for i in text if i.isdigit())
	return rating_count

def get_address(body):
	return body.find('span', {'class':'mrehover'}).text.strip()

def get_location(body):
	text = body.find('a', {'class':'rsmap'})
	if text == None:
		return
	text_list = text['onclick'].split(",")
	
	latitutde = text_list[3].strip().replace("'", "")
	longitude = text_list[4].strip().replace("'", "")
	
	return latitutde + ", " + longitude


def request(url):
	headers = {
		"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	return requests.get(url,headers=headers)


page_number = 1
service_count = 1

city = input("Enter the name of city\n")
option = input("Enter the type you want\n")
nu = int(input("Enter the number of data required multiple of 10\n"))

fields = ['Name', 'Phone', 'Rating', 'Rating Count', 'Address', 'Location']
out_file = open('data.csv','w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

# Write fields first
csvwriter.writerow(dict((fn,fn) for fn in fields))

while True:

	# Check if reached end of result
	if page_number > nu//10:
		break

	url="https://www.justdial.com/{}/{}/page-{}".format(city,option,page_number)
	print(url)
	req = request(url)
	page = req.text
	# page=urllib2.urlopen(url)

	soup = BeautifulSoup(page, "html.parser")
	services = soup.find_all('li', {'class': 'cntanr'})

	print(page)
	# Iterate through the 10 results in the page
	for service_html in services:

		# Parse HTML to fetch data
		dict_service = {}
		name = get_name(service_html)
		print(name)
		phone = get_phone_number(service_html)
		rating = get_rating(service_html)
		count = get_rating_count(service_html)
		address = get_address(service_html)
		location = get_location(service_html)
		if name != None:
			dict_service['Name'] = name
		if phone != None:
			dict_service['Phone'] = phone
		if rating != None:
			dict_service['Rating'] = rating
		if count != None:
			dict_service['Rating Count'] = count
		if address != None:
			dict_service['Address'] = address
		if location != None:
			dict_service['Address'] = location

		# Write row to CSV
		csvwriter.writerow(dict_service)
		print("#" + str(service_count) + " " , dict_service)
		service_count += 1

	page_number += 1

out_file.close()



