"use client";
import { useState } from "react";
import InputForm from "@/components/pricing/InputForm";
import BlackScholesSection from "@/components/pricing/BlackScholesSection";
import TreeModelSection from "@/components/pricing/TreeModelSection";
import ConvergenceTestSection from "@/components/pricing/ConvergenceTestSection";
import ValidationSection from "@/components/pricing/ValidationSection";
import { usePricingCalculations } from "../hooks/usePricingCalculations";

export default function PricingPage() {
  const [form, setForm] = useState({
    s0: 100,
    k: 100,
    t: 1,
    r: 0.025,
    sigma: 0.25,
    steps: 100,
  });

  const { loading, results, calculateAll } = usePricingCalculations();

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in p-4">
      <div className="text-center space-y-3">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent">
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
  );
}
