import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "bootstrap/dist/css/bootstrap.min.css";
import "./css/index.css";
import App from "./App.tsx";
import { BrowserRouter as Router } from 'react-router-dom';

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Router>
      <App />
    </Router>
  </StrictMode>
);
