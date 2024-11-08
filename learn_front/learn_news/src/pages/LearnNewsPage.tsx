import { useEffect, useState } from "react";
import "../css/news-item.css";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import Title from '../components/Title'; // 引入新组件

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

export default function LearnNewsPage() {
  const [newsData, setNewsData] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await fetch("http://127.0.0.1:1234/recent_news/30");
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.statusText}`);
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
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-12 col-md-10 col-lg-8">
          <h1 className="text-center mb-4">新闻列表</h1>
          <ul className="list-unstyled">
            {newsData.map((newsItem) => (
              <li key={newsItem.id} className="mb-3">
                <a
                  href={newsItem.link}
                  className="news-title text-decoration-none"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <div className="news-item rounded p-3 d-flex flex-column flex-md-row justify-content-between align-items-md-start">
                    <div className="mb-2 mb-md-0 flex-grow-1 me-md-3">
                      <Title title={newsItem.title} /> {/* 使用新组件 */}
                    </div>
                    <span className="news-date text-md-end flex-shrink-0">
                      {formatChineseDate(newsItem.time)}
                    </span>
                  </div>
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
