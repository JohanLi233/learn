export default function NewsTitle({ title }: { title: string }) {
  return (
    <div
      style={{
        wordBreak: "break-word", // 允许在任何字母间换行
        overflowWrap: "break-word", // 在必要时换行
        whiteSpace: "normal", // 正常处理空格
      }}
    >
      {title}
    </div>
  );
}
