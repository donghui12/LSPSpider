import requests
from fake_useragent import UserAgent
import re
import os
import random
import time

ua = UserAgent()
HEADER = {'User-Agent': ua.random}
ORIGIN_URL = 'http://tcmspw.com/tcmspsearch.php'
BASE_SEARCH_URL = 'http://tcmspw.com/tcmspsearch.php?qs=herb_all_name&q={}&token={}'
DEFAULT_PATH = './datafile/Text.txt'
TOKEN_PATH = './datafile/token.txt'
BASE_RESULT_URL = 'http://tcmspw.com/tcmspsearch.php?qr={}&qsr=herb_en_name&token={}c'


def getCon(url, mode='text'):
    try:
        resp = requests.get(url, headers=HEADER)
        if resp.status_code == 200 and mode == 'text':
            return resp.text
        elif resp.status_code == 200 and mode == 'byte':
            return resp.content
        else:
            print("链接失败:{}".format(resp.status_code))
            return 0
    except Exception as e:
        print('Error, {}'.format(e))
        return 0


def get_token(text):
    """
    获取token
    :param text:
    :return:
    """
    token = re.search(r'name="token" value="(.*?)"', text).groups(1)[0]
    SaveFile(token, TOKEN_PATH)
    return token


def Process_Text(text):
    pass


def get_English_Name(text):
    """
    获取草药的英文名称
    :param text:
    :return:
    """
    data = re.findall(r'{"herb_cn_name":"(.*?)","herb_en_name":"(.*?)","herb_pinyin":"(.*?)"}', text)
    if len(data) is 0:
        return None
    herb_en_name = data[0][1]
    return herb_en_name


def SaveFile(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print('保存成功')


def load_file(path):
    """
    加载token文件
    :param path:
    :return:
    """
    with open(path, 'r', encoding='utf-8') as f:
        token = f.read()
    return token


def load_sleep_time():
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time)


def main():
    # 获取token 值，不知道有没有用，不过还是获取
    print('检测token文件是否存在。。。')
    load_sleep_time()
    if not os.path.exists(TOKEN_PATH):
        print('token文件不存在。。。\n尝试生成token文件。。。')
        load_sleep_time()
        origin_text = getCon(ORIGIN_URL)
        get_token(origin_text)
        print('生成成功！')
    print('正在尝试加载token文件。。。')
    load_sleep_time()
    token = load_file(TOKEN_PATH)
    print('成功加载token文件！')
    load_sleep_time()
    while True:
        key = input('请输入药材名字：(输入-1以结束程序)')
        try:
            if int(key) is -1:
                break
        except ValueError as e:
            pass
        goal_url = BASE_SEARCH_URL.format(key, token)
        text = getCon(goal_url)
        print('正在获取‘{}’的英文名称。。。'.format(key))
        load_sleep_time()
        herb_en_name = get_English_Name(text)  # 获取英文名字
        print('获取成功！\n{}的英文名称为：{}'.format(key, herb_en_name))

    print('程序退出！')


if __name__ == '__main__':
    # 获取token 值，不知道有没有用，不过还是获取
    print('检测token文件是否存在。。。')
    if not os.path.exists(TOKEN_PATH):
        print('token文件不存在。。。\n尝试生成token文件。。。')
        origin_text = getCon(ORIGIN_URL)
        get_token(origin_text)
        print('生成成功！')
    print('token文件存在\n正在尝试加载token文件。。。')
    token = load_file(TOKEN_PATH)
    print('成功加载token文件！')

    # 获取英文名称
    key = 'Danggui'  # key = input('请输入药材名称:')
    goal_url = BASE_SEARCH_URL.format(key, token)
    text = getCon(goal_url)
    SaveFile(text, DEFAULT_PATH)
    herb_en_name = get_English_Name(text)

    # 获取主要文件
    result_url = BASE_RESULT_URL.format(herb_en_name, token)
    result_text = getCon(result_url)
    SaveFile(result_text, './datafile/resultText.txt')
