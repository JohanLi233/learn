import React, { useEffect, useState } from "react";
import "./css/news-item.css";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";

dayjs.locale("zh-cn");
dayjs.extend(utc);

interface NewsItem {
  id: number;
  title: string;
  time: string;
  link: string;
}

const formatChineseDate = (mysqlDateString: string) => {
  const date = dayjs(mysqlDateString).utcOffset(0);
  const now = dayjs().utcOffset(0);

  if (date.isSame(now, "day")) {
    return "今天 " + date.format("HH:mm");
  } else if (date.isSame(now.subtract(1, "day"), "day")) {
    return "昨天 " + date.format("HH:mm");
  } else if (date.isSame(now, "year")) {
    return date.format("M月D日 HH:mm");
  } else {
    return date.format("YYYY年M月D日 HH:mm");
  }
};

const LearnNewsPage: React.FC = () => {
  const [newsData, setNewsData] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await fetch("http://127.0.0.1:1234/recent_news/30");
        if (!response.ok) {
          throw new Error(
            `Network response was not ok: ${response.statusText}`
          );
        }
        const data: NewsItem[] = await response.json();
        setNewsData(data);
      } catch (error) {
        console.error("Fetching news failed: ", error);
        setError((error as Error).message);
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  if (loading || error) {
    return (
      <div className="d-flex justify-content-center align-items-center">
        <div className="text-center">
          <div className="">{loading ? "Loading..." : `Error: ${error}`}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="d-flex justify-content-center align-items-center">
      <div className="text-center">
        <h1>新闻列表</h1>
        <ul className="list-unstyled">
          {newsData.map((newsItem) => (
            <li key={newsItem.id} className="mb-3">
              <a href={newsItem.link} className="news-title" target="_blank">
                <div className="news-item rounded p-3 text-left d-flex justify-content-between align-items-center">
                  {newsItem.title}
                  <span className="news-date">
                    {formatChineseDate(newsItem.time)}
                  </span>
                </div>
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LearnNewsPage;
