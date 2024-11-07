// App.tsx
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LearnNewsPage from "./LearnNewsPage";
import Navbar from "./Navbar";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/App.css"
import Home from "./Home";

function App() {
  return (
    <div className="transparent-container text-white p-20" style={{ minHeight: '100vh' }}>
      <Router>
        <div className="container mt-5 pt-4">
          <Navbar />
        </div>
        <Routes>
          <Route
            path="/"
            element={
              <Home />
            }
          />
          <Route path="/learn-news" element={<LearnNewsPage />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
