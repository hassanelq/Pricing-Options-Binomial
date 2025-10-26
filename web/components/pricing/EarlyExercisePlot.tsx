"use client";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface BoundaryPoint {
  time: number;
  stock_price: number;
  time_to_maturity: number;
}

interface PutEarlyExercisePlotProps {
  binomialBoundary: BoundaryPoint[];
  trinomialBoundary: BoundaryPoint[];
  strikePrice: number;
  spotPrice: number;
}

export function PutEarlyExercisePlot({
  binomialBoundary,
  trinomialBoundary,
  strikePrice,
  spotPrice,
}: PutEarlyExercisePlotProps) {
  // Prepare data for plotting
  const binomialTimes = binomialBoundary.map((p) => p.time);
  const binomialPrices = binomialBoundary.map((p) => p.stock_price);

  const trinomialTimes = trinomialBoundary.map((p) => p.time);
  const trinomialPrices = trinomialBoundary.map((p) => p.stock_price);

  const traces: any[] = [];

  // Add binomial put boundary
  if (binomialBoundary.length > 0) {
    traces.push({
      x: binomialTimes,
      y: binomialPrices,
      type: "scatter",
      mode: "lines+markers",
      name: "Binomial",
      line: { color: "#ef4444", width: 3 },
      marker: { size: 6 },
    });
  }

  // Add trinomial put boundary
  if (trinomialBoundary.length > 0) {
    traces.push({
      x: trinomialTimes,
      y: trinomialPrices,
      type: "scatter",
      mode: "lines+markers",
      name: "Trinomial",
      line: { color: "#f97316", width: 2 },
      marker: { size: 4, symbol: "square" },
    });
  }

  // Add strike price and spot price reference lines
  const maxTime = Math.max(...binomialTimes, ...trinomialTimes, 0);

  if (maxTime > 0) {
    traces.push({
      x: [0, maxTime],
      y: [strikePrice, strikePrice],
      type: "scatter",
      mode: "lines",
      name: "Strike Price",
      line: { color: "#666", width: 2, dash: "dot" },
      showlegend: true,
    });

    traces.push({
      x: [0, maxTime],
      y: [spotPrice, spotPrice],
      type: "scatter",
      mode: "lines",
      name: "Current Spot",
      line: { color: "#22c55e", width: 2, dash: "dashdot" },
      showlegend: true,
    });
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">
        Early Exercise Boundary - American Put
      </h2>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        Shows the critical stock prices below which early exercise becomes
        optimal for American put options. Exercise the put when the stock price
        drops below the boundary.
      </p>

      {traces.length > 2 ? (
        <Plot
          data={traces}
          layout={{
            autosize: true,
            xaxis: {
              title: { text: "Time (years)" },
              gridcolor: "#e5e7eb",
              zeroline: false,
            },
            yaxis: {
              title: { text: "Stock Price ($)" },
              gridcolor: "#e5e7eb",
              zeroline: false,
            },
            legend: {
              x: 1,
              xanchor: "right",
              y: 1,
              bgcolor: "rgba(255,255,255,0.8)",
              bordercolor: "#e5e7eb",
              borderwidth: 1,
            },
            hovermode: "closest",
            plot_bgcolor: "#ffffff",
            paper_bgcolor: "#ffffff",
            margin: { t: 20, r: 20, b: 60, l: 60 },
          }}
          config={{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ["lasso2d", "select2d"],
          }}
          style={{ width: "100%", height: "500px" }}
        />
      ) : (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">
            No early exercise boundary detected for puts.
          </p>
          <ul className="mt-4 text-left max-w-md mx-auto list-disc list-inside">
            <li>The put option may be far out-of-the-money</li>
            <li>Try increasing the number of tree steps</li>
          </ul>
        </div>
      )}
    </div>
  );
}

interface CallEarlyExercisePlotProps {
  binomialBoundary: BoundaryPoint[];
  trinomialBoundary: BoundaryPoint[];
  strikePrice: number;
  spotPrice: number;
}

export function CallEarlyExercisePlot({
  binomialBoundary,
  trinomialBoundary,
  strikePrice,
  spotPrice,
}: CallEarlyExercisePlotProps) {
  // Prepare data for plotting
  const binomialTimes = binomialBoundary.map((p) => p.time);
  const binomialPrices = binomialBoundary.map((p) => p.stock_price);

  const trinomialTimes = trinomialBoundary.map((p) => p.time);
  const trinomialPrices = trinomialBoundary.map((p) => p.stock_price);

  const traces: any[] = [];

  // Add binomial call boundary
  if (binomialBoundary.length > 0) {
    traces.push({
      x: binomialTimes,
      y: binomialPrices,
      type: "scatter",
      mode: "lines+markers",
      name: "Binomial",
      line: { color: "#3b82f6", width: 3 },
      marker: { size: 6 },
    });
  }

  // Add trinomial call boundary
  if (trinomialBoundary.length > 0) {
    traces.push({
      x: trinomialTimes,
      y: trinomialPrices,
      type: "scatter",
      mode: "lines+markers",
      name: "Trinomial",
      line: { color: "#8b5cf6", width: 2 },
      marker: { size: 4, symbol: "square" },
    });
  }

  // Add strike price and spot price reference lines
  const maxTime = Math.max(...binomialTimes, ...trinomialTimes, 0);

  if (maxTime > 0) {
    traces.push({
      x: [0, maxTime],
      y: [strikePrice, strikePrice],
      type: "scatter",
      mode: "lines",
      name: "Strike Price",
      line: { color: "#666", width: 2, dash: "dot" },
      showlegend: true,
    });

    traces.push({
      x: [0, maxTime],
      y: [spotPrice, spotPrice],
      type: "scatter",
      mode: "lines",
      name: "Current Spot",
      line: { color: "#22c55e", width: 2, dash: "dashdot" },
      showlegend: true,
    });
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 border border-gray-200 dark:border-gray-700">
      <h2 className="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-100">
        Early Exercise Boundary - American Call (with Dividends)
      </h2>
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
        Shows the critical stock prices above which early exercise becomes
        optimal for American call options when dividends are present. Exercise
        the call when the stock price rises above the boundary.
      </p>

      {traces.length > 2 ? (
        <Plot
          data={traces}
          layout={{
            autosize: true,
            xaxis: {
              title: { text: "Time (years)" },
              gridcolor: "#e5e7eb",
              zeroline: false,
            },
            yaxis: {
              title: { text: "Stock Price ($)" },
              gridcolor: "#e5e7eb",
              zeroline: false,
            },
            legend: {
              x: 1,
              xanchor: "right",
              y: 1,
              bgcolor: "rgba(255,255,255,0.8)",
              bordercolor: "#e5e7eb",
              borderwidth: 1,
            },
            hovermode: "closest",
            plot_bgcolor: "#ffffff",
            paper_bgcolor: "#ffffff",
            margin: { t: 20, r: 20, b: 60, l: 60 },
          }}
          config={{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ["lasso2d", "select2d"],
          }}
          style={{ width: "100%", height: "500px" }}
        />
      ) : (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">
            No early exercise boundary detected for calls.
          </p>
          <ul className="mt-4 text-left max-w-md mx-auto list-disc list-inside">
            <li>The call option may be far out-of-the-money</li>
            <li>Dividend yield may be too small to justify early exercise</li>
            <li>Try increasing the dividend yield or number of tree steps</li>
          </ul>
        </div>
      )}
    </div>
  );
}
