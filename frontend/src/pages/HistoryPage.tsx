import { useEffect, useState } from "react";
import { HistoryList } from "../components/HistoryList";
import { fetchAnalysis, fetchAnalyses, getExportUrl, type AnalysisDetail, type AnalysisListItem } from "../lib/api";

function buildSummary(items: AnalysisListItem[]) {
  const fakeCount = items.filter((item) => item.label === "fake").length;
  const realCount = items.length - fakeCount;
  const averageConfidence = items.length
    ? items.reduce((total, item) => total + item.confidence_percent, 0) / items.length
    : 0;

  return {
    total: items.length,
    fakeCount,
    realCount,
    averageConfidence
  };
}

export function HistoryPage() {
  const [items, setItems] = useState<AnalysisListItem[]>([]);
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [selected, setSelected] = useState<AnalysisDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;

    async function loadAnalyses() {
      setLoading(true);
      setError(null);

      try {
        const nextItems = await fetchAnalyses();
        if (!active) {
          return;
        }

        setItems(nextItems);
        if (nextItems[0]) {
          setSelectedId(nextItems[0].id);
        }
      } catch (loadError) {
        if (!active) {
          return;
        }
        setError(loadError instanceof Error ? loadError.message : "Unable to load analysis history.");
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadAnalyses();

    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!selectedId) {
      setSelected(null);
      return;
    }

    let active = true;

    async function loadSelected() {
      try {
        const detail = await fetchAnalysis(selectedId);
        if (active) {
          setSelected(detail);
        }
      } catch {
        if (active) {
          setSelected(null);
        }
      }
    }

    void loadSelected();

    return () => {
      active = false;
    };
  }, [selectedId]);

  const summary = buildSummary(items);

  return (
    <div className="page-stack">
      <section className="panel analytics-panel">
        <div className="section-header">
          <div>
            <p className="panel-kicker">Archive overview</p>
            <h1>Saved analysis trends</h1>
          </div>
          <a className="cta-secondary" href={getExportUrl()}>
            Export CSV
          </a>
        </div>
        <div className="stat-grid">
          <article className="stat-card">
            <span className="stat-label">Total analyses</span>
            <strong>{summary.total}</strong>
          </article>
          <article className="stat-card">
            <span className="stat-label">Fake-leaning</span>
            <strong>{summary.fakeCount}</strong>
          </article>
          <article className="stat-card">
            <span className="stat-label">Real-leaning</span>
            <strong>{summary.realCount}</strong>
          </article>
          <article className="stat-card">
            <span className="stat-label">Average confidence</span>
            <strong>{summary.averageConfidence.toFixed(1)}%</strong>
          </article>
        </div>
      </section>

      <HistoryList
        items={items}
        selectedId={selectedId}
        onSelect={setSelectedId}
        selected={selected}
        loading={loading}
        error={error}
      />
    </div>
  );
}
