#encoding=utf8
import requests
import re
CITY_LIST={}
def load_city_list():
    html=requests.get('http://m.gewara.com/touch/cityList.xhtml').text
    string = '<a href="(.*?)">(.*?)</a>'
    city = re.findall(string, html, re.S)
    for each in city:
        CITY_LIST[each[1]] = 'http://m.gewara.com'+each[0]
load_city_list()
class Gewara:
    def __init__(self,city):
        self.browser=requests.session()
        self.set_city(city)
        self.cinema_dict = {}
    def get_city_url(self,city_name):
        return CITY_LIST[city_name.decode('utf8')]

    def set_city(self,city_name):
        url=self.get_city_url(city_name)
        self.browser.get(url)

    def get_all_cinema(self):

        for x in range(1, 100):
            url = 'https://m.gewara.com/movie/m/ajax/getCinemaList.xhtml?pageNo='+str(x)+'&pointx=&pointy=&countycode=&subwayid=&indexareacode=&specialfield='
            html = self.browser.get(url).text
            if not html:break
            cinema_list=re.findall('<a  hr(.*?)</a>',html,re.S)
            for each in cinema_list:
                name=re.findall('<b>(.*?)</b>',each,re.S)[0]
                address=re.findall('<span class="ui_oneLine">(.*?)</span>',each,re.S)[0]
                cid=re.findall('cid=(.*?)"',each,re.S)[0]
                self.cinema_dict[cid]=name
        return self.cinema_dict

    def get_cinema_movie(self,cid):
        # GET MID LIST
        result=[]
        movie_dict={}
        for x in range(0, 100):
            html = self.browser.get('http://m.gewara.com/movie/m/ajax/choiceMovie.xhtml?pageNo='+str(x)+'&cid='+str(cid)+'&ajax=true&filmfest=').text
            if not html:break
            movie_list=re.findall('<li>(.*?)</li>',html,re.S)
            for each in movie_list:
                mid=re.findall('id="(.*?)"',each,re.S)[0]
                name=re.findall('<b>(.*?)</b>',each,re.S)[0]
                movie_dict[name]=mid
        for key,value in movie_dict.items():
            data={'mid':value,
                'cid':cid,
                'discountid':'',
                'adverId':'',
                'from':'',
                'appVersion':'',
                'apptype':'',
                'osType':''
                  }
            movie=self.browser.post('http://m.gewara.com/movie/m/ajax/chooseMovieOpi.xhtml',data=data).text

            date=re.findall('id="(.*?)"',movie.replace('id="choiceDate"',''),re.S)
            for each in date:
                data_date={'mid':value,
                'cid':cid,
                'discountid':'',
                'adverId':'',
                'opiClick':'true',
                'openDate':each,
                'from':'',
                'appVersion':'',
                'apptype':'',
                'osType':''
                  }

                movie_date=self.browser.post('http://m.gewara.com/movie/m/ajax/chooseMovieOpi.xhtml',data=data_date).text
                each_movie=re.findall('<div class="box(.*?)</div>',movie_date,re.S)
                for each_time_movie in each_movie:
                    label_b=re.findall('<b(.*?)</b>',each_time_movie,re.S)
                    try:
                        room=re.findall('<em class="ui_edtType ">(.*?)</em>',each_time_movie,re.S)[0].replace('\t','')
                    except:
                        room=re.findall('<em class="ui_edtType hasType ">(.*?)<span',each_time_movie,re.S)[0].replace('\t','')
                    movie_time=label_b[0].replace('\r','').replace('\n','').replace('\t','').replace('>','')
                    if 'ui_movieType ui_typePurple' in movie_time:
                        continue
                    version=label_b[1].replace('>','')
                    if 'fs14' in label_b[2]:
                        price=re.findall('</i>(.*?) ',label_b[2]+' ',re.S)[0]

                        # 敲黑板 看这里

                        result.append({'movie_name': key, 'movie_time': movie_time, 'movie_date': each,
                                   'version': version, 'room': room, 'price': price})

                        # 敲黑板 看这里
                    else:
                        price=False
                    print key,each,movie_time,version,room,price




a=Gewara('上海')
for each,value in a.get_all_cinema().items():
    print value,each
    a.get_cinema_movie(each)