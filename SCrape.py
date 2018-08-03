from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import timedelta
import subprocess
import os
from winsound import *

# Defines the clear fucntion so as to keep me from going insane
clear = lambda: os.system('cls')

# Too cool for you
print  ' _____ _____                                     _   _   __  '
print '/  ___/  __ \                                   | | | | /  | '
print '\ `--.| /  \/_ __ __ _ _ __   ___     ______    | | | | `| | '
print  ' `--. \ |   |  __/ _` |  _ \ / _ \   |______|   | | | |  | | '
print '/\__/ / \__/\ | | (_| | |_) |  __/              \ \_/ /__| |_'
print '\____/ \____/_|  \__,_| .__/ \___|               \___/(_)___/'
print '                      | |                                    '
print '                      |_|                                    '


# Select the Chrome webdriver for Selenium to use, insert YOUR path here
d = webdriver.Chrome('PATH TO CHROMEDRIVER.EXE')
print '[+] Driver Selected (Chrome)'

# Go to the website
d.get('https://scrap.tf/raffles')
print '[+] Fetching Raffles Page'

# Cookies, add your values in the blank space after value
scrap_session = {'name' : 'PHPSESSID', 'value' : '', 'secure' : True}
scrap_session2 = {'name' : 'scr_session', 'value' : '', 'secure' : True}
cf_uid = {'name' : '_cfduid', 'value' : '', 'secure' : True}
_asc = {'name' : '_asc', 'value' : '', 'secure' : True}
_auc = {'name' : '_auc', 'value' : '', 'secure' : True}
_ga = {'name' : '_ga', 'value' : '', 'secure' : True}
_gat = {'name' : '_gat', 'value' : '', 'secure' : True}
_gid = {'name' : '_gid', 'value' : '', 'secure' : True}

# Add aforementioned cookies
d.add_cookie(scrap_session)
d.add_cookie(scrap_session2)
d.add_cookie(_asc)
d.add_cookie(_auc)
d.add_cookie(_ga)
d.add_cookie(_gat)
d.add_cookie(_gid)
d.add_cookie(cf_uid)
print '[+] Cookies Added'


# Force the site to use the cookies
d.find_element_by_xpath('//*[@id="navbar-main"]/ul[2]/li/a/img').click()
print '[+] Logged In Through Cookies'

# After cookies are set and we are logged in, reload the page back to the raffles
d.get('https://scrap.tf/raffles')
print '[+] Redirecting...'

# Defines procedure for handling a Captcha
def captcha():
    PlaySound("nothing.wav", SND_FILENAME)
    raw_input("Press enter when captcha complete... Commie Bastards")

# Checks for a Captcha
if d.find_elements_by_xpath('//*[contains(text(), "Public Raffles")]'):
    print "[+] No Captcha, go for spasms"

else:
    captcha()


# Function for estimating the time it will take too complete (Rough Estimate)
def timeget():
    x = d.find_element_by_css_selector('.panel > div:nth-child(2) > div:nth-child(1) > i18n:nth-child(1) > var:nth-child(1)').text
    joined = x.split("/", 1)[0]
    total = x.split("/", 1)[-1]
    tojoin = int(total) - int(joined)
    total_time = (int(tojoin) * 3.1) + (int(joined) * 2 + 120)
    seconds = int(total_time)
    microseconds = int((total_time * 1000000) % 1000000)
    output = timedelta(0, seconds, microseconds)
    clear()
    # Too cool for you
    print  ' _____ _____                                     _   _   __  '
    print '/  ___/  __ \                                   | | | | /  | '
    print '\ `--.| /  \/_ __ __ _ _ __   ___     ______    | | | | `| | '
    print  ' `--. \ |   |  __/ _` |  _ \ / _ \   |______|   | | | |  | | '
    print '/\__/ / \__/\ | | (_| | |_) |  __/              \ \_/ /__| |_'
    print '\____/ \____/_|  \__,_| .__/ \___|               \___/(_)___/'
    print '                      | |                                    '
    print '                      |_|                                    '
    print ("[+] Estimated time ")
    print (output)

# Gets time
timeget()
pausetime = 0.3

# Scrolls to bottom of page until there is no more page so as to aquire all listings
last_height = d.execute_script("return document.body.scrollHeight")
while True:
    d.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(pausetime)
    new_height = d.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# The bit that actually grabs all of the links
link_list = [str(a.get_attribute('href')) for a in d.find_elements_by_xpath(".//a")]

# Begins sorting links into ones that are Raffles and ones that aren't, and writing them to a file for further use
f1 = open("linx.txt", "r+")
f1.truncate()
for x in link_list:
    if "/raffles/" in x and "puzzle" not in x and "history" not in x and "won" not in x and "mine" not in x and "ending" not in x and "create" not in x:
        dat = str(x)
        f1.write(dat + "\n")
f1.close()

# Strips the top link progressing down the lines of the file and joins it whilst looking for and potential Captchas(will alert with a sound!)
with open("linx.txt", "r+") as fp:
   line = fp.readline()
   cnt = 1
   while line:
       t = 3.5
       d.get(line.strip())
       print ("[+] OBTAINING: " + line.strip())
       time.sleep(0.3)
       if d.find_elements_by_class_name('subtitle'):


           if d.find_elements_by_xpath('//*[contains(text(), "Enter Raffle")]'):
               d.find_elements_by_css_selector('#raffle-enter')[0].click()
               print("[+] JOINED")
           else:
               print ("[+] ALREADY JOINED")
               t = 0.85
       else:
           captcha()

           if d.find_elements_by_xpath('//*[contains(text(), "Enter Raffle")]'):
               d.find_elements_by_css_selector('#raffle-enter')[0].click()
               print("[+] JOINED")
           else:
               print ("[+] ALREADY JOINED")
               t = 0
       time.sleep(t)
       line = fp.readline()
       cnt += 1

f1.close()
d.quit()
