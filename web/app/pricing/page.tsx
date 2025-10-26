"use client";
import { useState } from "react";
import Link from "next/link";
import dynamic from "next/dynamic";
import * as XLSX from "xlsx";
import InputForm from "@/components/pricing/InputForm";
import BlackScholesSection from "@/components/pricing/BlackScholesSection";
import TreeModelSection from "@/components/pricing/TreeModelSection";
import ConvergenceTestSection from "@/components/pricing/ConvergenceTestSection";
import ValidationSection from "@/components/pricing/ValidationSection";
import { usePricingCalculations } from "../../hooks/usePricingCalculations";

// Dynamically import plot components to avoid SSR issues
const PutEarlyExercisePlot = dynamic(
  () =>
    import("@/components/pricing/EarlyExercisePlot").then(
      (mod) => mod.PutEarlyExercisePlot
    ),
  { ssr: false }
);

const CallEarlyExercisePlot = dynamic(
  () =>
    import("@/components/pricing/EarlyExercisePlot").then(
      (mod) => mod.CallEarlyExercisePlot
    ),
  { ssr: false }
);

const TreeVisualization = dynamic(
  () =>
    import("@/components/pricing/TreeVisualization").then(
      (mod) => mod.TreeVisualization
    ),
  { ssr: false }
);

