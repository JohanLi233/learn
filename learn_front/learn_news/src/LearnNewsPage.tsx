import React, { useEffect, useState } from "react";
import "./css/news-item.css";

interface NewsItem {
  id: number;
  title: string;
  // 你可以在这里添加更多字段
}

const LearnNewsPage: React.FC = () => {
  const [newsData, setNewsData] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        console.log("Fetching news...");
        const response = await fetch("http://127.0.0.1:1234/recent_news");
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
      <div className="d-flex justify-content-center align-items-center vh-10 mt-4">
        <div className="text-center">
          <h1>Learn News Page</h1>
          <div className="">
            {loading ? "Loading..." : `Error: ${error}`}
          </div>
        </div>
      </div>
    );
  }


  return (
    <div className="d-flex justify-content-center align-items-center vh-10 mt-4">
      <div className="text-center">
        <h1>Learn News Page</h1>
        <ul className="list-unstyled">
          {newsData.map((newsItem) => (
            <li key={newsItem.id} className="mb-3">
              <div className="news-item rounded p-3 text-left">{newsItem.title}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LearnNewsPage;
