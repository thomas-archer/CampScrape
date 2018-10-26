from bs4 import BeautifulSoup as soup
import smtplib
import os
from lxml import html
import requests


campgroundCode = "70161" #Plaskett creek url code
provided_date = "10/10/2018"
provided_url = "https://www.recreation.gov/campsiteCalendar.do?page=matrix&calarvdate="+provided_date+"&contractCode=NRSO&parkId="+campgroundCode
excludeGroupsites = True
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

#Slack notification to personal 
def send_message_to_slack(text):
    from urllib import request
    import json
    post = {"text": "{0}".format(text)}
    try:
        json_data = json.dumps(post)
        req = request.Request("https://hooks.slack.com/services/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",
                              data=json_data.encode('ascii'),
                              headers={'Content-Type': 'application/json'}) 
        request.urlopen(req)
    except Exception as em:
        print("EXCEPTION: " + str(em))


#Desktop notification function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

#Email notification function
def email_sites(myLinks):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login("thoms.archer@gmail.com", "")
	send_from = "" #Sender email
	send_to = "" #Receiving email
	subject = "Available Campsites!!!"
	mail_text = "Campsites are available at Plaskett Creek! Here's a list of current available sites:\n\n"+myLinks
	message = 'Subject:{}\n\n{}'.format(subject,mail_text)
	s.sendmail(send_from, send_to, message)
	s.quit()
	print("email sent!")
	return

#Main function
def scrape_sites(campDate, campURL):
	available_sites = []
	available_links=""
	req = requests.get(campURL,headers=agent)
	page_soup = soup(req.text, "html.parser")
	table_rows = page_soup.find("table",{"name":"calendar"}).tbody.findAll("tr")
	#Removes group sites
	if excludeGroupsites:
		for row in table_rows:
			link_text=''
			try:
				link_text = row.find("div",{"class":"siteListLabel"}).a.text
			except AttributeError:
				pass
			if "GS" in link_text:
				table_rows.remove(row)
	#Find and store all available sites in array available_sites
	for row in table_rows:
		avail_days = row.findAll("a",{"class":"avail"})
		for day in avail_days:
			day_link = day["href"]
			print(day_link)
			if campDate in day_link:
				temp = "recreation.gov"+str(day_link)
				available_sites.append(temp)
	#If there are any available sites, add their link to available_links string
	if available_sites:
		for a in available_sites:
			available_links+=a+'\n\n'
		print(available_links)
		notify(title = 'Campsites!', subtitle = "", message  = 'Sites are now available!')
		#email_sites(available_links)
		send_message_to_slack('Yo! Campsites are available! Links: \n' + available_links)

	else:
		#notify(title = 'Campsites!', subtitle = "", message  = 'No sites currently available')
		send_message_to_slack('No sites available yet.')

scrape_sites(provided_date,provided_url)