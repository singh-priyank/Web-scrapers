from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import csv

driver = webdriver.Firefox()
driver.get("https://www.icsi.edu/member/members-directory/")

time.sleep(3)

#Scroll page down
# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
print(last_height)
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(0.5)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height
time.sleep(1)

## You have to switch to the iframe like so: ##
driver.switch_to_frame(driver.find_element_by_tag_name("iframe"))

try:
	print("about to look")
	element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_partial_link_text("Clear"))
	print("still looking?")
finally: print('done')



#Click on button Clear  //*[@id="dnn_ctr410_MemberSearch_grdMembers_ctl00_ctl02_ctl01_PageSizeComboBox_Arrow"]
driver.find_element_by_partial_link_text("Clear").click()
time.sleep(3)
driver.find_element_by_xpath('//*[@id="dnn_ctr410_MemberSearch_grdMembers_ctl00_ctl02_ctl01_PageSizeComboBox_Arrow"]').click()
time.sleep(1)
#driver.find_element_by_xpath('/html/body/form/div[1]/div/div/ul/li[3]').click()
#time.sleep(7)

#Opening csv file
with open('final_data.csv', 'a+', newline='') as file:
	writer = csv.writer(file)
	#writer.writerow(["Name", "Membership Number","CP Number","Benevolent Member","Address","City","Email","Phone","Mobile"])
	
	
	for j in range(0,5284):
		for i in range(1,11):
			row = []
			try:
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div'.format(i)).text)
			except: continue
			try:
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/div/div[3]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:	
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/div/div[4]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:	
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/div/div[5]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/div[1]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/div[2]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/div[4]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:	
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/div[3]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			try:
				row.append(driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/div[5]/table/tbody/tr/td[2]'.format(i)).text)
			except: continue
			if(len(row)==9):
				writer.writerow(row)

			#org_name = driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[{}]/td[1]/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/div/div[2]/table/tbody/tr/td[2]'.format(i)).text
		#row = table_id.find_element_by_tag_name("tbody")/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/tbody/tr[1]/td[1]
		
		'''if(m%10==1):
			driver.find_element_by_partial_link_text("...").click()
			time.sleep(5)
			print(j)
			continue
		try:
			element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/thead/tr[2]/td/table/tbody/tr/td/div[3]/input[1]'))
		finally: print('done')'''
		try:
			element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/thead/tr[2]/td/table/tbody/tr/td/div[3]/input[1]'))
		finally: print('.')
		driver.find_element_by_xpath('/html/body/form/div[3]/div/div/div[1]/div[2]/div/div/div/div/div[3]/div/table/thead/tr[2]/td/table/tbody/tr/td/div[3]/input[1]').click()
		#driver.find_element_by_partial_link_text('{}'.format(j)).click()
		time.sleep(2)
		print('next page opened.')
		print(j)


