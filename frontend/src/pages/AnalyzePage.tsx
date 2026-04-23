import { ChangeEvent, DragEvent, FormEvent, useDeferredValue, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { sampleArticles } from "../data/sampleArticles";
import { analyzeArticle, type AnalysisDetail } from "../lib/api";
import { ResultPanel } from "../components/ResultPanel";

function estimateWordCount(text: string) {
  const trimmed = text.trim();
  if (!trimmed) {
    return 0;
  }

  return trimmed.split(/\s+/).length;
}

export function AnalyzePage() {
  const [searchParams] = useSearchParams();
  const [title, setTitle] = useState("");
  const [body, setBody] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [inlineError, setInlineError] = useState<string | null>(null);
  const [resultError, setResultError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisDetail | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const deferredBody = useDeferredValue(body);

  useEffect(() => {
    const slug = searchParams.get("sample");
    if (!slug) {
      return;
    }

    const article = sampleArticles.find((item) => item.slug === slug);
    if (article) {
      setTitle(article.title);
      setBody(article.body);
      setFile(null);
      setInlineError(null);
      setResultError(null);
    }
  }, [searchParams]);

  function onFileSelection(nextFile: File | null) {
    setFile(nextFile);
    setInlineError(null);
  }

  function handleFileInput(event: ChangeEvent<HTMLInputElement>) {
    onFileSelection(event.target.files?.[0] ?? null);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    setDragActive(false);
    onFileSelection(event.dataTransfer.files?.[0] ?? null);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!title.trim() || (!body.trim() && !file)) {
      setInlineError("Add a title and either article text or a supported file before running analysis.");
      return;
    }

    setLoading(true);
    setInlineError(null);
    setResultError(null);

    try {
      const analysis = await analyzeArticle({ title, body, file });
      setResult(analysis);
    } catch (submissionError) {
      setResultError(submissionError instanceof Error ? submissionError.message : "Unable to analyze the article.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-stack analysis-page">
      <section className="panel analysis-header">
        <div>
          <p className="panel-kicker">Analysis workspace</p>
          <h1>Build a credibility assessment from text or uploads.</h1>
        </div>
        <div className="live-meta">
          <span>{estimateWordCount(deferredBody)} draft words</span>
          <span>{file ? `Attached: ${file.name}` : "No file attached"}</span>
        </div>
      </section>

      <div className="analysis-layout">
        <form className="panel composer" onSubmit={handleSubmit}>
          <label className="field">
            <span>Article title</span>
            <input
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="Enter the article headline or summary line"
            />
          </label>

          <label className="field">
            <span>Article body</span>
            <textarea
              value={body}
              onChange={(event) => setBody(event.target.value)}
              placeholder="Paste the article body, claim, or transcript excerpt here"
              rows={14}
            />
          </label>

          <label
            className={dragActive ? "dropzone active" : "dropzone"}
            onDragOver={(event) => {
              event.preventDefault();
              setDragActive(true);
            }}
            onDragLeave={() => setDragActive(false)}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept=".txt,.docx,.pdf"
              onChange={handleFileInput}
              aria-label="Upload article file"
            />
            <strong>Drop `.txt`, `.docx`, or `.pdf` here</strong>
            <span>{file ? file.name : "File text will be combined with anything pasted above."}</span>
          </label>

          <button type="submit" className="cta-primary">
            Run Analysis
          </button>

          {inlineError ? (
            <p className="inline-error" role="alert">
              {inlineError}
            </p>
          ) : null}
        </form>

        <ResultPanel result={result} loading={loading} error={resultError} />
      </div>
    </div>
  );
}
