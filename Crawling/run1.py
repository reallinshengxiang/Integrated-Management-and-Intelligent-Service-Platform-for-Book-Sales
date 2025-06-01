import random
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# 快代理试用：https://www.kuaidaili.com/freetest/


def get_request(url, **kwargs):
    time.sleep(random.uniform(0.1, 2))
    print(f'===============================地址：{url} ===============================')
    # 定义一组User-Agent字符串
    user_agents = [
        # Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        # Firefox
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/117.0',
        # Edge
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2040.0',
        # Safari
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15',
    ]

    # 请求头
    headers = {
        'User-Agent': random.choice(user_agents)
    }
    # 用户名密码认证(私密代理/独享代理)
    username = ""
    password = ""
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                        "proxy": '36.25.243.5:11768'},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password,
                                                         "proxy": '36.25.243.5:11768'}
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url=url, timeout=10, headers=headers, **kwargs)
            # response = requests.get(url=url, timeout=10, headers=headers, proxies=proxies, **kwargs)
            if response.status_code == 200:
                return response
            else:
                print(f"请求失败，状态码: {response.status_code}，正在重新发送请求 (尝试 {attempt + 1}/{max_retries})")
        except requests.exceptions.RequestException as e:
            print(f"请求过程中发生异常: {e}，正在重新发送请求 (尝试 {attempt + 1}/{max_retries})")

        # 如果不是最后一次尝试，则等待一段时间再重试
        if attempt < max_retries - 1:
            time.sleep(random.uniform(1, 2))
    print('================多次请求失败，请查看异常情况================')
    return None  # 或者返回最后一次的响应，取决于你的需求


def save_book_html_file(save_dir, file_name, content):
    dir_path = Path(save_dir)
    # 确保保存目录存在，如果不存在则创建所有必要的父级目录
    dir_path.mkdir(parents=True, exist_ok=True)
    # 使用 'with' 语句打开文件以确保正确关闭文件流
    with open(save_dir + file_name, 'w', encoding='utf-8') as fp:
        print(f"==============================={save_dir + file_name} 文件已保存===============================")
        fp.write(str(content))


def download_book_tag():
    save_dir = 'douban/douban_book/douban_book_tag/'
    file_name = 'douban_book_all_tag.html'
    book_tag_url = 'https://book.douban.com/tag/?view=type&icn=index-sorttags-all'
    tag_file_path = Path(save_dir + file_name)
    if tag_file_path.exists() and tag_file_path.is_file():
        print(f'\n===============================文件 {tag_file_path} 已存在===============================')
    else:
        print(f'===============================文件 {tag_file_path} 不存在，正在下载...===============================')
        save_book_html_file(save_dir=save_dir, file_name=file_name, content=get_request(book_tag_url).text)


def get_soup(markup):
    return BeautifulSoup(markup=markup, features='lxml')


def get_book_type_and_href():
    # 定义HTML文件路径
    file = 'douban/douban_book/douban_book_tag/douban_book_all_tag.html'
    # 初始化一个空字典用于存储标签名称和对应的链接
    name_href_result = {}
    # 定义豆瓣书籍的基础URL，用于拼接完整的链接
    book_base_url = 'https://book.douban.com'
    # 打开并读取HTML文件内容
    with open(file=file, mode='r', encoding='utf-8') as fp:
        # 使用BeautifulSoup解析HTML内容
        soup = get_soup(fp)
        # 选择包含所有标签链接的主要容器
        tag = soup.select_one('#content > div > div.article > div:nth-child(2)')
        # 选择所有包含标签链接的表格行（每个类别下的标签表）
        tables = tag.select('div > a.tag-title-wrapper + table.tagCol')
        # 遍历每个表格
        for table in tables:
            # 选择表格中的所有行（tr标签）
            tr_tags = table.select('tr')
            # 遍历每一行
            for tr_tag in tr_tags:
                # 选择行中的所有单元格（td标签）
                td_tags = tr_tag.select('td')
                # 遍历每个单元格
                for td_tag in td_tags:
                    # 选择单元格中的第一个a标签（如果存在）
                    a_tag = td_tag.select_one('a')
                    # 如果找到了a标签，则提取文本和href属性
                    if a_tag:
                        # 提取a标签的文本内容，并去除两端空白字符
                        tag_text = a_tag.string
                        # 获取a标签的href属性，并与基础URL拼接成完整链接
                        tag_href = book_base_url + a_tag.attrs.get('href')
                        # 将提取到的标签文本和链接添加到结果字典中
                        name_href_result[tag_text] = tag_href
    # 返回包含所有标签名称和对应链接的字典
    return name_href_result


def get_book_data_dagai(name, start):
    book_tag_base_url = 'https://book.douban.com/tag/' + name
    payload = {
        'start': start,
        'type': 'T'
    }
    response = get_request(book_tag_base_url, params=payload)
    if response is None:
        return None
    return response.text


def download_book_data_dagai(name, start):
    save_dir = 'douban/douban_book/douban_book_data_dagai/'
    file_name = f'douban_book_data_dagai_{name}_{start}.html'
    dagai_file_path = Path(save_dir + file_name)
    if dagai_file_path.exists() and dagai_file_path.is_file():
        print(f'===============================文件 {dagai_file_path} 已存在===============================')
    else:
        print(
            f'===============================文件 {dagai_file_path} 不存在，正在下载...===============================')
        content = get_book_data_dagai(name, start)
        if content is None:
            return None
        # 判断是否是最后一页
        soup = get_soup(content)
        p_tag = soup.select_one('#subject_list > p')
        if p_tag is not None:
            print(f"===============================分类 {name} 的网页爬取完成===============================")
            return True
        save_book_html_file(save_dir=save_dir, file_name=file_name, content=content)


def download_book_data_detail():
    save_dir = 'douban/douban_book/douban_book_data_detail/'
    dagai_dir = Path('douban/douban_book/douban_book_data_dagai/')
    dagai_file_list = dagai_dir.rglob('*.html')
    for dagai_file in dagai_file_list:
        soup = get_soup(markup=open(file=dagai_file, mode='r', encoding='utf-8'))
        a_tag_list = soup.select('#subject_list > ul > li  h2 > a')
        for a_tag in a_tag_list:
            href = a_tag.attrs.get('href')
            book_id = href.split('/')[-2]
            file_name = f'douban_book_data_detail_{book_id}.html'
            detail_file_path = Path(save_dir + file_name)
            if detail_file_path.exists() and detail_file_path.is_file():
                print(f'===============================文件 {detail_file_path} 已存在===============================')
            else:
                print(
                    f'===============================文件 {detail_file_path} 不存在，正在下载...===============================')
                response = get_request(href)
                if response is None:
                    continue
                save_book_html_file(save_dir, file_name, response.text)


def print_in_rows(items, items_per_row=20):
    for index, name in enumerate(items, start=1):
        print(f'{name}', end=' ')
        if index % items_per_row == 0:
            print()


if __name__ == '__main__':
    
    download_book_tag()

    book_type = get_book_type_and_href()
    book_type_name = book_type.keys()
    print(book_type_name)
    for type_name in book_type_name:
        print(f'===============================图书分类标签：{type_name}===============================')
        start_ = 0
        while True:
            flag = download_book_data_dagai(type_name, start_)
            start_ = start_ + 20
            if flag is None:
                continue
            if flag:
                print(f'======================================图书分类标签 {type_name} 的大概html下载完成======================================')
                break
    
    download_book_data_detail()