"use client";
import React from "react";

interface Greeks {
  delta: number;
  gamma: number;
  theta: number;
  vega: number;
  rho: number;
}

interface EnhancedPricingResultsProps {
  blackScholes: {
    callPrice: number;
    putPrice: number;
    callGreeks: Greeks;
    putGreeks: Greeks;
  };
  binomial: {
    europeanCall: number;
    europeanPut: number;
    americanCall: number;
    americanPut: number;
  };
  trinomial: {
    europeanCall: number;
    europeanPut: number;
    americanCall: number;
    americanPut: number;
  };
}

export function EnhancedPricingResults({
  blackScholes,
  binomial,
  trinomial,
}: EnhancedPricingResultsProps) {
  const GreeksCard = ({ greeks, title }: { greeks: Greeks; title: string }) => (
    <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
      <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-3">
        {title}
      </h4>
      <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Delta (Δ)</p>
          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {greeks.delta.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Gamma (Γ)</p>
          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {greeks.gamma.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Theta (Θ)</p>
          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {greeks.theta.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Vega (ν)</p>
          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {greeks.vega.toFixed(4)}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-400">Rho (ρ)</p>
          <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {greeks.rho.toFixed(4)}
          </p>
        </div>
      </div>
    </div>
  );

  const PriceCard = ({
    label,
    price,
    color,
  }: {
    label: string;
    price: number;
    color: string;
  }) => (
    <div
      className={`bg-gradient-to-br ${color} rounded-lg p-4 text-white shadow-md`}
    >
      <p className="text-sm opacity-90 mb-1">{label}</p>
      <p className="text-2xl font-bold">${price.toFixed(4)}</p>
    </div>
  );

  return (
    <div className="space-y-8">
      {/* CALL OPTIONS SECTION */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b-2 border-green-500">
          <div className="w-12 h-12 bg-green-500 rounded-lg flex items-center justify-center">
            <span className="text-2xl font-bold text-white">C</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              Call Option Pricing
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Upside profit potential
            </p>
          </div>
        </div>

        {/* Black-Scholes Call */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
            Black-Scholes-Merton Model
          </h3>
          <div className="space-y-4">
            <PriceCard
              label="Call Option Price"
              price={blackScholes.callPrice}
              color="from-green-500 to-green-600"
            />
            <GreeksCard greeks={blackScholes.callGreeks} title="Call Greeks" />
          </div>
        </div>

        {/* Binomial & Trinomial Call */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Binomial */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
              Binomial Tree Model
            </h3>
            <div className="space-y-3">
              <PriceCard
                label="European Call"
                price={binomial.europeanCall}
                color="from-blue-500 to-blue-600"
              />
              <PriceCard
                label="American Call"
                price={binomial.americanCall}
                color="from-indigo-500 to-indigo-600"
              />
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Early Exercise Premium
                </p>
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  ${(binomial.americanCall - binomial.europeanCall).toFixed(4)}
                </p>
              </div>
            </div>
          </div>

          {/* Trinomial */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
              Trinomial Tree Model
            </h3>
            <div className="space-y-3">
              <PriceCard
                label="European Call"
                price={trinomial.europeanCall}
                color="from-blue-500 to-blue-600"
              />
              <PriceCard
                label="American Call"
                price={trinomial.americanCall}
                color="from-indigo-500 to-indigo-600"
              />
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Early Exercise Premium
                </p>
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  $
                  {(trinomial.americanCall - trinomial.europeanCall).toFixed(4)}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* PUT OPTIONS SECTION */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b-2 border-red-500">
          <div className="w-12 h-12 bg-red-500 rounded-lg flex items-center justify-center">
            <span className="text-2xl font-bold text-white">P</span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-gray-100">
              Put Option Pricing
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Downside protection strategy
            </p>
          </div>
        </div>

        {/* Black-Scholes Put */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
            Black-Scholes-Merton Model
          </h3>
          <div className="space-y-4">
            <PriceCard
              label="Put Option Price"
              price={blackScholes.putPrice}
              color="from-red-500 to-red-600"
            />
            <GreeksCard greeks={blackScholes.putGreeks} title="Put Greeks" />
          </div>
        </div>

        {/* Binomial & Trinomial Put */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* Binomial */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
              Binomial Tree Model
            </h3>
            <div className="space-y-3">
              <PriceCard
                label="European Put"
                price={binomial.europeanPut}
                color="from-orange-500 to-orange-600"
              />
              <PriceCard
                label="American Put"
                price={binomial.americanPut}
                color="from-rose-500 to-rose-600"
              />
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Early Exercise Premium
                </p>
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  ${(binomial.americanPut - binomial.europeanPut).toFixed(4)}
                </p>
              </div>
            </div>
          </div>

          {/* Trinomial */}
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200 mb-4">
              Trinomial Tree Model
            </h3>
            <div className="space-y-3">
              <PriceCard
                label="European Put"
                price={trinomial.europeanPut}
                color="from-orange-500 to-orange-600"
              />
              <PriceCard
                label="American Put"
                price={trinomial.americanPut}
                color="from-rose-500 to-rose-600"
              />
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-3">
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  Early Exercise Premium
                </p>
                <p className="text-lg font-bold text-gray-900 dark:text-gray-100">
                  ${(trinomial.americanPut - trinomial.europeanPut).toFixed(4)}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
