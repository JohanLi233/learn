import React, { useEffect, useState } from 'react';

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
        const response = await fetch('http://127.0.0.1:1234/recent_news'); // 确保你的API URL是正确的
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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Learn News Page</h1>
      <ul>
        {newsData.map((newsItem) => (
          <li key={newsItem.id}>{newsItem.title}</li> // 使用更可靠的 `id` 作为 key
        ))}
      </ul>
    </div>
  );
};

export default LearnNewsPage;
