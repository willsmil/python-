# coding=utf-8
import random
import re
from bs4 import BeautifulSoup
import time

import csv
from urllib import request


def get_html(url):
    req = request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = request.urlopen(req).read()
    return html


def get_url(html):
    htmlCharset = "utf-8"
    soup = BeautifulSoup(html, "lxml", from_encoding=htmlCharset)
    urlList = []
    for tag in soup.find_all(href=re.compile("//shuju.wdzj.com/plat-info")):
        href = "http:" + tag.get('href')
        urlList.append(href)
    return urlList


def get_dataUrl(url):
    html = get_html(url)
    htmlCharset = "utf-8"
    soup = BeautifulSoup(html, "lxml", from_encoding=htmlCharset)
    dataUrl = soup.find_all(href=re.compile('//www.wdzj.com/dangan/'))
    return 'https:' + dataUrl[2].get('href')


def get_data(dataUrl):
    html = get_html(dataUrl)
    soup = BeautifulSoup(html, "lxml", from_encoding="utf-8")
    name = soup.find('h1').get('alt')
    type = soup.find("span", "tag tag1").get_text().replace('\n', '').replace(' ', '')
    str = soup.find("div", "pt-info").get_text().replace('\n', '').replace(' ', '')
    s = str.split("上线")
    time = s[0]
    location = s[1]
    infoList = soup.find_all("div", "r")
    regMoney = infoList[0].get_text().replace('\n', '').replace(' ', '')
    bankSave = infoList[1].get_text().replace('\n', '').replace(' ', '')
    debtAssign = infoList[6].get_text().replace('\n', '').replace(' ', '')
    tenderGuarantee = infoList[7].get_text().replace('\n', '').replace(' ', '')
    guaranteeType = infoList[8].get_text().replace('\n', '').replace(' ', '')
    tmp = soup.find("div", "dianpinbox").get_text().replace('\n', '').replace(' ', '')
    grade = tmp.split('已有')[0]
    list = [name, type, location, time, regMoney, bankSave, debtAssign, tenderGuarantee, guaranteeType, grade]
    return list


def work():
    html = get_html("https://shuju.wdzj.com")
    urlList = get_url(html)

    row = ['名字', '类型', '注册地点', '上线时间', '注册资金', '存管方式', '债权转让', '投标保障', '保障模式', '评分']
    out = open("csv_test.csv", "a", newline="")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(row)

    for url in urlList:
        try:
            dataUrl = get_dataUrl(url)
            time.sleep(random.randint(1, 5))
            row = get_data(dataUrl)
            out = open("result.csv", "a", newline="")
            csv_writer = csv.writer(out, dialect="excel")
            csv_writer.writerow(row)
            time.sleep(random.randint(2, 3))
        except BaseException:
            continue
    out.close()


if __name__ == '__main__':
    work()
