# SocialCopsChallengeInUniqueManner

from wand.image import Image
from PIL import Image as PI
import pyocr
import io
import pyocr.builders
import requests
from bs4 import BeautifulSoup
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from selenium import webdriver
import pandas as pd
import time

tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[1]

lst = []
updated_list = []
#voter_details_url = []
age = []
gender = []
district = []
state = []
assembly_constituency = []
name = []
name_in_hindi = []
EPICNO = []
relative_name = []
relative_name_in_hindi = []
partNo = []
partName = []
serialNo = []
pollingStation = []

"""
req = requests.get('http://164.100.180.82/Rollpdf/AC276/S24A276P001.pdf')
response = open('rawVoterList.pdf', 'wb')
for chunk in req.iter_content(100000):
    response.write(chunk)
response.close()
"""

def to_txt(pdf_path):
    input_ = open(pdf_path, 'rb')
    output = StringIO()

    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    process_pdf(manager, converter, input_)

    return output.getvalue() 

#f = open('RawVoter.txt', 'w')
#f.write(to_txt('rawVoterList.pdf'))

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
                


def generateCaptchaURL():
    datetime = []
    localtime = time.asctime( time.localtime(time.time()) )
    datetime.append(localtime.split(' ')[0])
    datetime.append(localtime.split(' ')[1])
    datetime.append(localtime.split(' ')[2])
    datetime.append(localtime.split(' ')[4])
    datetime.append(localtime.split(' ')[3])
    date = (' '.join(datetime))
    return ('http://electoralsearch.in/Captcha?image=true&id=' + date + ' GMT+0530 (IST)')

def captchaImageDownload():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
    captchaUrl = generateCaptchaURL()
    req = requests.get(captchaUrl, headers = headers)
    response = open(captchaUrl.replace('/', '-').replace('.', '-') + '.png', 'wb')
    for chunk in req.iter_content(100000):
        response.write(chunk)
    response.close()
    return (captchaUrl.replace('/', '-').replace('.', '-') + '.png')


def CaptchaText():
    req_image = []
    final_text = []
    captchaUrl = captchaImageDownload()
    #image_pdf = Image(filename="Resume.pdf", resolution=300)
    #image_jpeg = image_pdf.convert('jpeg')
    image_png = Image(filename = captchaUrl, resolution = 100)
    image_jpeg = image_png.convert('jpeg')
    for img in image_png.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))
    for img in req_image: 
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt.replace('\n', '').replace(' ', ''))
    return (final_text)

def getVoterDetails(VoterID):
    text = CaptchaText()
    path_to_chromedriver = '/home/damodhar/chromedriver'
    browser = webdriver.Chrome(executable_path = path_to_chromedriver)
    url = 'http://electoralsearch.in/'
    browser.get(url)
    browser.find_element_by_xpath('//*[@id="continue"]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/ul/li[2]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[1]/div/div[2]/input').clear()
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[1]/div/div[2]/input').send_keys(VoterID)
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[2]/div/div[2]/span/select/option[35]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[3]/div/div[2]/input').send_keys(text)
    browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[4]/div/button').click()
    browser.implicitly_wait(3)
    try:
        invalidCaptcha = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[2]/form/fieldset/div[3]/div/div[2]/span').text
    except:
        pass
    
    print (invalidCaptcha)
    
    if '*Invalid Captcha' in invalidCaptcha:
        getVoterDetails(VoterID)
        
    browser.implicitly_wait(3)
    
    try:
        if 'Number of Record(s) Found: 1' in browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div/div[1]').text:
            age.append(browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div/table/tbody/tr/td[4]').text)
            district.append(browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div/table/tbody/tr/td[7]').text)
            assembly_constituency.append(browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div/table/tbody/tr/td[10]').text)
            browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div/table/tbody/tr/td[1]/form/input[21]').click()
            browser.implicitly_wait(3)
            browser.switch_to_window(browser.window_handles[1])
            state.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[2]/td[2]').text)
            name.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[5]/td').text)
            name_in_hindi.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[4]/td[2]').text)
            gender.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[6]/td[2]').text)
            EPICNO.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[7]/td[2]').text)
            relative_name.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[9]/td').text)
            relative_name_in_hindi.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[8]/td[2]').text)
            partNo.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[10]/td[2]').text)
            partName.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[11]/td[2]').text)
            serialNo.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[12]/td[2]').text)
            pollingStation.append(browser.find_element_by_xpath('/html/body/div[3]/div/div[1]/table/tbody/tr[13]/td[2]/a').text)
        
        if 'Number of Record(s) Found: 0' in browser.find_element_by_xpath('/html/body/div[4]/div[2]/div[1]/div/div[1]').text:
            age.append('')
            district.append('')
            assembly_constituency.append('')
            name.append('')
            name_in_hindi.append('')
            gender.append('')
            state.append('')
            EPICNO.append(VoterID)
            relative_name.append('')
            relative_name_in_hindi.append('')
            partNo.append('')
            partName.append('')
            serialNo.append('')
            pollingStation.append('')
    except:
        getVoterDetails(VoterID)

        
getVoterDetails('ANB2155281')

df=pd.DataFrame(name, columns = ['Voter Name'])
df['Voter Name In Hindi'] = name_in_hindi
df['Gender'] = gender
df['Age'] = age
df['Identity Card Number'] = EPICNO
df['Relative Name'] = relative_name
df['Relative Name In Hindi'] = relative_name_in_hindi
df['Serial Number'] = serialNo
df['Assembly Constituency'] = assembly_constituency
df['Part Number'] = partNo
df['Part Name'] = partName
df['Polling Station'] = pollingStation
df['District'] = district
df['State'] = state
df.to_csv('test.csv',index=True,header=True)
print ('1')
