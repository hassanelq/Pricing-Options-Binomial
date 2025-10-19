import { useState } from "react";

interface TestResult {
  name: string;
  passed: boolean;
  value: number;
  target: number;
  unit: string;
}

interface TestCategory {
  name: string;
  tests: TestResult[];
  all_passed: boolean;
}

interface ValidationResults {
  categories: TestCategory[];
  overall_passed: boolean;
  total_tests: number;
  passed_tests: number;
}

interface ValidationSectionProps {
  validation: ValidationResults;
}

interface CategoryInfo {
  description: string;
  formula: string;
  targetExplanation: string;
  whyItMatters: string;
}

// Category information with formulas and explanations
const categoryInfoMap: Record<string, CategoryInfo> = {
  "European Pricing Accuracy": {
    description:
      "Compares tree model prices against the analytical Black-Scholes solution for European options.",
    formula: "Error = |V_tree - V_BS| / V_BS × 100%",
    targetExplanation:
      "Base targets: Binomial ≤ 0.15%, Trinomial ≤ 0.08% at N=250. Scales with N: target = base × (250/N). At N=100: Binomial ≤ 0.375%, Trinomial ≤ 0.2%",
    whyItMatters:
      "Tree models should converge to the exact Black-Scholes price as steps increase. This validates numerical accuracy.",
  },
  "Arbitrage & Put-Call Parity": {
    description:
      "Tests fundamental no-arbitrage bounds and the put-call parity relationship for European options.",
    formula:
      "Bounds: C ≥ max(S - Ke^(-rT), 0), P ≥ max(Ke^(-rT) - S, 0)\nParity: C - P = S - Ke^(-rT)",
    targetExplanation:
      "Lower bounds must hold (arbitrage-free). Parity residual ε ≤ 0.02% of spot. These are mathematical requirements, not based on N.",
    whyItMatters:
      "Violating these creates risk-free profit opportunities (arbitrage). Put-call parity is a fundamental relationship in options theory.",
  },
  "American Option Checks": {
    description:
      "Validates properties specific to American options: no early exercise for calls (no dividends), positive premium for puts.",
    formula:
      "Call: C^Am ≈ C^Eu (difference ≤ $0.0001)\nPut: P^Am ≥ P^Eu (premium ≥ 0)",
    targetExplanation:
      "For non-dividend stocks, American calls should equal European calls exactly. American puts always worth at least as much as European puts.",
    whyItMatters:
      "Tests theoretical properties: early exercise of calls is never optimal without dividends.",
  },
  "Convergence Analysis": {
    description:
      "Measures how tree model errors decrease as the number of steps increases.",
    formula: "Error(N) = |V_tree(N) - V_BS| / V_BS × 100%",
    targetExplanation:
      "Base targets: Binomial ≤ 0.2%, Trinomial ≤ 0.1% at N=400. Scales: target = base × (400/N). At N=100: Binomial ≤ 0.8%, Trinomial ≤ 0.4%",
    whyItMatters:
      "Convergence rate shows computational efficiency. Error should decrease ~O(1/N). More steps = better accuracy but slower computation.",
  },
  "Risk-Neutral Validity": {
    description:
      "Verifies risk-neutral probabilities are valid and the martingale property holds under the risk-neutral measure.",
    formula:
      "Binomial: p = (e^(rΔt) - d)/(u - d) ∈ [0,1]\nTrinomial: p_up, p_mid, p_down ∈ [0,1], sum = 1\nMartingale: E[S_T] = S₀e^(rT)",
    targetExplanation:
      "All probabilities must be in [0,1]. Martingale error ≤ 0.1%. These ensure the model is mathematically consistent.",
    whyItMatters:
      "Invalid probabilities make the model nonsensical. Martingale property ensures risk-neutral pricing is correct and expectation matches forward price.",
  },
};

export default function ValidationSection({
  validation,
}: ValidationSectionProps) {
  const [expandedCategory, setExpandedCategory] = useState<number | null>(null);

  const toggleCategory = (index: number) => {
    setExpandedCategory(expandedCategory === index ? null : index);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-4">Model Validation Tests</h2>

      {/* Test Categories */}
      <div className="space-y-6">
        {validation.categories.map((category, idx) => {
          const categoryInfo = categoryInfoMap[category.name];
          return (
            <div key={idx} className="border rounded-lg p-4">
              {/* Category Header */}
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <span
                    className={`text-2xl ${
                      category.all_passed ? "text-green-500" : "text-yellow-500"
                    }`}
                  >
                    {category.all_passed ? "✓" : "⚠"}
                  </span>
                  {idx + 1}. {category.name}
                </h3>
                {categoryInfo && (
                  <button
                    onClick={() => toggleCategory(idx)}
                    className="px-3 py-1 text-sm bg-blue-100 text-blue-700 hover:bg-blue-200 rounded-md transition-colors"
                  >
                    {expandedCategory === idx ? "Hide Info ▲" : "Show Info ▼"}
                  </button>
                )}
              </div>

              {/* Expandable Category Information */}
              {expandedCategory === idx && categoryInfo && (
                <div className="mb-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-semibold text-blue-900 mb-1">
                        Description:
                      </h4>
                      <p className="text-sm text-gray-700">
                        {categoryInfo.description}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-semibold text-blue-900 mb-1">
                        Formula:
                      </h4>
                      <pre className="text-xs bg-white p-2 rounded border border-blue-200 overflow-x-auto">
                        {categoryInfo.formula}
                      </pre>
                    </div>
                    <div>
                      <h4 className="font-semibold text-blue-900 mb-1">
                        Target Explanation:
                      </h4>
                      <p className="text-sm text-gray-700">
                        {categoryInfo.targetExplanation}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-semibold text-blue-900 mb-1">
                        Why It Matters:
                      </h4>
                      <p className="text-sm text-gray-700">
                        {categoryInfo.whyItMatters}
                      </p>
                    </div>
                  </div>
                </div>
              )}

              {/* Tests Table */}
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Status
                      </th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Test
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">
                        Value
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">
                        Target
                      </th>
                      <th className="px-4 py-2 text-center text-xs font-medium text-gray-500 uppercase">
                        Result
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {category.tests.map((test, testIdx) => (
                      <tr
                        key={testIdx}
                        className={test.passed ? "" : "bg-red-50"}
                      >
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span
                            className={`text-xl ${
                              test.passed ? "text-green-500" : "text-red-500"
                            }`}
                          >
                            {test.passed ? "✓" : "✗"}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm text-gray-900">
                          {test.name}
                        </td>
                        <td className="px-4 py-3 text-sm text-right font-mono">
                          {formatValue(test.value, test.unit)}
                        </td>
                        <td className="px-4 py-3 text-sm text-right font-mono text-gray-500">
                          {test.unit === "$" ? "≥ " : "≤ "}
                          {formatValue(test.target, test.unit)}
                        </td>
                        <td className="px-4 py-3 text-center">
                          <span
                            className={`px-2 py-1 text-xs font-medium rounded ${
                              test.passed
                                ? "bg-green-100 text-green-800"
                                : "bg-red-100 text-red-800"
                            }`}
                          >
                            {test.passed ? "PASS" : "FAIL"}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function formatValue(value: number, unit: string): string {
  if (unit === "%") {
    return value.toFixed(4) + "%";
  } else if (unit === "$") {
    return "$" + value.toFixed(6);
  } else {
    return value.toFixed(6);
  }
}
