export default function PageFoot() {
  return (
    <footer className="d-flex justify-content-end p-3">
      <div
        className="bg-dark bg-opacity-75 p-3 rounded shadow-sm text-end text-white position-fixed bottom-0"
        style={{ maxWidth: "350px", marginRight: "auto" }}
      >
        <a
          href="https://github.com/JohanLi233"
          target="_blank"
          rel="noopener noreferrer"
          style={{ fontSize: "0.8rem", color: "gray" }}
        >
          Powered by ©JohanLi233
        </a>
      </div>
    </footer>
  );
}
