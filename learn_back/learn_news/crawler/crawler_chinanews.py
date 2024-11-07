import logging
from datetime import datetime, timedelta

import pymysql
import requests
from bs4 import BeautifulSoup
from db_config import db_config

# 配置日志，输出到文件并同时输出到控制台
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建日志格式
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# 创建文件处理器，日志将写入到 'crawler.log' 文件中
file_handler = logging.FileHandler("crawler.log", encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# 连接到MySQL数据库
try:
    connection = pymysql.connect(**db_config)
    logging.info("成功连接到MySQL数据库")
except pymysql.MySQLError as e:
    logging.error(f"连接到MySQL数据库失败: {e}")
    exit(1)

# 创建一个游标对象
cursor = connection.cursor()

# 基础URL
base_url = "https://www.chinanews.com.cn"

# 请求头，模拟浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/112.0.0.0 Safari/537.36"
}


def fetch_page(url):
    """获取网页内容"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except requests.RequestException as e:
        logging.error(f"请求失败: {url} - {e}")
        return None


def parse_main_page(html, year):
    """解析主页面，提取新闻项"""
    soup = BeautifulSoup(html, "html.parser")
    news_items = []

    # 根据用户描述，分类在 div dd_lm 中，标题和链接在 dd_bt 中，时间在 dd_time 中
    categories = soup.find_all("div", class_="dd_lm")
    titles = soup.find_all("div", class_="dd_bt")
    times = soup.find_all("div", class_="dd_time")

    # 确保所有列表长度一致
    if not (len(categories) == len(titles) == len(times)):
        logging.warning("分类、标题和时间的数量不一致，可能存在解析错误。")

    for cat, title, time_ in zip(categories, titles, times):
        category = cat.get_text(strip=True)
        title_tag = title.find("a")
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            href = title_tag.get("href")
            if href.startswith("http"):
                link = href
            else:
                link = base_url + href
        else:
            title_text = ""
            link = ""
        time_text = time_.get_text(strip=True)
        datetime_str = f"{year}-{time_text}"
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        formatted_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        news_items.append(
            {
                "category": category,
                "title": title_text,
                "link": link,
                "time": formatted_time,
            }
        )
    return news_items


def parse_detail_page(html):
    """解析详情页面，提取内容"""
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", class_="left_zw")
    if content_div:
        # 获取所有文本内容，并去除多余的空白字符
        content = content_div.get_text(separator="\n", strip=True)
        return content
    else:
        logging.warning("未找到内容 div 'left_zw'")
        return ""


def news_exists(link):
    """检查新闻是否已存在于数据库中"""
    sql = "SELECT COUNT(*) FROM news WHERE link = %s"
    try:
        cursor.execute(sql, (link,))
        count = cursor.fetchone()[0]
        return count > 0
    except pymysql.MySQLError as e:
        logging.error(f"查询数据库失败: {e}")
        return False


def save_to_mysql(data):
    """将数据保存到MySQL数据库"""
    # 先检查是否存在
    if news_exists(data["link"]):
        logging.info(f"新闻已存在，跳过: {data['title']}")
        return

    sql = """
    INSERT INTO news (category, title, link, time, content)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(
            sql,
            (
                data["category"],
                data["title"],
                data["link"],
                data["time"],
                data["content"],
            ),
        )
        connection.commit()
        logging.info(f"已保存: {data['title']}")
    except pymysql.MySQLError as e:
        logging.error(f"保存到数据库失败: {e}")
        connection.rollback()


def generate_dates(year):
    """生成指定年份的所有日期"""
    start_date = datetime(year, 11, 7)
    end_date = datetime(year, 11, 7)
    delta = timedelta(days=1)
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += delta


def main():
    year = 2024
    date_generator = generate_dates(year)
    total_saved = 0
    for date in date_generator:
        date_str = date.strftime("%Y/%m%d")
        target_url = f"https://www.chinanews.com.cn/scroll-news/{date_str}/news.shtml"
        logging.info(f"开始处理日期: {date.strftime('%Y-%m-%d')} - URL: {target_url}")

        # 获取主页面内容
        main_page = fetch_page(target_url)
        if not main_page:
            logging.warning(f"无法获取主页面内容: {target_url}，跳过该日期。")
            continue

        # 解析主页面，获取新闻列表
        news_list = parse_main_page(main_page, year)
        logging.info(f"找到 {len(news_list)} 条新闻")

        for news in news_list:
            if not news["link"]:
                logging.warning("跳转链接为空，跳过此新闻。")
                continue

            # 获取详情页面内容
            detail_page = fetch_page(news["link"])
            if not detail_page:
                logging.warning(f"无法获取详情页面: {news['link']}")
                continue

            # 解析详情页面，获取内容
            content = parse_detail_page(detail_page)
            news["content"] = content

            # 保存到数据库
            save_to_mysql(news)
            total_saved += 1

            # 为了避免过于频繁的请求，暂停一段时间
            # time.sleep(0.01)  # 根据需要调整暂停时间

        # 可选：暂停一天或其他逻辑，以控制抓取速度
        # time.sleep(5)  # 例如，每处理一天暂停5秒

    # 关闭数据库连接
    cursor.close()
    connection.close()
    logging.info(f"爬虫任务完成。共保存 {total_saved} 条新闻。")


if __name__ == "__main__":
    main()
