import { Route, Routes } from "react-router-dom";
import { NavBar } from "./components/NavBar";
import { AnalyzePage } from "./pages/AnalyzePage";
import { HistoryPage } from "./pages/HistoryPage";
import { LandingPage } from "./pages/LandingPage";

export default function App() {
  return (
    <div className="app-shell">
      <div className="backdrop backdrop-top" />
      <div className="backdrop backdrop-bottom" />
      <NavBar />
      <main className="content-shell">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/analyze" element={<AnalyzePage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </main>
    </div>
  );
}
