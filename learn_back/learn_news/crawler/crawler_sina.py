import logging
from datetime import datetime

import pymysql
import requests
from bs4 import BeautifulSoup
from config import db_config

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
base_api_url = "https://feed.mix.sina.com.cn/api/roll/get"
base_url = "https://finance.sina.com.cn"

# 请求头，模拟浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/112.0.0.0 Safari/537.36",
    "Referer": "https://finance.sina.com.cn/",
    "Accept": "application/json, text/javascript, */*; q=0.01",
}


def fetch_page(url, params=None):
    """获取网页内容或API响应"""
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        # 判断是否为JSON响应
        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()
        else:
            response.encoding = response.apparent_encoding
            return response.text
    except requests.RequestException as e:
        logging.error(f"请求失败: {url} - {e}")
        return None


def parse_main_page(json_data):
    """解析主页面的JSON数据，提取新闻项"""
    news_items = []
    try:
        if json_data.get("result", {}).get("status", {}).get("code") != 0:
            logging.error("API返回状态码不为0，解析中止。")
            return news_items

        data_list = json_data.get("result", {}).get("data", [])
        for item in data_list:
            category = item.get("channelid", "")
            title = item.get("title", "")
            link = item.get("url", "")
            # 将时间戳转换为可读格式
            timestamp = int(item.get("intime", "0"))
            time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            news_items.append(
                {"category": category, "title": title, "link": link, "time": time_str}
            )
    except Exception as e:
        logging.error(f"解析JSON数据时出错: {e}")
    return news_items


def parse_detail_page(html):
    """解析详情页面，提取内容"""
    soup = BeautifulSoup(html, "html.parser")
    # 根据示例HTML，内容可能在多个<p>标签中
    content_paragraphs = soup.find_all("p")
    content_paragraphs = content_paragraphs[:-8]
    content = "\n".join([p.get_text(strip=True) for p in content_paragraphs])
    # 处理图片描述等非文本内容（可选）
    # print(content)
    return content


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


def main():
    total_saved = 0
    for page in range(1, 30):  # 前30页
        params = {"pageid": 153, "lid": 2509, "k": "", "num": 50, "page": page}
        logging.info(f"开始处理第 {page} 页 - URL: {base_api_url} with params {params}")

        # 获取API响应
        json_data = fetch_page(base_api_url, params=params)
        if not json_data:
            logging.warning(f"无法获取第 {page} 页的数据，跳过该页。")
            continue

        # 解析主页面，获取新闻列表
        news_list = parse_main_page(json_data)
        logging.info(f"第 {page} 页找到 {len(news_list)} 条新闻")

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
            # time.sleep(0.1)  # 根据需要调整暂停时间

        # 可选：暂停一段时间，以控制抓取速度
        # time.sleep(1)  # 例如，每处理一页暂停1秒

    # 关闭数据库连接
    cursor.close()
    connection.close()
    logging.info(f"爬虫任务完成。共保存 {total_saved} 条新闻。")


if __name__ == "__main__":
    main()
