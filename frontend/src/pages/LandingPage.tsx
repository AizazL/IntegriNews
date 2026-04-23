import { Link } from "react-router-dom";

export function LandingPage() {
  return (
    <div className="page-stack">
      <section className="panel title-panel">
        <h1>Credibility triage for fast-moving newsrooms.</h1>
      </section>

      <section className="panel process-panel">
        <div className="process-heading">
          <p className="panel-kicker">How It Works</p>
          <h2>From raw article text to a saved credibility review.</h2>
        </div>

        <div className="process-rail" aria-label="How IntegriNews works">
          <div className="process-track" aria-hidden="true" />

          <div className="process-step">
            <span className="process-dot" aria-hidden="true" />
            <strong>Ingest</strong>
            <p>Paste article text or upload a PDF, DOCX, or TXT file.</p>
          </div>

          <div className="process-step">
            <span className="process-dot" aria-hidden="true" />
            <strong>Assess</strong>
            <p>Review the verdict, confidence, risk band, and warning cues.</p>
          </div>

          <div className="process-step">
            <span className="process-dot" aria-hidden="true" />
            <strong>Archive</strong>
            <p>Save the result, revisit past analyses, and export the history.</p>
          </div>
        </div>
      </section>

      <section className="panel support-panel">
        <div className="support-copy">
          <p className="panel-kicker">Overview</p>
          <p className="hero-text">
            IntegriNews helps reviewers assess suspicious articles with structured verdicts, confidence framing,
            saved analysis history, and evidence-oriented heuristics.
          </p>
        </div>

        <div className="support-actions">
          <div className="hero-actions">
            <Link to="/analyze" className="cta-primary">
              Launch Analyzer
            </Link>
            <Link to="/history" className="cta-secondary">
              View Archive
            </Link>
          </div>
          <p className="hero-note">Paste article text or upload a PDF, DOCX, or TXT file to start a review.</p>
        </div>
      </section>
    </div>
  );
}
