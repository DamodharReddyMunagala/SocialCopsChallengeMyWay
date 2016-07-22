# SocialCopsChallengeMyWay
import requests
from bs4 import BeautifulSoup
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from selenium import webdriver
import pandas as pd

lst = []
updated_list = []
#voter_details_url = []
age = []
gender = []
voter_name = []
polling_date = []
relative_name = []
serial_number = []
voter_name_in_hindi = []
identity_card_number = []
relative_name_in_hindi = []
constituency_number_and_name = []
polling_station_number_and_name = []
constituency_number_and_name_in_hindi = []

req = requests.get('http://164.100.180.82/Rollpdf/AC276/S24A276P001.pdf')
response = open('rawVoterList.pdf', 'wb')
for chunk in req.iter_content(100000):
    response.write(chunk)
response.close()

def to_txt(pdf_path):
    input_ = open(pdf_path, 'rb')
    output = StringIO()

    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    process_pdf(manager, converter, input_)

    return output.getvalue() 

f = open('RawVoter.txt', 'w')
f.write(to_txt('rawVoterList.pdf'))

with open('RawVoter.txt') as file:
    for line in file:
        lst.append(line.split(' '))

for line in lst:
    for word in line:
        if 'ANB' in word:
            if 'ANB' == word[0 : 3]:
                updated_list.append(word[0 : 10])
        if 'GLT' in word:
            if 'GLT' == word[0 : 3]:
                updated_list.append(word[0 : 10])
        if 'UP/28/135/' in word:
            if 'UP/28/135/' == word[0 : 10]:
                updated_list.append(word[0 : 17])

def getVoterUrl(VoterID):
    path_to_chromedriver = '/home/damodhar/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    url = 'http://164.100.180.82/searchengine/SearchEngineEnglish.aspx'
    browser.get(url)
    browser.find_element_by_xpath('//*[@id = "ddlDistricts"]/option[contains(text(), "Faizabad")]').click()
    browser.implicitly_wait(3)
    try:
        browser.find_element_by_xpath('//*[@id="txtEPICNo"]').clear()
        browser.find_element_by_xpath('//*[@id="txtEPICNo"]').send_keys(VoterID)
        browser.find_element_by_xpath('//*[@id = "Button1"]').click()
        browser.implicitly_wait(2)
    except:
        getVoterUrl(VoterID)
        
    try:
        link = '/html/body/form/div[6]/div/div[3]/div/div/div/div/div/div/div/table/tbody/tr/td/div/table/tbody/tr[14]/td/div/table/tbody/tr[2]/td[1]/a'
        browser.find_element_by_xpath(link).click()
        browser.implicitly_wait(2)
        test_html = browser.page_source
        test_soup = BeautifulSoup(test_html, 'lxml')
    except:
        test_html = browser.page_source
        test_soup = BeautifulSoup(test_html, 'lxml')    
    
    browser.switch_to_window(browser.window_handles[0])
    html = browser.page_source
    browser.quit()
    soup = BeautifulSoup(html, 'lxml')
    #voter_details_url.append([[VoterID],['http://164.100.180.82/searchengine/' + VoterUrl]])
    try:
        if 'Total 1 record(s) found' == (test_soup.find('span', {'id' : 'lblNote'}).text):
            constituency_number_and_name.append(soup.find('span', {'id' : 'lbl_AC_NO_NAME'}).text.strip())
            constituency_number_and_name_in_hindi.append(soup.find('span', {'id' : 'lbl_AC_NO_NAME_VER'}).text.strip())
            voter_name.append(soup.find('span', {'id' : 'lbl_NAME'}).text.strip())
            voter_name_in_hindi.append(soup.find('span', {'id' : 'lbl_NAME_VER'}).text.strip())
            gender.append(soup.find('span', {'id' : 'lbl_SEX'}).text.strip())
            identity_card_number.append(soup.find('span', {'id' : 'lbl_EPIC'}).text.strip())
            relative_name.append(soup.find('span', {'id' : 'lbl_RELATIVE_NAME'}).text.strip())
            relative_name_in_hindi.append(soup.find('span', {'id' : 'lbl_RELATIVE_NAME_VER'}).text.strip())
            serial_number.append(soup.find('span', {'id' : 'lbl_SERIAL_NO'}).text.strip())
            polling_station_number_and_name.append(soup.find('span', {'id' : 'lbl_POL_STN_NO_NAME_VER'}).text.strip())
            polling_date.append(soup.find('span', {'id' : 'LblPollDate'}).text.strip())
            cells = (test_soup.find('tr', {'style' : 'color:#224388;background-color:#D0E0FB;'}).findAll('td'))
            age.append(cells[9].text)

        if 'No Match Found :(' == (soup.find('span', {'id' : 'lblNote'}).text):
            #voter_details_url.append([[VoterID], ['No Details URL for this VoterID']])
            constituency_number_and_name.append('')
            constituency_number_and_name_in_hindi.append('')
            voter_name.append('')
            voter_name_in_hindi.append('')
            gender.append('')
            identity_card_number.append(VoterID)
            relative_name.append('')
            relative_name_in_hindi.append('')
            serial_number.append('')
            polling_station_number_and_name.append('')
            polling_date.append('')
            age.append('')
    except:
        getVoterUrl(VoterID)

for VoterID in updated_list:
    getVoterUrl(VoterID)

df=pd.DataFrame(voter_name, columns = ['Voter Name'])
df['Voter Name In Hindi'] = voter_name_in_hindi
df['Gender'] = gender
df['Age'] = age
df['Identity Card Number'] = identity_card_number
df['Relative Name'] = relative_name
df['Relative Name In Hindi'] = relative_name_in_hindi
df['Serial Number'] = serial_number
df['Constituency Number And Name In Hindi'] = constituency_number_and_name_in_hindi
df['Constituency Number And Name'] = constituency_number_and_name
df['Polling Station Number And Name'] = polling_station_number_and_name
df['Polling Date'] = polling_date
df.to_csv('SocialCopsChallengeFullyCompleted.csv',index=True,header=True)
print ('1')
