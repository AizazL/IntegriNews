import { MemoryRouter } from "react-router-dom";
import { render, screen, waitFor } from "@testing-library/react";
import { HistoryPage } from "./HistoryPage";

vi.mock("../lib/api", async () => {
  const actual = await vi.importActual<typeof import("../lib/api")>("../lib/api");
  return {
    ...actual,
    fetchAnalyses: vi.fn(),
    fetchAnalysis: vi.fn(),
    getExportUrl: () => "http://localhost:8000/analyses/export.csv"
  };
});

import { fetchAnalyses, fetchAnalysis } from "../lib/api";

const mockedFetchAnalyses = vi.mocked(fetchAnalyses);
const mockedFetchAnalysis = vi.mocked(fetchAnalysis);

describe("HistoryPage", () => {
  beforeEach(() => {
    mockedFetchAnalyses.mockReset();
    mockedFetchAnalysis.mockReset();
  });

  test("shows loading first and then an empty state", async () => {
    mockedFetchAnalyses.mockResolvedValue([]);

    render(
      <MemoryRouter>
        <HistoryPage />
      </MemoryRouter>
    );

    expect(screen.getByText(/collecting saved analyses/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/analysis archive is empty/i)).toBeInTheDocument());
  });

  test("shows an error state when history loading fails", async () => {
    mockedFetchAnalyses.mockRejectedValue(new Error("Backend offline"));

    render(
      <MemoryRouter>
        <HistoryPage />
      </MemoryRouter>
    );

    await waitFor(() => expect(screen.getByText("Backend offline")).toBeInTheDocument());
    expect(mockedFetchAnalysis).not.toHaveBeenCalled();
  });
});
