// App.tsx
import { Route, Routes } from "react-router-dom";
import LearnNewsPage from "./LearnNewsPage";
import Navbar from "./Navbar";
import "./css/App.css";
import Home from "./Home";

function App() {
  return (
    <div className="app-container" style={{ minHeight: "100vh" }}>
      <Navbar />
      <div className="content-container transparent-container text-white p-20">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/learn-news" element={<LearnNewsPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;