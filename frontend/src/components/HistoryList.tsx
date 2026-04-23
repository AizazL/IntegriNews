import type { AnalysisDetail, AnalysisListItem } from "../lib/api";

type HistoryListProps = {
  items: AnalysisListItem[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  selected: AnalysisDetail | null;
  loading: boolean;
  error: string | null;
};

export function HistoryList({
  items,
  selectedId,
  onSelect,
  selected,
  loading,
  error
}: HistoryListProps) {
  if (loading) {
    return (
      <section className="panel">
        <p className="panel-kicker">History loading</p>
        <h2>Collecting saved analyses.</h2>
      </section>
    );
  }

  if (error) {
    return (
      <section className="panel panel-error" role="alert">
        <p className="panel-kicker">History unavailable</p>
        <h2>{error}</h2>
      </section>
    );
  }

  if (!items.length) {
    return (
      <section className="panel panel-muted">
        <p className="panel-kicker">No saved work</p>
        <h2>Your analysis archive is empty.</h2>
        <p>Run an article through the analyzer to populate trends, exports, and detailed history.</p>
      </section>
    );
  }

  return (
    <div className="history-layout">
      <section className="panel">
        <div className="section-header">
          <div>
            <p className="panel-kicker">Saved analyses</p>
            <h2>Recent newsroom reviews</h2>
          </div>
        </div>
        <div className="history-list">
          {items.map((item) => (
            <button
              type="button"
              key={item.id}
              className={item.id === selectedId ? "history-item active" : "history-item"}
              onClick={() => onSelect(item.id)}
            >
              <span className="history-item-topline">
                <strong>{item.title}</strong>
                <em>{new Date(item.created_at).toLocaleString()}</em>
              </span>
              <span className="history-item-meta">
                <span>{item.verdict}</span>
                <span>{item.confidence_percent.toFixed(1)}% confidence</span>
              </span>
              <p>{item.article_preview}</p>
            </button>
          ))}
        </div>
      </section>

      <section className="panel panel-emphasis">
        <p className="panel-kicker">Selected analysis</p>
        {selected ? (
          <>
            <h2>{selected.title}</h2>
            <p className="detail-summary">
              {selected.verdict} / {selected.confidence_percent.toFixed(1)}% confidence
            </p>
            <div className="badge-group compact">
              {selected.warning_badges.map((badge) => (
                <article key={badge.id} className={`badge-card ${badge.severity}`}>
                  <p>{badge.label}</p>
                  <span>{badge.description}</span>
                </article>
              ))}
            </div>
            <div className="article-detail">
              <p className="panel-kicker">Captured article text</p>
              <p>{selected.article_text}</p>
            </div>
          </>
        ) : (
          <p>Select an analysis to inspect the full saved result.</p>
        )}
      </section>
    </div>
  );
}
