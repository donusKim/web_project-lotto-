from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rotto_project.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()
from catalog.models import Round

class web_crawler(object):
    def __init__(self, url):
        self.url = url
        self.html = BeautifulSoup(requests.get(url).content, 'html.parser')


class lotto_num(web_crawler):
    def get_info(self):
        self.winning_num = [int(x) for x in self.html.find('meta', {'name': 'description'})['content'].split()[3].split('+')[0].split(',')]
        self.bonus_num = int(
            self.html.find('meta', {'name': 'description'})['content'].split()[3].split('+')[1].split('.')[0])

        info = self.html.findAll('td')
        self.winning_money = []
        self.winning_people = []
        self.winning_type = {}

        for i in [1, 7, 12, 17, 22]:
            self.winning_money.append(to_int(info[i].getText().split('원')[0]))
        for i in [2, 8, 13, 18, 23]:
            self.winning_people.append(to_int(info[i].getText()))

        type_info = re.sub('[\n\t\r ]', '', self.html.findAll('td')[5].getText())
        type_len = len(type_info)
        if type_info:
            methods = ['자동', '수동', '반자동']
            for method in methods:
                if type_info.find(method) > 0:
                    if method == '자동' and type_info.find('수동') > 0:
                        self.winning_type[method] = int(type_info[type_info.find(method) + 2:type_info.find('수동')])
                    elif method == '자동' and type_info.find('반자동') > 0:
                        self.winning_type[method] = int(type_info[type_info.find(method) + 2:type_info.find('반자동')])
                    elif method == '수동' and type_info.find('반자동') > 0:
                        self.winning_type[method] = int(type_info[type_info.find(method) + 2:type_info.find('반자동')])
                    else:
                        if method != '반자동':
                            self.winning_type[method] = int(type_info[type_info.find(method) + 2:type_len])
                        else:
                            self.winning_type[method] = int(type_info[type_info.find(method) + 3:type_len])

        return [self.winning_num, self.bonus_num, self.winning_money, self.winning_people, self.winning_type]


class lotto_store(web_crawler):
    def get_info(self):
        self.page_num = len(self.html.findAll('div', {'id': 'page_box'})[0].getText().replace('\n', ''))
        self.first_info = []
        self.second_info = []
        end_idx = 0
        for page in range(self.page_num):
            html_page = BeautifulSoup(requests.get(self.url + "&nowPage=" + str(page + 1)).content, 'html.parser')
            info = html_page.findAll('td')
            start = 0
            if page < 1:
                while 1:
                    if info[5 * start + 2].getText() != str(start + 1):
                        break
                    store_name = info[5 * start + 3].getText()
                    win_type = re.sub('[\n\t\r ]', '', info[5 * start + 4].getText())
                    store_address = info[5 * start + 5].getText()
                    self.first_info.append([store_name, store_address, win_type])
                    start += 1

                end_idx = 5 * start + 1
            start = 0
            while 1:
                if end_idx + 3 + 4 * start > len(info):
                    break
                store_name = info[end_idx + 2 + 4 * start].getText()
                store_address = info[end_idx + 3 + 4 * start].getText()
                self.second_info.append([store_name, store_address])
                start += 1

        return [self.first_info, self.second_info]


def to_int(money):
    total = 0
    money = money.split(',')
    for i in range(len(money)):
        total += int(money[len(money) - i - 1]) * 10 ** (i * 3)
    return total

def insert_round(round_num):
    url = "https://dhlottery.co.kr/gameResult.do?method=byWin&drwNo="+str(round_num)
    x = lotto_num(url)
    temp = x.get_info()
    if temp[4]:
        if '자동' not in temp[4]:
            if '수동' not in temp[4]:
                Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5], temp[1],
                           temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0], temp[3][1],
                           temp[3][2], temp[3][3], temp[3][4], 0, 0, temp[4]['반자동']).save()
            else:
                if '반자동' in temp[4]:
                    Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                               temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                               temp[3][1], temp[3][2], temp[3][3], temp[3][4], 0, temp[4]['수동'], temp[4]['반자동']).save()
                else:
                    Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                               temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                               temp[3][1], temp[3][2], temp[3][3], temp[3][4], 0, temp[4]['수동'], 0).save()
        else:
            if '수동' not in temp[4]:
                if '반자동' in temp[4]:
                    Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                               temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                               temp[3][1], temp[3][2], temp[3][3], temp[3][4], temp[4]['자동'], 0, temp[4]['반자동']).save()
                else:
                    Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                          temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                          temp[3][1], temp[3][2], temp[3][3], temp[3][4], temp[4]['자동'], 0, 0).save()
            else:
                if '반자동' in temp[4]:
                    Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                               temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                               temp[3][1], temp[3][2], temp[3][3], temp[3][4], temp[4]['자동'], temp[4]['수동'],
                               temp[4]['반자동']).save()
                else:
                    Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                               temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                               temp[3][1], temp[3][2], temp[3][3], temp[3][4], temp[4]['자동'], temp[4]['수동'], 0).save()
    else:
        Round(round_num, temp[0][0], temp[0][1], temp[0][2], temp[0][3], temp[0][4], temp[0][5],
                   temp[1], temp[2][0], temp[2][1], temp[2][2], temp[2][3], temp[2][4], temp[3][0],
                   temp[3][1], temp[3][2], temp[3][3], temp[3][4], 0, 0, 0).save()


if __name__=='__main__':
    week = 945
    insert_round(week)
