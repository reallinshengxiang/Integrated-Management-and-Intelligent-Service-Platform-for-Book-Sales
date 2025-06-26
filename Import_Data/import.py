import psycopg2
import csv
from datetime import datetime
import logging
from collections import defaultdict
import urllib.parse
import re
import locale

password = urllib.parse.quote_plus("Password!2025")
DB_CONFIG = f"postgres://linshengxiang:{password}@localhost:5433/bookstoredb"
CSV_BOOKS_PATH = "douban_books.csv"
CSV_REVIEWS_PATH = "bookreviews_processed.csv"
LOG_FILE = "import_errors.log"
SQL_INIT_FILE = "init_db.txt"

# 初始化日志
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_tables(conn, sql_file_path):
    """执行 SQL 脚本创建数据库表"""
    try:
        with open(sql_file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        with conn.cursor() as cur:
            cur.execute(sql_script)
        conn.commit()
        print("数据库表创建成功！")
    except Exception as e:
        logging.error(f"创建数据库表失败: {str(e)}")
        conn.rollback()

def import_publishers(conn, books_csv_path):
    """批量导入出版社数据（修复游标关闭问题）"""
    publisher_names = set()
    with open(books_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["publisher"]:
                publisher_names.add(row["publisher"])
    publisher_map = {}
    with conn.cursor() as cur:
        insert_sql = """
            INSERT INTO publishers (publisher_name)
            VALUES (%s)
            ON CONFLICT (publisher_name) DO NOTHING;
        """
        cur.executemany(insert_sql, [(name,) for name in publisher_names])
        conn.commit()
        cur.execute("SELECT id, publisher_name FROM publishers;")
        publisher_map = {name: pid for pid, name in cur.fetchall()}
    return publisher_map

def import_users(conn, reviews_csv_path):
    """从评论中提取唯一用户并导入（包含密码哈希）"""
    user_ids = set()
    with open(reviews_csv_path, "r", encoding="gb2312", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id_str = row["user_id"].strip()
            user_ids.add(int(user_id_str))
    insert_sql = """
        INSERT INTO users (id, username, password_hash, user_type, email, phone)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """
    dummy_hash = "import_default"
    with conn.cursor() as cur:
        for uid in user_ids:
            user_data = (uid, f"user_{uid}", dummy_hash, "customer", None, None)
            try:
                cur.execute(insert_sql, user_data)
                conn.commit()
            except Exception as e:
                conn.rollback()
    user_map = {str(uid): uid for uid in user_ids}
    return user_map

def parse_price(price_str):
    """增强版价格解析函数，处理各种货币格式"""
    if not price_str:
        return 0.00
    currency_symbols = {
        '¥', '￥', '€', '£', '$', '元', 'USD', 'EUR', 'GBP', 'JPY', 'CNY', 'NTD', 'NT$', 'RMB', 'CAD', 'AUD'
    }
    cleaned_str = price_str
    for symbol in currency_symbols:
        cleaned_str = cleaned_str.replace(symbol, '')
    cleaned_str = ''.join(c for c in cleaned_str if c.isdigit() or c in ['.', ',', '-'])
    if ',' in cleaned_str and '.' in cleaned_str:
        cleaned_str = cleaned_str.replace(',', '')
    elif ',' in cleaned_str:
        cleaned_str = cleaned_str.replace(',', '.')
    try:
        price = float(cleaned_str)
        if price < 0:
            return 0.00
        return round(price, 2)
    except ValueError:
        num_match = re.search(r'\d+\.?\d*', cleaned_str)
        if num_match:
            try:
                return round(float(num_match.group()), 2)
            except:
                return 0.00
        return 0.00

def parse_date(date_str):
    """增强版日期解析函数，支持多种格式"""
    if not date_str:
        return None
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error:
        pass
    formats = [
        "%Y/%m/%d",    # 2001/8/1
        "%Y-%m-%d",    # 2001-08-01
        "%Y-%m",       # 2004-10 (新增)
        "%b-%y",       # Oct-02
        "%b-%Y",       # Oct-2004 (新增)
        "%B-%y",       # April-04 (新增)
        "%B-%Y",       # April-2004 (新增)
        "%b %d, %Y",   # Oct 01, 2002
        "%d-%b-%Y",    # 01-Oct-2002
        "%Y",          # 2001
        "%m/%d/%Y",    # 08/01/2002 (美式)
        "%d/%m/%Y",    # 01/08/2002 (欧式)
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if fmt in ["%Y-%m", "%B-%y", "%B-%Y", "%b-%Y"]:
                return dt.replace(day=1).date()
            return dt.date()
        except ValueError:
            continue
    month_map = {
        'jan': 1, 'january': 1,
        'feb': 2, 'february': 2,
        'mar': 3, 'march': 3,
        'apr': 4, 'april': 4,
        'may': 5, 
        'jun': 6, 'june': 6,
        'jul': 7, 'july': 7,
        'aug': 8, 'august': 8,
        'sep': 9, 'september': 9,
        'oct': 10, 'october': 10,
        'nov': 11, 'november': 11,
        'dec': 12, 'december': 12
    }
    match = re.match(r"([a-zA-Z]+)\W*(\d{1,4})", date_str, re.IGNORECASE)
    if match:
        month_str, year_str = match.groups()
        month_name = month_str.lower()
        month = month_map.get(month_name)
        if not month:
            month_abbr = month_name[:3]
            month = month_map.get(month_abbr) 
        if month:
            year = int(year_str)
            if len(year_str) == 1:  # 1位年份 (e.g., April-4 → 2004)
                year = 2000 + year
            elif len(year_str) == 2:  # 2位年份
                year = 2000 + year if year < 50 else 1900 + year
            return datetime(year, month, 1).date()  # 设为当月第一天
    if re.match(r"^\d{4}$", date_str):
        try:
            return datetime(int(date_str), 1, 1).date()  # 设为该年1月1日
        except ValueError:
            pass
    match = re.match(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", date_str)
    if match:
        year, month, day = map(int, match.groups())
        try:
            return datetime(year, month, day).date()
        except ValueError:
            pass 
    match = re.match(r"(\d{4})[-/](\d{1,2})", date_str)
    if match:
        year, month = map(int, match.groups())
        try:
            return datetime(year, month, 1).date() 
        except ValueError:
            pass
    return None 
 
def import_books(conn, books_csv_path, publisher_map):
    """直接批量插入书籍数据（无临时文件）"""
    insert_sql = """
        INSERT INTO books (
            id, ISBN, title, price, author,
            publisher_id, publish_date, cover_link, rating
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s
        )
    """
    with conn.cursor() as cur:
        with open(books_csv_path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    book_id = row.get("book_id")
                    if not book_id:
                        logging.error(f"book_id缺失: {row.get('title', '未知')}，跳过记录")
                        continue
                    isbn = row.get("isbn")
                    if isbn:
                        if 'e' in isbn.lower():
                            isbn = f"{float(isbn):.0f}"
                        isbn = isbn.strip().replace('-', '')
                    else:
                        logging.error(f"ISBN缺失: {row.get('title', '未知')}，跳过记录")
                        continue
                    publisher_name = row["publisher"].strip() if row.get("publisher") else ""
                    publisher_id = publisher_map.get(publisher_name)
                    if not publisher_id:
                        cur.execute("SELECT id FROM publishers WHERE publisher_name = '未知出版社' LIMIT 1;")
                        default_pub = cur.fetchone()
                        if default_pub:
                            publisher_id = default_pub[0]
                        else:
                            cur.execute("INSERT INTO publishers (publisher_name) VALUES ('未知出版社') RETURNING id;")
                            publisher_id = cur.fetchone()[0]
                            publisher_map["未知出版社"] = publisher_id
                    price_str = row.get("price", "").strip()
                    price = parse_price(price_str)
                    pub_date_str = row.get("publication_year", "").strip()
                    publish_date = parse_date(pub_date_str)
                    if pub_date_str and not publish_date:
                        logging.info(f"日期解析失败: 原始值 '{pub_date_str}'") 
                    title = row["title"].strip() if row.get("title") else "无标题"
                    author = row["author"].strip() if row.get("author") else "佚名"
                    cover_link = row["img_src"].strip() if row.get("img_src") else None
                    rating_str = row.get("rating", "").strip()
                    rating = None
                    if rating_str:
                        try:
                            rating = float(rating_str)
                            if rating < 0 or rating > 10:
                                logging.warning(f"评分超出范围: {rating}，设为NULL")
                                rating = None
                            else:
                                rating = round(rating, 2) / 2
                        except ValueError:
                            logging.warning(f"评分格式错误: {rating_str}，设为NULL")
                    cur.execute("SELECT id FROM books WHERE ISBN = %s LIMIT 1;", (isbn,))
                    if cur.fetchone():
                        logging.error(f"ISBN已存在: {isbn}，跳过记录")
                        continue
                    cur.execute(
                        insert_sql,
                        (
                            book_id, isbn, title, price, author,
                            publisher_id, publish_date, cover_link, rating
                        )
                    )
                    conn.commit()
                    print(f"插入书籍: {book_id}, ISBN: {isbn}, 出版社ID: {publisher_id}")
                except Exception as e:
                    logging.error(f"书籍插入失败: {row.get('title', '未知')}, 错误: {str(e)}")
                    conn.rollback() 
                    continue
        conn.commit() 
    print("书籍导入完成")
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM books;")
        db_count = cur.fetchone()[0]
        with open(books_csv_path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.DictReader(f)
            csv_count = sum(1 for _ in reader)
        print(f"CSV 文件记录数: {csv_count}, 成功导入数据库记录数: {db_count}")

def import_reviews(conn, reviews_csv_path, user_map):
    """逐条插入评论数据，跳过无效book_id的评论"""
    insert_sql = """
        INSERT INTO reviews (
            book_id, user_id, rating, comment, created_at
        ) VALUES (
            %s, %s, %s, %s, %s
        );
    """
    success_count = 0
    invalid_book_count = 0
    other_error_count = 0
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM books;")
        existing_book_ids = {str(row[0]) for row in cur.fetchall()}
    if not existing_book_ids:
        raise ValueError("数据库中没有可用的书籍，无法导入评论")
    print(f"数据库中找到 {len(existing_book_ids)} 本图书")
    with open(reviews_csv_path, "r", encoding="gb2312", errors="replace") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            try:
                review_id = row.get('ID', f"自动生成_{idx}")
                book_id_str = row.get("book_id", "").strip()            
                if not book_id_str:
                    invalid_book_count += 1
                    raise ValueError("书籍ID为空")
                if book_id_str not in existing_book_ids:
                    invalid_book_count += 1
                    raise ValueError(f"书籍ID不存在: {book_id_str}")         
                book_id = int(book_id_str)
                user_id_str = row.get("user_id", "").strip()
                user_id = int(user_id_str)
                map_user_id = user_map.get(user_id_str)
                if map_user_id is None:
                    raise ValueError(f"用户ID不存在: {user_id_str}")
                rating_str = row.get("rating", "").strip()
                rating = None
                if rating_str:
                    try:
                        rating = int(rating_str)
                        if rating < 1 or rating > 5:
                            raise ValueError(f"评分超出范围: {rating}")
                    except (ValueError, TypeError) as e:
                        raise ValueError(f"评分解析错误: {rating_str}") from e
                comment = row.get("comment", "").strip()
                if comment:
                    comment = comment.replace("\n", " ")
                else:
                    comment = None
                date_str = row.get("time", "").strip()
                if not date_str:
                    raise ValueError("日期为空")
                try:
                    created_at = datetime.strptime(date_str, "%Y/%m/%d").date()
                except (ValueError, TypeError) as e:
                    raise ValueError(f"日期格式错误: {date_str} (格式应为YYYY/MM/DD)") from e
                with conn.cursor() as cur:
                    cur.execute(
                        insert_sql,
                        (book_id, user_id, rating, comment, created_at)
                    )
                    conn.commit()
                    success_count += 1
                    if success_count % 1000 == 0:
                        print(f"已成功导入 {success_count} 条评论")
            except ValueError as ve:
                error_info = {
                    "review_id": review_id,
                    "book_id": book_id_str,
                    "error": str(ve),
                    "line_number": idx
                }
                logging.error(f"评论导入失败（无效书籍ID）: {error_info}")
                invalid_book_count += 1
                conn.rollback()
                continue
            except Exception as e:
                error_info = {
                    "review_id": review_id,
                    "book_id": book_id_str if 'book_id_str' in locals() else None,
                    "error": str(e),
                    "line_number": idx
                }
                logging.error(f"评论导入失败（其他错误）: {error_info}")
                other_error_count += 1
                conn.rollback()
                continue
    print(f"导入完成: 成功 {success_count} 条, 无效书籍ID {invalid_book_count} 条, 其他错误 {other_error_count} 条")


def main():
    conn = psycopg2.connect(DB_CONFIG)
    create_tables(conn, SQL_INIT_FILE)
    print("开始导入出版社数据...")
    publisher_map = import_publishers(conn, CSV_BOOKS_PATH)
    print("开始导入用户数据...")
    user_map = import_users(conn, CSV_REVIEWS_PATH)
    print("开始导入书籍数据...")
    import_books(conn, CSV_BOOKS_PATH, publisher_map)
    print("开始导入评论数据...")
    import_reviews(conn, CSV_REVIEWS_PATH, user_map)
    conn.close()
    print("全部操作完成！")

if __name__ == "__main__":
    main()