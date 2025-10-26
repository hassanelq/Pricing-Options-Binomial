"use client";
import React from "react";
import dynamic from "next/dynamic";

const Plot = dynamic(() => import("react-plotly.js"), { ssr: false });

interface TreeNode {
  stock: number;
  european: number;
  american: number;
  early: boolean;
}

interface TreeLattice {
  N: number;
  levels: TreeNode[][];
}

interface TreeVisualizationProps {
  binomialTree: TreeLattice;
  trinomialTree: TreeLattice;
  strikePrice: number;
  exerciseType: "european" | "american";
  optionType: "put" | "call";
}

export function TreeVisualization({
  binomialTree,
  trinomialTree,
  strikePrice,
  exerciseType,
  optionType,
}: TreeVisualizationProps) {
  // Helper function to prepare tree data with correct connecting lines
  const prepareTreeData = (tree: TreeLattice, isBinomial: boolean) => {
    const x: number[] = [];
    const y: number[] = [];
    const stockLabels: string[] = [];
    const optionLabels: string[] = [];
    const colors: string[] = [];
    const sizes: number[] = [];

    // Lines data for connections
    const lineX: number[] = [];
    const lineY: number[] = [];

    // Store node positions for line drawing
    const nodePosMap: Map<string, { x: number; y: number }> = new Map();

    // First pass: collect all positions
    tree.levels.forEach((level, timeStep) => {
      level.forEach((node, nodeIndex) => {
        const numNodes = level.length;
        const centerOffset = (numNodes - 1) / 2;
        const yPos = nodeIndex - centerOffset;

        nodePosMap.set(`${timeStep}-${nodeIndex}`, {
          x: timeStep,
          y: yPos,
        });
      });
    });

    // Draw connecting lines based on tree type
    tree.levels.forEach((level, timeStep) => {
      if (timeStep < tree.levels.length - 1) {
        level.forEach((node, nodeIndex) => {
          const numNodes = level.length;
          const centerOffset = (numNodes - 1) / 2;
          const yPos = nodeIndex - centerOffset;

          const nextLevel = tree.levels[timeStep + 1];
          const numNextNodes = nextLevel.length;
          const nextCenterOffset = (numNextNodes - 1) / 2;

          if (isBinomial) {
            // Binomial tree: each node connects to exactly 2 nodes in next level
            // Up move connects to nodeIndex, Down move connects to nodeIndex + 1
            const connectIndices = [nodeIndex, nodeIndex + 1];
            connectIndices.forEach((nextNodeIndex) => {
              if (nextNodeIndex >= 0 && nextNodeIndex < numNextNodes) {
                const nextYPos = nextNodeIndex - nextCenterOffset;
                lineX.push(timeStep, timeStep + 1, null);
                lineY.push(yPos, nextYPos, null);
              }
            });
          } else {
            // Trinomial tree: each node connects to exactly 3 nodes in next level
            // Up move, middle move, down move
            const connectIndices = [nodeIndex, nodeIndex + 1, nodeIndex + 2];
            connectIndices.forEach((nextNodeIndex) => {
              if (nextNodeIndex >= 0 && nextNodeIndex < numNextNodes) {
                const nextYPos = nextNodeIndex - nextCenterOffset;
                lineX.push(timeStep, timeStep + 1, null);
                lineY.push(yPos, nextYPos, null);
              }
            });
          }
        });
      }
    });

    // Second pass: collect node data
    tree.levels.forEach((level, timeStep) => {
      level.forEach((node, nodeIndex) => {
        const numNodes = level.length;
        const centerOffset = (numNodes - 1) / 2;
        const yPos = nodeIndex - centerOffset;

        x.push(timeStep);
        y.push(yPos);

        stockLabels.push(`$${node.stock.toFixed(2)}`);

        const optionValue =
          exerciseType === "american" ? node.american : node.european;
        optionLabels.push(`${optionValue.toFixed(4)}`);

        // Enhanced color scheme
        if (exerciseType === "american" && node.early) {
          colors.push("#EF4444"); // Red for early exercise
          sizes.push(18);
        } else {
          colors.push("#3B82F6"); // Blue for normal nodes
          sizes.push(14);
        }
      });
    });

    return { x, y, stockLabels, optionLabels, colors, sizes, lineX, lineY };
  };

  const binomialData = prepareTreeData(binomialTree, true);
  const trinomialData = prepareTreeData(trinomialTree, false);

  const createPlotData = (data: ReturnType<typeof prepareTreeData>) => [
    // Connecting lines trace
    {
      x: data.lineX,
      y: data.lineY,
      mode: "lines",
      type: "scatter",
      line: {
        color: "rgba(107, 114, 128, 0.4)",
        width: 1.5,
      },
      hoverinfo: "none",
      showlegend: false,
    },
    // Nodes trace
    {
      x: data.x,
      y: data.y,
      mode: "markers+text",
      type: "scatter",
      marker: {
        size: data.sizes,
        color: data.colors,
        line: {
          color: "white",
          width: 2,
        },
        opacity: 0.9,
      },
      text: data.stockLabels.map(
        (s, i) =>
          `<b>${s}</b><br><span style="font-size:9px;">${data.optionLabels[i]}</span>`
      ),
      textposition: "top center",
      textfont: {
        size: 10,
        color: "black",
        family: "Arial, sans-serif",
      },
      hovertemplate:
        "<b>Stock Price:</b> %{customdata[0]}<br>" +
        "<b>Option Value:</b> %{customdata[1]}<br>" +
        "<extra></extra>",
      customdata: data.stockLabels.map((s, i) => [s, data.optionLabels[i]]),
      showlegend: false,
    },
  ];

  const createLayout = (tree: TreeLattice, title: string) => ({
    title: {
      text: title,
      font: { size: 16, color: "#1F2937" },
    },
    xaxis: {
      title: "Time Step (periods)",
      showgrid: true,
      gridwidth: 1,
      gridcolor: "rgba(229, 231, 235, 0.5)",
      zeroline: false,
      range: [-0.2, tree.N + 0.2],
      showline: true,
      linewidth: 2,
      linecolor: "#E5E7EB",
      tickfont: { size: 11, color: "#6B7280" },
      titlefont: { size: 12, color: "#374151" },
    },
    yaxis: {
      title: "Stock Price Paths",
      showgrid: true,
      gridwidth: 1,
      gridcolor: "rgba(229, 231, 235, 0.5)",
      zeroline: true,
      zerolinewidth: 2,
      zerolinecolor: "rgba(229, 231, 235, 0.8)",
      showline: true,
      linewidth: 2,
      linecolor: "#E5E7EB",
      tickfont: { size: 11, color: "#6B7280" },
      titlefont: { size: 12, color: "#374151" },
    },
    hovermode: "closest",
    height: 600,
    autosize: true,
    margin: { l: 60, r: 20, t: 40, b: 60 },
    plot_bgcolor: "#F9FAFB",
    paper_bgcolor: "#FFFFFF",
    font: { family: "system-ui, -apple-system, sans-serif", color: "#374151" },
  });

  return (
    <div className="w-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 rounded-xl shadow-2xl p-8 space-y-12">
      {/* Header Section */}
      <div className="border-b-2 border-gray-200 dark:border-gray-700 pb-6">
        <h2 className="text-3xl font-bold mb-3 text-gray-900 dark:text-white bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
          Option Pricing Tree
        </h2>
        <div className="flex flex-wrap gap-4 items-center text-sm">
          <div className="flex items-center gap-2">
            <span className="inline-block w-3 h-3 bg-blue-500 rounded-full"></span>
            <span className="text-gray-700 dark:text-gray-300">
              <span className="font-semibold">
                {exerciseType === "american" ? "American" : "European"}
              </span>{" "}
              {optionType === "put" ? "Put" : "Call"} Option
            </span>
          </div>
          <div className="text-gray-700 dark:text-gray-300">
            <span className="font-semibold">Strike Price:</span> ${strikePrice}
          </div>
          {exerciseType === "american" && (
            <div className="flex items-center gap-2">
              <span className="inline-block w-3 h-3 bg-red-500 rounded-full"></span>
              <span className="text-gray-700 dark:text-gray-300">
                Early Exercise Optimal
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Trees Container */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Binomial Tree */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700 flex flex-col">
          <div className="bg-gradient-to-r from-blue-500 to-blue-600 px-6 py-4">
            <h3 className="text-xl font-semibold text-white">Binomial Tree</h3>
            <p className="text-blue-100 text-sm mt-1">
              N = {binomialTree.N} periods (2 outcomes per node)
            </p>
          </div>
          <div className="flex-1 w-full">
            <Plot
              data={createPlotData(binomialData) as any}
              layout={createLayout(binomialTree, "") as any}
              config={{
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ["lasso2d", "select2d"],
              }}
              style={{ width: "100%", height: "100%" }}
            />
          </div>
        </div>

        {/* Trinomial Tree */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden border border-gray-200 dark:border-gray-700 flex flex-col">
          <div className="bg-gradient-to-r from-indigo-500 to-indigo-600 px-6 py-4">
            <h3 className="text-xl font-semibold text-white">Trinomial Tree</h3>
            <p className="text-indigo-100 text-sm mt-1">
              N = {trinomialTree.N} periods (3 outcomes per node)
            </p>
          </div>
          <div className="flex-1 w-full">
            <Plot
              data={createPlotData(trinomialData) as any}
              layout={createLayout(trinomialTree, "") as any}
              config={{
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ["lasso2d", "select2d"],
              }}
              style={{ width: "100%", height: "100%" }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
