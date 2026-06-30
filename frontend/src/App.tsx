import { useState } from "react";

import { AdminPage } from "./pages/AdminPage";
import { AnalyticsPage } from "./pages/AnalyticsPage";
import { SurveyPage } from "./pages/SurveyPage";
import "./styles/app.css";

type View = "survey" | "analytics" | "admin";

export function App() {
  const [view, setView] = useState<View>("survey");

  return (
    <main className="wt-app">
      <header className="wt-header">
        <div>
          <h1 className="wt-title">WaveTracker</h1>
          <p className="wt-subtitle">Wi-Fi Survey and Administration Workspace</p>
        </div>
        <nav className="wt-nav">
          <button
            type="button"
            className={view === "survey" ? "wt-active" : undefined}
            onClick={() => setView("survey")}
          >
            Survey
          </button>
          <button
            type="button"
            className={view === "analytics" ? "wt-active" : undefined}
            onClick={() => setView("analytics")}
          >
            Analytics
          </button>
          <button
            type="button"
            className={view === "admin" ? "wt-active" : undefined}
            onClick={() => setView("admin")}
          >
            Admin
          </button>
        </nav>
      </header>
      <section className="wt-view">
        {view === "survey" && <SurveyPage />}
        {view === "analytics" && <AnalyticsPage />}
        {view === "admin" && <AdminPage />}
      </section>
    </main>
  );
}
