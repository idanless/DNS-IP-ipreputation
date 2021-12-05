import requests
from bs4 import BeautifulSoup
import re

headers = {
'authority': 'www.abuseipdb.com',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
'referer': 'https://www.abuseipdb.com/'
}

class abuseipdb:
    def __init__(self,ip):
        self.flag = True
        self.ip = ip
        self.httpcall = requests.get('https://www.abuseipdb.com/check/'+"{}".format(self.ip),headers=headers)
        self.page = []
        self.tagcyber = {}
        self.parser = BeautifulSoup(self.httpcall.content, 'html.parser')
        status = self.parser.find("div", class_="well")
        if re.findall('not',status.find('h3').text):
            self.flag = False
    def Abusescore(self):
        if self.flag:
            r = self.parser.find("div", class_="well")
            r = r.find('p').text.split('.')
            for report in r[1].split():
                if re.findall('%', report):
                    return report.replace(':', '')

    def Get_tag(self):
        #first page
        if self.flag:
            t = self.parser.find("table", {"class": "table table-striped responsive-table"})
            t = t.find_all('span', class_='label label-default')
            for tag in t:
                if tag.text in self.tagcyber.keys():
                    self.tagcyber[tag.text] = int(self.tagcyber.get(tag.text) + 1)
                else:
                    self.tagcyber[tag.text] = 1
            return self.tagcyber

    def Lastupdate(self):
        if self.flag:
            u = self.parser.find("div", class_="content")
            u = u.find('section')
            u = u.findAll('b')[5].text
            return u

    def Number_rpeort(self):
        if self.flag:
            r = self.parser.find("div", class_="well")
            r = r.find('p').text.split('.')
            for report in r[0].split():
                if re.match(r'^([\s\d]+)$', report.replace(',', '')):
                    return report
