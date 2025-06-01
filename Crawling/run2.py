from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

def get_soup(markup):
    return BeautifulSoup(markup=markup, features='lxml')


def parse_detail_html_to_csv():
    # 定义CSV文件路径
    csv_file_dir = 'douban/douban_book/data_csv/'
    csv_file_name = 'douban_books.csv'
    csv_file_path = Path(csv_file_dir + csv_file_name)
    csv_file_dir_path = Path(csv_file_dir)
    csv_file_dir_path.mkdir(parents=True, exist_ok=True)

    detail_dir = Path('douban/douban_book/douban_book_data_detail/')
    detail_file_list = detail_dir.rglob('*.html')

    book_data = []
    count = 0
    total = 0
    output_str = ""
    def sprint(Str):
        nonlocal output_str
        output_str += str(Str)
        return
    for detail_file in detail_file_list:
        book_id = str(detail_file).split('_')[-1].split('.')[0]
        soup = get_soup(open(file=detail_file, mode='r', encoding='utf-8'))
        tag_title = soup.select_one('#wrapper > h1 > span')
        if tag_title is not None:
            title = tag_title.string
        tag_subjectwrap = soup.select_one('#content > div > div.article > div.indent > div.subjectwrap.clearfix')
        if tag_subjectwrap is not None:
            img_src = tag_subjectwrap.select_one('#mainpic > a > img').attrs.get('src')
            tag_info = tag_subjectwrap.select_one('div.subject.clearfix > #info')
            tag_author = tag_info.find(name='span', attrs={'class': 'pl'}, string=' 作者')
            if tag_author is None:
                author = ''
            else:
                author = tag_author.next_sibling.next_sibling.text.strip()
            tag_publisher = tag_info.find(name='span', attrs={'class': 'pl'}, string='出版社:')
            if tag_publisher is None:
                publisher = ''
            else:
                publisher = tag_publisher.next_sibling.next_sibling.text.strip()
            tag_producer = tag_info.find(name='span', attrs={'class': 'pl'}, string='出品方:')
            if tag_producer is None:
                producer = ''
            else:
                producer = tag_producer.next_sibling.next_sibling.text.strip()
            tag_original_title = tag_info.find(name='span', attrs={'class': 'pl'}, string='原作名:')
            if tag_original_title is None:
                original_title = ''
            else:
                original_title = tag_original_title.next_sibling.strip()
            tag_translator = tag_info.find(name='span', attrs={'class': 'pl'}, string=' 译者')
            if tag_translator is None:
                translator = ''
            else:
                translator = tag_translator.next_sibling.next_sibling.text.strip()
            tag_publication_year = tag_info.find(name='span', attrs={'class': 'pl'}, string='出版年:')
            if tag_publication_year is None:
                publication_year = ''
            else:
                publication_year = tag_publication_year.next_sibling.strip()
            tag_page_count = tag_info.find(name='span', attrs={'class': 'pl'}, string='页数:')
            if tag_page_count is None:
                page_count = ''
            else:
                page_count = tag_page_count.next_sibling.strip()
            tag_price = tag_info.find(name='span', attrs={'class': 'pl'}, string='定价:')
            if tag_price is None:
                price = ''
            else:
                price = tag_price.next_sibling.strip()
            tag_binding = tag_info.find(name='span', attrs={'class': 'pl'}, string='装帧:')
            if tag_binding is None:
                binding = ''
            else:
                binding = tag_binding.next_sibling.strip()
            tag_series = tag_info.find(name='span', attrs={'class': 'pl'}, string='丛书:')
            if tag_series is None:
                series = ''
            else:
                series = tag_series.next_sibling.next_sibling.text.strip()
            tag_isbn = tag_info.find(name='span', attrs={'class': 'pl'}, string='ISBN:')
            if tag_isbn is None:
                isbn = ''
            else:
                isbn = tag_isbn.next_sibling.strip()

            # 评分信息
            tag_rating_wrap_clearbox = tag_subjectwrap.select_one('#interest_sectl > div')
            if tag_rating_wrap_clearbox is not None:
                # 评分
                tag_rating = (tag_rating_wrap_clearbox.select_one('#interest_sectl > div > div.rating_self.clearfix > strong'))
                if tag_rating is None:
                    rating = ''
                else:
                    rating = tag_rating.string.strip()
                # 评论人数
                tag_rating_sum = tag_rating_wrap_clearbox.select_one('#interest_sectl > div > div.rating_self.clearfix > div > div.rating_sum > span > a > span')
                if tag_rating_sum is None:
                    rating_sum = ''
                else:
                    rating_sum = tag_rating_sum.string.strip()
                # 评论链接
                comment_link = f'https://book.douban.com/subject/{book_id}/comments/'
                # 五星比例
                tag_stars5_starstop = tag_rating_wrap_clearbox.select_one('#interest_sectl > div > span.stars5.starstop')
                if tag_stars5_starstop is None:
                    stars5_starstop = ''
                else:
                    stars5_starstop = tag_stars5_starstop.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                # 四星比例
                tag_stars4_starstop = tag_rating_wrap_clearbox.select_one('#interest_sectl > div > span.stars4.starstop')
                if tag_stars4_starstop is None:
                    stars4_starstop = ''
                else:
                    stars4_starstop = tag_stars4_starstop.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                # 三星比例
                tag_stars3_starstop = tag_rating_wrap_clearbox.select_one('#interest_sectl > div > span.stars3.starstop')
                if tag_stars3_starstop is None:
                    stars3_starstop = ''
                else:
                    stars3_starstop = tag_stars3_starstop.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                # 二星比例
                tag_stars2_starstop = tag_rating_wrap_clearbox.select_one('#interest_sectl > div > span.stars2.starstop')
                if tag_stars2_starstop is None:
                    stars2_starstop = ''
                else:
                    stars2_starstop = tag_stars2_starstop.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()
                # 一星比例
                tag_stars1_starstop = tag_rating_wrap_clearbox.select_one('#interest_sectl > div > span.stars1.starstop')
                if tag_stars1_starstop is None:
                    stars1_starstop = ''
                else:
                    stars1_starstop = tag_stars1_starstop.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()

                data_dict = {
                    'book_id': book_id,
                    'title': title,
                    'img_src': img_src,
                    'author': author,
                    'publisher': publisher,
                    'producer': producer,
                    'original_title': original_title,
                    'translator': translator,
                    'publication_year': publication_year,
                    'page_count': page_count,
                    'price': price,
                    'binding': binding,
                    'series': series,
                    'isbn': isbn,
                    'rating': rating,
                    'rating_sum': rating_sum,
                    'comment_link': comment_link,
                    'stars5_starstop': stars5_starstop,
                    'stars4_starstop': stars4_starstop,
                    'stars3_starstop': stars3_starstop,
                    'stars2_starstop': stars2_starstop,
                    'stars1_starstop': stars1_starstop
                }
                sprint(f'===========================文件路径：{detail_file}，解析后的数据如下：===========================')
                sprint(data_dict)
                sprint('===========================================================')
                # 把数据保存到列表中
                book_data.append(data_dict)
                count = count + 1
                if count == 100:
                    total += 100
                    print("count to 100:", total)
                    print(output_str)
                    df = pd.DataFrame(book_data)
                    if not csv_file_path.exists():
                        df.to_csv(csv_file_dir + csv_file_name, index=False, encoding='utf-8-sig')
                    else:
                        df.to_csv(csv_file_dir + csv_file_name, index=False, encoding='utf-8-sig', mode='a', header=False)
                    book_data = []
                    count = 0
                    output_str = ""


if __name__ == '__main__':
    parse_detail_html_to_csv()