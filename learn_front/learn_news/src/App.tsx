// App.tsx
import { Route, Routes } from "react-router-dom";
import { BrowserRouter as Router } from "react-router-dom";
import LearnNewsPage from "./pages/LearnNewsPage";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import PageFoot from "./components/PageFoot";

import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css";

export default function App() {
  return (
    <Router>
      <Navbar />
      <div className="app-container d-flex flex-column min-vh-100">
        <div className="content-container flex-grow-1 transparent-container text-white p-20">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/learn-news" element={<LearnNewsPage />} />
          </Routes>
        </div>
      </div>
      <PageFoot />
    </Router>
  );
}