export default function PricingPage() {
  const [form, setForm] = useState({
    s0: 90,
    k: 100,
    t: 1,
    r: 0.03,
    sigma: 0.4,
    steps: 50,
    q: 0.015,
  });

  const { loading, results, calculateAll } = usePricingCalculations();

  const handleDownloadReport = () => {
    if (!results.blackScholes) {
      alert("Please calculate pricing first");
      return;
    }

    // Create a new workbook
    const workbook = XLSX.utils.book_new();

    // Sheet 1: Input Parameters
    const inputData = [
      ["OPTION PRICING ANALYSIS REPORT"],
      ["Generated:", new Date().toLocaleString()],
      [],
      ["INPUT PARAMETERS"],
      ["Parameter", "Value"],
      ["Spot Price (S₀)", `$${form.s0}`],
      ["Strike Price (K)", `$${form.k}`],
      ["Time to Maturity (T)", `${form.t} years`],
      ["Risk-Free Rate (r)", `${(form.r * 100).toFixed(2)}%`],
      ["Volatility (σ)", `${(form.sigma * 100).toFixed(2)}%`],
      ["Dividend Yield (q)", `${(form.q * 100).toFixed(2)}%`],
      ["Tree Steps (N)", form.steps],
    ];
    const inputSheet = XLSX.utils.aoa_to_sheet(inputData);
    XLSX.utils.book_append_sheet(workbook, inputSheet, "Input Parameters");

    // Sheet 2: Black-Scholes Results
    const bsData = [
      ["BLACK-SCHOLES MODEL"],
      [],
      ["Option Type", "Price"],
      ["European Call", `$${results.blackScholes.callPrice.toFixed(4)}`],
      ["European Put", `$${results.blackScholes.putPrice.toFixed(4)}`],
      [],
      ["CALL GREEKS"],
      ["Greek", "Value"],
      ["Delta", results.blackScholes.callGreeks.delta.toFixed(4)],
      ["Gamma", results.blackScholes.callGreeks.gamma.toFixed(4)],
      ["Theta", results.blackScholes.callGreeks.theta.toFixed(4)],
      ["Vega", results.blackScholes.callGreeks.vega.toFixed(4)],
      ["Rho", results.blackScholes.callGreeks.rho.toFixed(4)],
      [],
      ["PUT GREEKS"],
      ["Greek", "Value"],
      ["Delta", results.blackScholes.putGreeks.delta.toFixed(4)],
      ["Gamma", results.blackScholes.putGreeks.gamma.toFixed(4)],
      ["Theta", results.blackScholes.putGreeks.theta.toFixed(4)],
      ["Vega", results.blackScholes.putGreeks.vega.toFixed(4)],
      ["Rho", results.blackScholes.putGreeks.rho.toFixed(4)],
    ];
    const bsSheet = XLSX.utils.aoa_to_sheet(bsData);
    XLSX.utils.book_append_sheet(workbook, bsSheet, "Black-Scholes");

    // Sheet 3: Tree Models
    const treeData = [
      ["TREE MODELS PRICING"],
      [],
      [
        "Model",
        "European Call",
        "European Put",
        "American Call",
        "American Put",
      ],
      [
        "Binomial",
        `$${results.binomial?.europeanCall.toFixed(4)}`,
        `$${results.binomial?.europeanPut.toFixed(4)}`,
        `$${results.binomial?.americanCall.toFixed(4)}`,
        `$${results.binomial?.americanPut.toFixed(4)}`,
      ],
      [
        "Trinomial",
        `$${results.trinomial?.europeanCall.toFixed(4)}`,
        `$${results.trinomial?.europeanPut.toFixed(4)}`,
        `$${results.trinomial?.americanCall.toFixed(4)}`,
        `$${results.trinomial?.americanPut.toFixed(4)}`,
      ],
    ];
    const treeSheet = XLSX.utils.aoa_to_sheet(treeData);
    XLSX.utils.book_append_sheet(workbook, treeSheet, "Tree Models");

    // Sheet 4: Convergence Data
    if (results.binomial?.convergence && results.trinomial?.convergence) {
      const convergenceData = [
        ["CONVERGENCE ANALYSIS"],
        [],
        ["Steps", "Binomial Price", "Trinomial Price", "Black-Scholes Price"],
      ];

      const minLength = Math.min(
        results.binomial.convergence.length,
        results.trinomial.convergence.length
      );

      // Add rows where both models have data
      for (let i = 0; i < minLength; i++) {
        const binomialPoint = results.binomial.convergence[i];
        const trinomialPoint = results.trinomial.convergence[i];
        convergenceData.push([
          binomialPoint.steps.toString(),
          binomialPoint.price.toFixed(4),
          trinomialPoint.price.toFixed(4),
          results.blackScholes.callPrice.toFixed(4),
        ]);
      }

      // Add remaining binomial data if any
      for (let i = minLength; i < results.binomial.convergence.length; i++) {
        const binomialPoint = results.binomial.convergence[i];
        convergenceData.push([
          binomialPoint.steps.toString(),
          binomialPoint.price.toFixed(4),
          "N/A",
          results.blackScholes.callPrice.toFixed(4),
        ]);
      }

      // Add remaining trinomial data if any
      for (let i = minLength; i < results.trinomial.convergence.length; i++) {
        const trinomialPoint = results.trinomial.convergence[i];
        convergenceData.push([
          trinomialPoint.steps.toString(),
          "N/A",
          trinomialPoint.price.toFixed(4),
          results.blackScholes.callPrice.toFixed(4),
        ]);
      }

      const convergenceSheet = XLSX.utils.aoa_to_sheet(convergenceData);
      XLSX.utils.book_append_sheet(workbook, convergenceSheet, "Convergence");
    }

    // Sheet 5: Validation Tests
    const validationData = [
      ["MODEL VALIDATION TESTS"],
      [],
      ["Total Tests", results.validation?.total_tests || 0],
      ["Passed Tests", results.validation?.passed_tests || 0],
      [],
      ["Category", "Test Name", "Value", "Unit", "Target", "Status"],
    ];

    results.validation?.categories.forEach((category: any) => {
      category.tests.forEach((test: any) => {
        validationData.push([
          category.name,
          test.name,
          test.value.toFixed(6),
          test.unit,
          test.target.toFixed(6),
          test.passed ? "PASS" : "FAIL",
        ]);
      });
    });

    const validationSheet = XLSX.utils.aoa_to_sheet(validationData);
    XLSX.utils.book_append_sheet(workbook, validationSheet, "Validation");

    // Sheet 6: Early Exercise Boundary
    if (results.binomial && results.trinomial) {
      const boundaryData = [
        ["EARLY EXERCISE BOUNDARY ANALYSIS"],
        [],
        ["PUT OPTIONS - Optimal Exercise Frontier"],
        [
          "Time (years)",
          "Binomial Boundary",
          "Trinomial Boundary",
          "Strike Price",
        ],
      ];

      // Combine put boundaries
      const maxPutLength = Math.max(
        results.binomial.boundaryPut.length,
        results.trinomial.boundaryPut.length
      );

      for (let i = 0; i < maxPutLength; i++) {
        const binPoint = results.binomial.boundaryPut[i];
        const triPoint = results.trinomial.boundaryPut[i];
        boundaryData.push([
          binPoint ? binPoint.time.toFixed(4) : "N/A",
          binPoint ? `$${binPoint.stock_price.toFixed(4)}` : "N/A",
          triPoint ? `$${triPoint.stock_price.toFixed(4)}` : "N/A",
          `$${form.k}`,
        ]);
      }

      // Add call boundaries if dividends exist
      if (form.q > 0) {
        boundaryData.push(
          [],
          ["CALL OPTIONS - Optimal Exercise Frontier (with Dividends)"],
          [
            "Time (years)",
            "Binomial Boundary",
            "Trinomial Boundary",
            "Strike Price",
          ]
        );

        const maxCallLength = Math.max(
          results.binomial.boundaryCall.length,
          results.trinomial.boundaryCall.length
        );

        for (let i = 0; i < maxCallLength; i++) {
          const binPoint = results.binomial.boundaryCall[i];
          const triPoint = results.trinomial.boundaryCall[i];
          boundaryData.push([
            binPoint ? binPoint.time.toFixed(4) : "N/A",
            binPoint ? `$${binPoint.stock_price.toFixed(4)}` : "N/A",
            triPoint ? `$${triPoint.stock_price.toFixed(4)}` : "N/A",
            `$${form.k}`,
          ]);
        }
      }

      const boundarySheet = XLSX.utils.aoa_to_sheet(boundaryData);
      XLSX.utils.book_append_sheet(workbook, boundarySheet, "Early Exercise");
    }

    // Generate Excel file and download
    XLSX.writeFile(workbook, `option-pricing-report-${Date.now()}.xlsx`);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto space-y-8 px-4">
        {/* Header with Navigation */}
        <div className="flex justify-between items-center">
          <Link
            href="/"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors flex items-center gap-2"
          >
            ← Back to Home
          </Link>
          <Link
            href="/documentation"
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors flex items-center gap-2 border border-gray-300 px-4 py-2 rounded-lg hover:border-gray-400"
          >
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
              />
            </svg>
            Documentation
          </Link>
        </div>

        <div className="text-center space-y-3">
          <h1 className="text-4xl leading-snug font-bold bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
            Option Pricing Calculator
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Black-Scholes, Binomial, and Trinomial methods
          </p>
        </div>

        <InputForm
          form={form}
          setForm={setForm}
          onCalculate={() => calculateAll(form)}
          loading={loading}
          onDownloadReport={handleDownloadReport}
          hasResults={!!results.blackScholes}
        />

        {results.blackScholes && (
          <BlackScholesSection
            callPrice={results.blackScholes.callPrice}
            putPrice={results.blackScholes.putPrice}
            callGreeks={results.blackScholes.callGreeks}
            putGreeks={results.blackScholes.putGreeks}
          />
        )}

        {results.binomial && (
          <TreeModelSection
            title="Binomial Tree Model"
            europeanCall={results.binomial.europeanCall}
            europeanPut={results.binomial.europeanPut}
            americanCall={results.binomial.americanCall}
            americanPut={results.binomial.americanPut}
            bsPrice={results.blackScholes?.callPrice || 0}
          />
        )}

        {results.trinomial && (
          <TreeModelSection
            title="Trinomial Tree Model"
            europeanCall={results.trinomial.europeanCall}
            europeanPut={results.trinomial.europeanPut}
            americanCall={results.trinomial.americanCall}
            americanPut={results.trinomial.americanPut}
            bsPrice={results.blackScholes?.callPrice || 0}
          />
        )}

        {/* Tree Visualizations - American Put */}
        {results.trees && (
          <TreeVisualization
            binomialTree={results.trees.put.binomial}
            trinomialTree={results.trees.put.trinomial}
            strikePrice={form.k}
            exerciseType="american"
            optionType="put"
          />
        )}

        {/* Put Early Exercise Boundary - Always shown */}
        {results.binomial && results.trinomial && (
          <PutEarlyExercisePlot
            binomialBoundary={results.binomial.boundaryPut}
            trinomialBoundary={results.trinomial.boundaryPut}
            strikePrice={form.k}
            spotPrice={form.s0}
          />
        )}

        {/* Tree Visualizations - American Call */}
        {results.trees && (
          <TreeVisualization
            binomialTree={results.trees.call.binomial}
            trinomialTree={results.trees.call.trinomial}
            strikePrice={form.k}
            exerciseType="american"
            optionType="call"
          />
        )}

        {/* Call Early Exercise Boundary - Only shown when dividends > 0 */}
        {results.binomial && results.trinomial && form.q > 0 && (
          <CallEarlyExercisePlot
            binomialBoundary={results.binomial.boundaryCall}
            trinomialBoundary={results.trinomial.boundaryCall}
            strikePrice={form.k}
            spotPrice={form.s0}
          />
        )}

        {results.binomial && results.trinomial && results.blackScholes && (
          <ConvergenceTestSection
            bsPrice={results.blackScholes.callPrice}
            binomialConvergence={results.binomial.convergence}
            trinomialConvergence={results.trinomial.convergence}
          />
        )}

        {results.validation && (
          <ValidationSection validation={results.validation} />
        )}
      </div>
    </div>
  );
}
