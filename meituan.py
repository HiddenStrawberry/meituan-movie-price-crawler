# encoding=utf8
import re
import requests
from bs4 import BeautifulSoup as bs
from meituan_price_img import tesseract
import time

CITY_LIST = {}


def load_city_list():
    html = requests.get('http://www.meituan.com/index/changecity/initiative').text
    string = 'class="isonline" href="(.*?)">(.*?)</a>'
    city = re.findall(string, html, re.S)
    for each in city:
        CITY_LIST[each[1]] = each[0]


load_city_list()


def save_img(img_locate, ir):
    try:
        fp = open(img_locate, 'wb')
        fp.write(ir.content)
        fp.close()
        return True
    except Exception as Err:
        print (Err)


def get_city_url(city_name):
    return CITY_LIST[city_name.decode('utf8')]


def get_all_cinema(cityurl):
    cinema_dict = {}
    for x in range(1, 100):
        url = 'http://' + cityurl + '/dianying/cinemalist/all/all/page' + str(x)
        html = requests.get(url).text
        cinema_list = re.findall(
                '<a class="link--black__green" href="//(.*?)" gaevent="(.*?)" target="_blank">(.*?)</a>', html, re.S)
        if len(cinema_list) == 0: break
        for each in cinema_list:
            cinema_dict[each[2]] = 'http://' + each[0]
    return cinema_dict


def get_cinema_movie(cinema_url):
    result = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Host': 'sh.meituan.com',
    }
    html = requests.get(cinema_url, headers=headers).text
    soup = bs(html, 'html.parser')
    info = soup.select('.movie-info')
    for each in info:
        soup = bs(str(each), 'html.parser')
        movie_name = soup.select('h3')[0].string
        showtime = re.findall('<div class="show-time">(.*?)</div>', str(soup), re.S)[0]
        showtime_list = re.findall('data-date="(.*?)"', showtime, re.S)
        table = soup.select('table')
        count = 0
        for each2 in table:
            k_price = ''
            movie_date = showtime_list[count]
            soup = bs(str(each2), 'html.parser')
            tr = soup.select('tr')
            for each3 in tr:
                price = ''
                try:
                    td = re.findall('<td>(.*?)</td>', str(each3), re.S)
                    movie_time = re.findall('"start-time">(.*?)</span', td[0], re.S)[0]
                    version = td[1]
                    room = td[2]
                    try:
                        pricemsg = td[3]
                        price = re.findall('"background-image: url\(\/(.*?)>', pricemsg, re.S)
                    except:
                        pass
                except:
                    pass

                if len(price) == 2:
                    k_price = ''
                    for each in price:
                        url = re.findall('\/(.*?)\@', each, re.S)[0]
                        position = re.search(' (.*?)px (.*?)px', each)
                        (x, y) = (position.group(1), position.group(2))
                        x = -int(x)
                        y = -int(y)
                        ir = requests.get('http://' + url, verify=False)
                        save_img('1.png', ir)
                        t = tesseract(x, y, '1.png')
                        time.sleep(0.5)
                        k_price = k_price + t

                if len(price) == 7:
                    k_price = ''
                    count = 0
                    for each in [price[2], price[3], price[5], price[6]]:
                        count += 1
                        if count == 3: k_price = str(k_price) + str('.')
                        url = re.findall('\/(.*?)\@', each, re.S)[0]
                        position = re.search(' (.*?)px (.*?)px', each)
                        (x, y) = (position.group(1), position.group(2))
                        x = -int(x)
                        y = -int(y)
                        ir = requests.get('http://' + url, verify=False)
                        save_img('1.png', ir)
                        t = tesseract(x, y, '1.png')
                        k_price = str(k_price) + str(t)
                k_price = k_price.replace('\n', '')
                try:
                    result.append({'movie_name': movie_name, 'movie_time': movie_time, 'movie_date': movie_date,
                                   'version': version, 'room': room, 'price': k_price})
                except:
                    pass
    return result


print get_city_url('上海')
print get_all_cinema('sh.meituan.com')
print get_cinema_movie('http://sh.meituan.com/shop/58174')
