import re
from datetime import datetime
import locale

import re
from datetime import datetime
import locale

def parse_date(date_str):
    """增强版日期解析函数，支持多种格式"""
    if not date_str:
        return None
    
    # 设置英文locale确保月份缩写解析正确
    try:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    except locale.Error:
        pass  # 如果失败，继续尝试其他方法
    
    # 尝试多种日期格式
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
    
    # 尝试标准格式
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            # 对于只有年份和月份的情况，设为当月第一天
            if fmt in ["%Y-%m", "%B-%y", "%B-%Y", "%b-%Y"]:
                return dt.replace(day=1).date()
            return dt.date()
        except ValueError:
            continue
    
    # 尝试特殊格式：月份缩写/全称 + 年份 (April-4, April-93)
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
    
    # 匹配格式：月份名称（全称或缩写） + 连字符 + 1-4位年份
    match = re.match(r"([a-zA-Z]+)\W*(\d{1,4})", date_str, re.IGNORECASE)
    if match:
        month_str, year_str = match.groups()
        month_name = month_str.lower()
        month = month_map.get(month_name)
        
        if not month:
            # 尝试匹配前3个字母作为缩写
            month_abbr = month_name[:3]
            month = month_map.get(month_abbr)
        
        if month:
            year = int(year_str)
            # 处理不同位数的年份
            if len(year_str) == 1:  # 1位年份 (e.g., April-4 → 2004)
                year = 2000 + year
            elif len(year_str) == 2:  # 2位年份
                year = 2000 + year if year < 50 else 1900 + year
            # 3位或4位年份直接使用
            return datetime(year, month, 1).date()  # 设为当月第一天
    
    # 尝试仅年份格式 (2001)
    if re.match(r"^\d{4}$", date_str):
        try:
            return datetime(int(date_str), 1, 1).date()  # 设为该年1月1日
        except ValueError:
            pass
    
    # 尝试复杂格式：2001/8/1 (带单数字月份/日期)
    match = re.match(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})", date_str)
    if match:
        year, month, day = map(int, match.groups())
        try:
            return datetime(year, month, day).date()
        except ValueError:
            pass 
    
    # 尝试 YYYY-MM 格式 (2004-10)
    match = re.match(r"(\d{4})[-/](\d{1,2})", date_str)
    if match:
        year, month = map(int, match.groups())
        try:
            return datetime(year, month, 1).date()  # 设为当月第一天
        except ValueError:
            pass
    
    return None  # 所有尝试失败
 

# 测试用例
test_cases = [
    # 标准格式
    ("2001/8/1", "2001-08-01"),
    ("2023-12-31", "2023-12-31"),
    ("2005", "2005-01-01"),
    ("Oct-02", "2002-10-01"),
    ("Mar-04", "2004-03-01"),
    ("May-94 ", "1994-05-01"),
    ("Dec-00 ", "2000-12-01"),
    
    # 变体格式
    ("OCT-87", "1987-10-01"),
    ("aug-04", "2004-08-01"),
    ("Nov03", "2003-11-01"),
    ("Sep 2004", "2004-09-01"),
    ("15-Jul-2023", "2023-07-15"),
    ("01/08/2023", "2023-08-01"),  # 欧式格式 (日/月/年)
    ("08/01/2023", "2023-08-01"),  # 美式格式 (月/日/年)
    
    # 边界情况
    ("1999/12/31", "1999-12-31"),
    ("2000-01-01", "2000-01-01"),
    ("Jan-50", "2050-01-01"),  # 2050年
    ("Feb-49", "2049-02-01"),  # 2049年
    ("Mar-50", "1950-03-01"),  # 1950年 (因为<50)
    ("Apr-99", "1999-04-01"),
    ("May-00", "2000-05-01"),
    
    # 无效格式
    ("January-2023", None),  # 月份全名
    ("2023-10", None),       # 缺少日期
    ("Invalid", None),       # 完全无效
    ("", None),              # 空字符串
    ("32-13-2023", None),    # 无效日期
]

print("测试 parse_date 函数:")
print("=" * 60)

for date_str, expected in test_cases:
    result = parse_date(date_str)
    result_str = str(result) if result else "None"
    expected_str = str(expected) if expected else "None"
    
    # 检查测试结果
    status = "✓" if (result_str == expected_str) else "✗"
    
    print(f"{status} 输入: '{date_str}'")
    print(f"   预期: {expected_str}")
    print(f"   结果: {result_str}")
    print("-" * 60)

# 统计测试结果
total = len(test_cases)
passed = sum(1 for date_str, expected in test_cases 
             if (str(parse_date(date_str)) if parse_date(date_str) else None) == expected)

print(f"\n测试总结: {passed}/{total} 通过 ({passed/total*100:.1f}%)")