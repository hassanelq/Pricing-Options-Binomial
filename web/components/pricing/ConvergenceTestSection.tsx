import Plot from "@/components/Plot";

interface ConvergenceTestSectionProps {
  bsPrice: number;
  binomialConvergence: Array<{ steps: number; price: number; error: number }>;
  trinomialConvergence: Array<{ steps: number; price: number; error: number }>;
}

export default function ConvergenceTestSection({
  bsPrice,
  binomialConvergence,
  trinomialConvergence,
}: ConvergenceTestSectionProps) {
  // Prices now come directly from API
  const binomialPrices = binomialConvergence.map((c) => ({
    steps: c.steps,
    price: c.price,
  }));

  const trinomialPrices = trinomialConvergence.map((c) => ({
    steps: c.steps,
    price: c.price,
  }));

  // Get all unique steps
  const allSteps = Array.from(
    new Set([
      ...binomialPrices.map((p) => p.steps),
      ...trinomialPrices.map((p) => p.steps),
    ])
  ).sort((a, b) => a - b);

  // Prepare plot data with all three lines
  const plotData = [
    {
      x: allSteps,
      y: allSteps.map(() => bsPrice),
      type: "scatter" as const,
      mode: "lines" as const,
      name: "Black-Scholes Price",
      line: { color: "#ef4444", width: 2, dash: "dash" },
    },
    {
      x: binomialPrices.map((p) => p.steps),
      y: binomialPrices.map((p) => p.price),
      type: "scatter" as const,
      mode: "lines+markers" as const,
      name: "Binomial Price",
      line: { color: "#22c55e", width: 1 },
      marker: { size: 3 },
    },
    {
      x: trinomialPrices.map((p) => p.steps),
      y: trinomialPrices.map((p) => p.price),
      type: "scatter" as const,
      mode: "lines+markers" as const,
      name: "Trinomial Price",
      line: { color: "#f59e0b", width: 2 },
      marker: { size: 3 },
    },
  ];

  const plotLayout = {
    title: {
      text: "Convergence to Black-Scholes",
      font: { size: 20, color: "#1f2937" },
    },
    xaxis: {
      title: "Number of Steps",
      gridcolor: "#e5e7eb",
    },
    yaxis: {
      title: "Call Option Price",
      gridcolor: "#e5e7eb",
    },
    plot_bgcolor: "#ffffff",
    paper_bgcolor: "#ffffff",
    showlegend: true,
    legend: {
      x: 1,
      xanchor: "right",
      y: 1,
      bgcolor: "rgba(255, 255, 255, 0.8)",
      bordercolor: "#d1d5db",
      borderwidth: 1,
    },
    hovermode: "x unified" as const,
    margin: { t: 60, b: 60, l: 60, r: 20 },
  };

  return (
    <div className="bg-gradient-to-br from-slate-50 to-gray-50 dark:from-slate-950/20 dark:to-gray-950/20 rounded-lg shadow-lg p-6 border border-slate-200 dark:border-slate-800">
      <h2 className="text-2xl font-bold mb-6 text-slate-900 dark:text-slate-100">
        Tests - Convergence Analysis
      </h2>

      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
        <Plot
          data={plotData}
          layout={plotLayout}
          config={{ responsive: true, displayModeBar: true }}
          style={{ width: "100%", height: "700px" }}
        />
      </div>

      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-red-50 dark:bg-red-950/20 rounded-lg p-4 border border-red-200 dark:border-red-800">
          <p className="text-sm font-semibold text-red-900 dark:text-red-100 mb-1">
            Black-Scholes Price
          </p>
          <p className="text-2xl font-bold text-red-600 dark:text-red-400">
            ${bsPrice.toFixed(4)}
          </p>
          <p className="text-xs text-red-600 dark:text-red-400 mt-1">
            Analytical solution
          </p>
        </div>

        <div className="bg-green-50 dark:bg-green-950/20 rounded-lg p-4 border border-green-200 dark:border-green-800">
          <p className="text-sm font-semibold text-green-900 dark:text-green-100 mb-1">
            Binomial Convergence
          </p>
          <p className="text-2xl font-bold text-green-600 dark:text-green-400">
            {binomialConvergence[binomialConvergence.length - 1]?.error.toFixed(
              3
            )}
            %
          </p>
          <p className="text-xs text-green-600 dark:text-green-400 mt-1">
            Final error at{" "}
            {binomialConvergence[binomialConvergence.length - 1]?.steps} steps
          </p>
        </div>

        <div className="bg-amber-50 dark:bg-amber-950/20 rounded-lg p-4 border border-amber-200 dark:border-amber-800">
          <p className="text-sm font-semibold text-amber-900 dark:text-amber-100 mb-1">
            Trinomial Convergence
          </p>
          <p className="text-2xl font-bold text-amber-600 dark:text-amber-400">
            {trinomialConvergence[
              trinomialConvergence.length - 1
            ]?.error.toFixed(3)}
            %
          </p>
          <p className="text-xs text-amber-600 dark:text-amber-400 mt-1">
            Final error at{" "}
            {trinomialConvergence[trinomialConvergence.length - 1]?.steps} steps
          </p>
        </div>
      </div>
    </div>
  );
}
