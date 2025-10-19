interface Greeks {
  delta: number;
  gamma: number;
  theta: number;
  vega: number;
  rho: number;
}

interface BlackScholesSectionProps {
  callPrice: number;
  putPrice: number;
  callGreeks: Greeks;
  putGreeks: Greeks;
}

export default function BlackScholesSection({
  callPrice,
  putPrice,
  callGreeks,
  putGreeks,
}: BlackScholesSectionProps) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/20 dark:to-indigo-950/20 rounded-lg shadow-lg p-6 border border-blue-200 dark:border-blue-800">
      <h2 className="text-2xl font-bold mb-6 text-blue-900 dark:text-blue-100">
        Black-Scholes Model
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Call Option */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <h3 className="text-xl font-semibold mb-4 text-green-600 dark:text-green-400">
            Call Option
          </h3>
          <div className="mb-4">
            <p className="text-3xl font-bold text-gray-900 dark:text-gray-100">
              ${callPrice.toFixed(4)}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Option Price
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Greeks:
            </h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-gray-600 dark:text-gray-400">Delta:</span>
                <span className="ml-2 font-medium">
                  {callGreeks.delta.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Gamma:</span>
                <span className="ml-2 font-medium">
                  {callGreeks.gamma.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Theta:</span>
                <span className="ml-2 font-medium">
                  {callGreeks.theta.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Vega:</span>
                <span className="ml-2 font-medium">
                  {callGreeks.vega.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Rho:</span>
                <span className="ml-2 font-medium">
                  {callGreeks.rho.toFixed(4)}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Put Option */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <h3 className="text-xl font-semibold mb-4 text-red-600 dark:text-red-400">
            Put Option
          </h3>
          <div className="mb-4">
            <p className="text-3xl font-bold text-gray-900 dark:text-gray-100">
              ${putPrice.toFixed(4)}
            </p>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Option Price
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Greeks:
            </h4>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div>
                <span className="text-gray-600 dark:text-gray-400">Delta:</span>
                <span className="ml-2 font-medium">
                  {putGreeks.delta.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Gamma:</span>
                <span className="ml-2 font-medium">
                  {putGreeks.gamma.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Theta:</span>
                <span className="ml-2 font-medium">
                  {putGreeks.theta.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Vega:</span>
                <span className="ml-2 font-medium">
                  {putGreeks.vega.toFixed(4)}
                </span>
              </div>
              <div>
                <span className="text-gray-600 dark:text-gray-400">Rho:</span>
                <span className="ml-2 font-medium">
                  {putGreeks.rho.toFixed(4)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
