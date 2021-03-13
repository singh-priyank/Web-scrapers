from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

state = []
confirm_cases = []
cured_cases = []
death_cases = []
Passenger_screened_on_Airport,Active_Cases,Cured,Deaths = 0,0,0,0
Total_sample_tested,Total_sample_today=0,0

def getdata(url):
	headers = {
    	"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0"
	}
	return requests.get(url,headers=headers).text


data = getdata("https://www.mygov.in/corona-data/covid19-statewise-status/")

soup = BeautifulSoup(data, "lxml")
#print(soup.prettify())
Passenger = soup.find('div',{'class':'field field-name-field-passenger-screened-format field-type-text field-label-above'})
Passenger_screened_on_Airport = Passenger.text.split()[4]

Active = soup.find('div',{'class':'field field-name-field-total-active-case field-type-number-integer field-label-above'})
Active_Cases = Active.text.split()[2]

Cured = soup.find('div',{'class':'field field-name-field-total-cured-discharged field-type-number-integer field-label-above'})
Cured = Cured.text.split()[1]

Deaths = soup.find('div',{'class':'field field-name-field-total-death-case field-type-number-integer field-label-above'})
Deaths = Deaths.text.split()[1]

Sample = soup.find('div',{'class':'field field-name-field-total-samples-tested field-type-text field-label-above'})
Total_sample_tested = Sample.text.split()[3]

Today = soup.find('div',{'class':'field field-name-field-samples-tested-today field-type-text field-label-above'})
Total_sample_today = Today.text.split()[3]

names = soup.find_all('div',{'class':'field field-name-field-select-state field-type-list-text field-label-above'})

confirmed = soup.find_all('div',{'class':'field field-name-field-total-confirmed-indians field-type-number-integer field-label-above'})

cured = soup.find_all('div',{'class':'field field-name-field-cured field-type-number-integer field-label-above'})

deaths = soup.find_all('div',{'class':'field field-name-field-deaths field-type-number-integer field-label-above'})



for name in names:
	tem = name.text.split()
	state.append(' '.join(tem[2:]))

for confirm in confirmed:
	confirm_cases.append(confirm.text.split()[2])

for i in cured:
	cured_cases.append(i.text.split()[3])

for death in deaths:
	death_cases.append(death.text.split()[1])

print(state)
print(confirm_cases)
print(cured_cases)
print(death_cases)

