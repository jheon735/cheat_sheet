import numpy as np
import requests
from bs4 import BeautifulSoup
import sys

def getimage(date):
    DATE=str(date)
    YYYY=str(date)[:4]
    if date<19960519:
        print('No data')
        sys.exit()
    if date<20110101:
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/mdiigr/%s/'%(YYYY,DATE))
        html=req.text
        soup=BeautifulSoup(html,'html.parser')
        notice=soup.select('table > tr > td > a')
        filename=notice[4].text
        f=open('%s_conti.jpg'%date,'wb')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/mdiigr/%s/%s'%(YYYY,DATE,filename))
        f.write(req.content)
        f.close()
        print('saved continum image')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/mdimag/%s/'%(YYYY,DATE))
        html=req.text
        soup=BeautifulSoup(html,'html.parser')
        notice=soup.select('table > tr > td > a')
        filename=notice[4].text
        f=open('%s_mag.jpg'%date,'wb')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/mdimag/%s/%s'%(YYYY,DATE,filename))
        f.write(req.content)
        f.close()
        print('saved mag image')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/eit195/%s/'%(YYYY,DATE))
        html=req.text
        soup=BeautifulSoup(html,'html.parser')
        notice=soup.select('table > tr > td > a')
        filename=notice[4].text
        f=open('%s_195.jpg'%date,'wb')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/eit195/%s/%s'%(YYYY,DATE,filename))
        f.write(req.content)
        f.close()
        print('saved 195 image')
    elif date>20110101:
        req = requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/hmiigr/%s/' % (YYYY, DATE))
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        notice = soup.select('table > tr > td > a')
        filename = notice[4].text
        f = open('%s_conti.jpg' % date, 'wb')
        req = requests.get(
            'https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/hmiigr/%s/%s' % (YYYY, DATE, filename))
        f.write(req.content)
        f.close()
        print('saved continum image')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/hmimag/%s/'%(YYYY,DATE))
        html=req.text
        soup=BeautifulSoup(html,'html.parser')
        notice=soup.select('table > tr > td > a')
        filename=notice[4].text
        f=open('%s_mag.jpg'%date,'wb')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/hmimag/%s/%s'%(YYYY,DATE,filename))
        f.write(req.content)
        f.close()
        print('saved mag image')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/eit195/%s/'%(YYYY,DATE))
        html=req.text
        soup=BeautifulSoup(html,'html.parser')
        notice=soup.select('table > tr > td > a')
        filename=notice[4].text
        f=open('%s_195.jpg'%date,'wb')
        req=requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/eit195/%s/%s'%(YYYY,DATE,filename))
        f.write(req.content)
        f.close()
        print('saved 195 image')



def get_xray_flux_plot(date):
    DATE=str(date)
    YYYY=str(date)[:4]
    req=requests.get('https://www.spaceweatherlive.com/images/Archief/%s/plots/xray/%s_xray.gif'%(YYYY,DATE))
    f=open('%s_xrayflux.gif'%date,'wb')
    f.write(req.content)
    f.close()
    print('saved x-ray flux graph')


def get_195_image(date):
    DATE = str(date)
    YYYY = str(date)[:4]
    if date < 19960519:
        print('No data')
        sys.exit()
    req = requests.get('https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/eit195/%s/' % (YYYY, DATE))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    notice = soup.select('table > tr > td > a')
    filename = notice[4].text
    f = open('%s_195.jpg' % date, 'wb')
    req = requests.get(
        'https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/%s/eit195/%s/%s' % (YYYY, DATE, filename))
    f.write(req.content)
    f.close()

    print('saved 195 image')

