# coding: utf-8

import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import datetime as dt
import sqlite3
import os
import re
import copy
import time
os.chdir('/path/to/your/directory')  # Specify the path to your directory

import text_mining

def main():
    ec = scrape('https://www.economist.com/middle-east-and-africa/', economist)
    aj = scrape('https://www.aljazeera.com/topics/regions/middleeast.html', aljazeera)
    tr = scrape('https://www.reuters.com/news/archive/middle-east', reuters)
    bc = scrape('https://www.bbc.co.uk/news/world/middle_east', bbc)
    ws = scrape('https://www.wsj.com/news/types/middle-east-news', wsj)
    ft = scrape('https://www.ft.com/world/mideast', financialtimes)
    bb = scrape('https://www.bloomberg.com/view/topics/middle-east', bloomberg)
    cn = scrape('https://edition.cnn.com/middle-east', cnn)
    fo = scrape('https://fortune.com/tag/middle-east/', fortune)

    df = ft
    for i in [aj, tr, bc, ws, cn, fo, ec, bb]:
        df = df.append(i)

    df.reset_index(inplace=True, drop=True)

    df = database(df)

    output = text_mining.remove_similar(df, text_mining.stopword)

    for i in range(len(output)):
        if 'https://' not in output['link'][i]:
            temp = re.search('www', output['link'][i]).start()
            output.at[i, 'link'] = 'http://' + output['link'][i][temp:]

    print(output)

    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" 
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html>

    <head>
    <meta charset="UTF-8">
    <meta content="width=device-width, initial-scale=1" name="viewport">
    <meta name="x-apple-disable-message-reformatting">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta content="telephone=no" name="format-detection">
    <title></title>
    <!--[if (mso 16)]>
    <style type="text/css">
    a {text-decoration: none;}
    </style>
    <![endif]-->
    <!--[if gte mso 9]><style>sup 
    { font-size: 100% !important; }</style><![endif]-->
    </head>

    <body>
    <div class="es-wrapper-color">
        <!--[if gte mso 9]>
                <v:background xmlns:v="urn:schemas-microsoft-com:vml" 
                fill="t">
                    <v:fill type="tile" color="#333333"></v:fill>
                </v:background>
            <![endif]-->
        <table class="es-content-body" width="600" 
        cellspacing="15" cellpadding="15" bgcolor="#ffffff" 
        align="center">
         <tr>
            <td class="esd-block-text" align="center">
            <h2>Middle East</h2></td>
         </tr></table>
         <div><br></div>
        
    """

    for i in range(len(output)):
        html += """<table class="es-content-body" width="600" 
        cellspacing="10" cellpadding="5" bgcolor="#ffffff"
        align="center">"""
        html += """<tr><td class="esd-block-text es-p10t es-p10b"
        align="center"><p><a href="%s">
        <font color="#6F6F6F">%s<font><a></p></td></tr>
        <tr><td align="center">
        <img src="%s" width="200" height="150"/></td></tr>
        <tr>""" % (output['link'][i], output['title'][i], output['image'][i])
        html += """</tr></table><div><br></div>"""

    html += """
    </div>
    </body>
    </html>
    """

    send(html)


def send(html):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)

    receivers = ['email1@example.com', 'email2@example.com', 'email3@example.com']
    mail.To = ';'.join(receivers)
    
    mail.Subject = 'Mid East Newsletter %s' % (dt.datetime.now())
    mail.BodyFormat = 2
    mail.HTMLBody = html

    condition = str(input('0/1 for no/yes:'))
    if condition == '1':
        mail.Send()
        print('\nSENT')
    else:
        print('\nABORT')


def database(df):
    temp = []
    conn = sqlite3.connect('mideast_news.db')
    c = conn.cursor()

    for i in range(len(df)):
        try:
            c.execute("""INSERT INTO news VALUES (?,?,?)""", df.iloc[i, :])
            conn.commit()

            print('Updating...')

            temp.append(i)

        except Exception as e:
            print(e)

    conn.close()

    if temp:
        output = df.loc[[i for i in temp]]
        output.reset_index(inplace=True, drop=True)
    else:
        output = pd.DataFrame()
        output['title'] = ['No updates yet.']
        output['link'] = output['image'] = ['']

    return output


def scrape(url, method):
    print('scraping webpage effortlessly')
    time.sleep(5)

    session = requests.Session()
    response = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = bs(response.content, 'html.parser', from_encoding='utf_8_sig')

    df = method(page)
    out = database(df)

    return out


def economist(page):
    title, link, image = [], [], []
    df = pd.DataFrame()
    prefix = 'https://www.economist.com'

    a = page.find_all('div', class_="topic-item-container")

    for i in a:
        link.append(prefix + i.find('a').get('href'))
        title.append(i.find('a').text)
        image.append(i.parent.find('img').get('src'))

    df['title'] = title
    df['link'] = link
    df['image'] = image

    return df


def fortune(page):
    title, link, image = [], [], []
    df = pd.DataFrame()
    prefix = 'https://fortune.com'

    a = page.find_all('article')

    for i in a:
        link.append(prefix + i.find('a').get('href'))

        if 'http' in i.find('img').get('src'):
            image.append(i.find('img').get('src'))
        else:
            image.append('')

        temp = re.split('\s*', i.find_all('a')[1].text)
        temp.pop()
