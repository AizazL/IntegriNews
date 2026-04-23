import { MemoryRouter } from "react-router-dom";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { AnalyzePage } from "./AnalyzePage";

vi.mock("../lib/api", async () => {
  const actual = await vi.importActual<typeof import("../lib/api")>("../lib/api");
  return {
    ...actual,
    analyzeArticle: vi.fn()
  };
});

import { analyzeArticle } from "../lib/api";

const mockedAnalyzeArticle = vi.mocked(analyzeArticle);

describe("AnalyzePage", () => {
  beforeEach(() => {
    mockedAnalyzeArticle.mockReset();
  });

  test("validates required title and content before submit", async () => {
    const user = userEvent.setup();
    render(
      <MemoryRouter>
        <AnalyzePage />
      </MemoryRouter>
    );

    await user.click(screen.getByRole("button", { name: /run analysis/i }));

    expect(
      screen.getByText(/add a title and either article text or a supported file before running analysis/i)
    ).toBeInTheDocument();
    expect(mockedAnalyzeArticle).not.toHaveBeenCalled();
  });

  test("shows selected upload filename and renders analysis results", async () => {
    const user = userEvent.setup();
    mockedAnalyzeArticle.mockResolvedValue({
      id: 1,
      created_at: new Date().toISOString(),
      title: "Investigative brief",
      label: "real",
      verdict: "Strong legitimate-reporting signal",
      risk_band: "Low",
      fake_probability: 0.11,
      confidence_percent: 89.0,
      advisory_note: "Use this as one signal among many.",
      input_stats: {
        word_count: 120,
        character_count: 680,
        reading_time_minutes: 1
      },
      warning_badges: [],
      source_type: "upload",
      source_name: "brief.txt",
      article_text: "A reported article body"
    });

    render(
      <MemoryRouter>
        <AnalyzePage />
      </MemoryRouter>
    );

    await user.type(screen.getByPlaceholderText(/enter the article headline/i), "Investigative brief");
    await user.type(screen.getByPlaceholderText(/paste the article body/i), "A reported article body");

    const file = new File(["A reported article body"], "brief.txt", { type: "text/plain" });
    await user.upload(screen.getByLabelText(/upload article file/i), file);

    expect(screen.getByText("Attached: brief.txt")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /run analysis/i }));

    await waitFor(() => expect(mockedAnalyzeArticle).toHaveBeenCalled());
    expect(screen.getByText(/strong legitimate-reporting signal/i)).toBeInTheDocument();
    expect(screen.getByText(/89.0%/i)).toBeInTheDocument();
  });
});
