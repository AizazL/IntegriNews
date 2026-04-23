import type { AnalysisDetail } from "../lib/api";

type ResultPanelProps = {
  result: AnalysisDetail | null;
  loading: boolean;
  error: string | null;
};

function meterClass(riskBand: string) {
  switch (riskBand.toLowerCase()) {
    case "critical":
      return "critical";
    case "high":
      return "high";
    case "moderate":
      return "moderate";
    default:
      return "low";
  }
}

export function ResultPanel({ result, loading, error }: ResultPanelProps) {
  if (loading) {
    return (
      <section className="panel panel-emphasis">
        <p className="panel-kicker">Analysis in progress</p>
        <h2>Interpreting article structure, tone, and signal strength.</h2>
        <div className="skeleton-stack" aria-label="Loading analysis result">
          <div className="skeleton-line" />
          <div className="skeleton-line wide" />
          <div className="skeleton-line" />
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="panel panel-error" role="alert">
        <p className="panel-kicker">Analysis blocked</p>
        <h2>{error}</h2>
        <p>Try adding article text directly or uploading a supported file.</p>
      </section>
    );
  }

  if (!result) {
    return (
      <section className="panel panel-muted">
        <p className="panel-kicker">Ready for review</p>
        <h2>No article analyzed yet.</h2>
        <p>Paste text, drop a file, or launch one of the sample articles to generate a credibility readout.</p>
      </section>
    );
  }

  return (
    <section className="panel panel-emphasis" aria-live="polite">
      <div className="result-header">
        <div>
          <p className="panel-kicker">Latest assessment</p>
          <h2>{result.verdict}</h2>
        </div>
        <span className={`risk-pill ${meterClass(result.risk_band)}`}>{result.risk_band}</span>
      </div>

      <div className="meter-shell" aria-label="Confidence meter">
        <div
          className={`meter-fill ${meterClass(result.risk_band)}`}
          style={{ width: `${result.confidence_percent}%` }}
        />
      </div>

      <div className="stat-grid">
        <article className="stat-card">
          <span className="stat-label">Verdict</span>
          <strong>{result.label === "fake" ? "Fake-leaning" : "Real-leaning"}</strong>
        </article>
        <article className="stat-card">
          <span className="stat-label">Confidence</span>
          <strong>{result.confidence_percent.toFixed(1)}%</strong>
        </article>
        <article className="stat-card">
          <span className="stat-label">Reading time</span>
          <strong>{result.input_stats.reading_time_minutes} min</strong>
        </article>
      </div>

      <div className="insight-grid">
        <article className="insight-card">
          <p className="panel-kicker">Advisory note</p>
          <p>{result.advisory_note}</p>
        </article>
        <article className="insight-card">
          <p className="panel-kicker">Input stats</p>
          <ul className="meta-list">
            <li>{result.input_stats.word_count} words</li>
            <li>{result.input_stats.character_count} characters</li>
            <li>Source: {result.source_name ?? result.source_type}</li>
          </ul>
        </article>
      </div>

      <div className="badge-group">
        {result.warning_badges.length ? (
          result.warning_badges.map((badge) => (
            <article key={badge.id} className={`badge-card ${badge.severity}`}>
              <p>{badge.label}</p>
              <span>{badge.description}</span>
            </article>
          ))
        ) : (
          <article className="badge-card quiet">
            <p>No heuristic warnings triggered</p>
            <span>The article structure did not trip any of the supplemental credibility heuristics.</span>
          </article>
        )}
      </div>
    </section>
  );
}
