# SocialCopsChallengeMyWay

Output File:https://drive.google.com/file/d/0Bz5PoqZFBaM-cHExdWttVkF2TTA/view


Explanation of the code:
1. Using requests Library:

 With the help of the requests library I have downloaded the pdf from "http://164.100.180.82/Rollpdf/AC276/S24A276P001.pdf"

req = requests.get('http://164.100.180.82/Rollpdf/AC276/S24A276P001.pdf')
response = open('rawVoterList.pdf', 'wb')
for chunk in req.iter_content(100000):
    response.write(chunk)
response.close()
2. Using pdfminer library in to_text(pdf_path) function :
To this function we will be providing the path to the downloaded pdf('rawVoterList.pdf')
Using 1. from io import StringIO
          2. from pdfminer.pdfinterp import PDFResourceManager, process_pdf
          3. from pdfminer.converter import TextConverter
          4. from pdfminer.layout import LAParams
we will be converting the pdf file to text file.

def to_txt(pdf_path):
    input_ = open(pdf_path, 'rb')
    output = StringIO()

    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    process_pdf(manager, converter, input_)

    return output.getvalue() 
Using

f = open('RawVoter.txt', 'w')
f.write(to_txt('rawVoterList.pdf'))
we will be writing the text to 'RawVoter.txt' that we extracted from 'rawVoterList.pdf'
3. Converting the string ('RawVoter.txt') to lists using split(' '):

with open('RawVoter.txt') as file:
    for line in file:
        lst.append(line.split(' '))
4. Extracting the Voter's Identity Number:

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
"""Now comes the real challenge:"""

5. Here we go to the 'http://164.100.180.82/searchengine/SearchEngineEnglish.aspx' and we will using web scraping to scrape the details of the voters
Challenges in this step:
Challenge 1: First when we send a HTTP request we will be getting the response till selecting the districts and the HTML content is not loaded completely to POST the requests.
Solution 1: Selenium is just the tool for that. Selenium is a webdriver: it takes control of your browser, which then does all the work like loading the web page that will change dynamically when there is a selection or any entry.
Challenge 2: Locating the HTML element is faster than loading the dynamic webpage.
Solution 2: To overcome this we will be using "browser.implicitly_wait(3)" this will solve the problem for you as it makes the browser to wait till it loads the HTML content and now we can locate our HTML content with ease.

Challenge 3: Some of the voter's details are not loaded in the website.
Solution 3: To overcome this I have used the exception handling.
Challenge 4: Sometimes the data is not loaded properly in the website this leading to the duplication of the records.
Solution 4: In order to eliminate the duplication of the records I used recursion in this kind of exceptions.

Not only these 4 exceptions there are more exceptions in this code as they are common exceptions I am not elaborating here.


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
6. Looping the list of Voter Identity Cards that is stored in the updated_list:

for VoterID in updated_list:
    getVoterUrl(VoterID)
7. Writing data to csv file using pandas:
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
8. Plotting the voters according to their ages using Matplotlib library and saving the figure:

import pandas as pd
from pandas import DataFrame, Series
import csv
import matplotlib.pyplot as plt
from scipy import ndimage
records = []
with open('SocialCopsChallengeFullyCompleted1.csv') as file:
    reader = csv.reader(file)
    for row in reader:
        records.append(row)
frame = DataFrame(records)
age_counts = frame[3].value_counts()
clean_age = frame[3].fillna('Missing')
clean_age[clean_age == ''] = 'Unknown'
cleaned_age_counts = clean_age.value_counts()
cleaned_age_counts.plot(kind = 'barh')
plt.title('Plotting voter according to their ages')
plt.xlabel('Count')
plt.ylabel('Age')
plt.grid(True)
plt.savefig('challenge.png', dpi = 2000)
plt.show()
