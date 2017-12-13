#! /usr/bin/python2
import mechanize
import cookielib
import bs4
from gtts import gTTS
import os
import sys

def talk(texttospeech):  #text to speech with GTTS
	tts = gTTS(text=texttospeech, lang='en')
	tts.save("/home/lazz/mylastvoice.mp3")
	os.system("mpg123 -q /home/lazz/mylastvoice.mp3")
	os.remove("/home/lazz/mylastvoice.mp3")
# Browser

br = mechanize.Browser()
# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
print("Getting libraries!")

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

 #giving the script an identity as chrome
br.addheaders = [('User-agent', 'Chrome')]


# The site we will navigate into, handling it's session
br.open('https://eservice.worldlink.com.np/login/index')
print("connecting...")


# View available forms
# for f in br.forms():
#     print f

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=0)

# User credentials
br.form['username'] = 'username'
br.form['password'] = 'password'

# Login
br.submit()
print("logged in")
data=br.open('https://eservice.worldlink.com.np/online/activeDevice').read()

soup = bs4.BeautifulSoup(data,"html5lib")

print("Collecting Data...")

# data =soup.select('.activeDeviceList')
data =soup.select('.activeDeviceList span')	
for d in data:
	print(d.getText())

#using beautiful soup to parse data
tabletd = soup.select('.activeDeviceList tbody tr td')
dataOfUsers=[]
for each in tabletd:
	users=each.getText()
	dataOfUsers.append(users)

N = 4
subList = [dataOfUsers[n:n+N] for n in range(0, len(dataOfUsers), N)]
	
#color in the text
CRED = '\033[91m'
CGREEN = '\033[32m'
CEND = '\033[0m'


#logic
if len(subList)<=2:
	goodtoplay="Sir, There are only "+str(len(subList))+" devices connected. It's Good to Play!"
	print(CGREEN + '\t \t'+goodtoplay + CEND)
	talk(goodtoplay)

else:
	nogood="Sir, There are "+str(len(subList))+" users connected. It might lag."
	print(CRED + "\t"+nogood + CEND)
	talk(nogood)

for sublistusers in subList:
	for data2 in sublistusers:
		print(data2)
	print("\n")


