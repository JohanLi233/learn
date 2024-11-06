// App.tsx
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LearnNewsPage from "./LearnNewsPage";
import Navbar from "./Navbar";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  return (
    <div className="bg-dark text-white p-20">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<h1>Developing</h1>} />
          <Route path="/learn-news" element={<LearnNewsPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
