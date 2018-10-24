import requests
from bs4 import BeautifulSoup
import sys


def bbs_set(user_name, password, text):
    TARGET_URL = 'https://bbs.sjtu.edu.cn'
    s = requests.Session()
    s.post(TARGET_URL + '/bbslogin', data={
        'id': user_name,
        'pw': password,
        'submit': 'login'
    })
    s.post(TARGET_URL + '/bbsplan', data={
        'text': text.encode('gbk'),
        'type': 'update'
    })

    soup = BeautifulSoup(s.get(TARGET_URL + '/bbsplan').text, 'lxml')
    print(soup.find('textarea').string.strip())


if __name__ == '__main__':
    bbs_set(sys.argv[1], sys.argv[2], sys.argv[3])
