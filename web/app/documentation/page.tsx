"use client";

import Link from "next/link";
import { ArrowLeft, BookOpen } from "lucide-react";
import "katex/dist/katex.min.css";
import { InlineMath, BlockMath } from "react-katex";

export default function DocumentationPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link
            href="/"
            className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Home
          </Link>
          <div className="flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-600" />
            <h1 className="text-xl font-bold text-slate-900">
              Theory & Documentation
            </h1>
          </div>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8 space-y-10">
          {/* PDF Report Download Button */}
          <div className="flex justify-center">
            <a
              href="/Project-Report-Hassan-ELQADI.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-3 bg-gradient-to-r from-red-600 to-red-700 text-white px-8 py-4 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              Download Project Report (PDF)
            </a>
          </div>

          {/* Introduction */}
          <section>
            <h2 className="text-3xl font-bold text-slate-900 mb-4">
              Option Pricing Theory & Methods
            </h2>
            <p className="text-slate-700 leading-relaxed mb-4">
              This application implements three fundamental approaches to option
              pricing: the <strong>Black-Scholes analytical model</strong> for
              European options and two{" "}
              <strong>numerical lattice methods</strong> (Binomial and Trinomial
              trees) that can handle both European and American-style options.
            </p>
            <p className="text-slate-700 leading-relaxed">
              All models assume a frictionless market with no dividends (
              <InlineMath math="q = 0" />
              ), constant volatility <InlineMath math="\sigma" />, and constant
              risk-free rate <InlineMath math="r" />.
            </p>
          </section>

          {/* Black-Scholes Model */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              1. Black-Scholes-Merton Model
            </h3>
            <p className="text-slate-700 mb-4">
              The Black-Scholes-Merton model (1973) provides closed-form
              analytical solutions for European options. Under the assumption of
              geometric Brownian motion for the underlying asset, the option
              prices are given by:
            </p>

            <div className="bg-slate-50 rounded-lg p-6 space-y-6 overflow-x-auto">
              <div>
                <p className="font-semibold text-slate-800 mb-3">
                  European Call Option Price:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <BlockMath math="C(S_0, t) = S_0 \mathcal{N}(d_1) - K e^{-rT} \mathcal{N}(d_2)" />
                </div>
              </div>

              <div>
                <p className="font-semibold text-slate-800 mb-3">
                  European Put Option Price:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <BlockMath math="P(S_0, t) = K e^{-rT} \mathcal{N}(-d_2) - S_0 \mathcal{N}(-d_1)" />
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-3">
                  Where the auxiliary variables are:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200 space-y-3">
                  <BlockMath math="d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}" />
                  <BlockMath math="d_2 = d_1 - \sigma\sqrt{T} = \frac{\ln(S_0/K) + (r - \sigma^2/2)T}{\sigma\sqrt{T}}" />
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-3">Parameters:</p>
                <div className="grid md:grid-cols-2 gap-3 text-sm">
                  <div className="flex items-start gap-2">
                    <InlineMath math="S_0" /> <span>:</span>
                    <span className="text-slate-700">Current stock price</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <InlineMath math="K" /> <span>:</span>
                    <span className="text-slate-700">Strike price</span>
                  </div>
                  <div className="flex items-start gap-2">
                    <InlineMath math="T" /> <span>:</span>
                    <span className="text-slate-700">
                      Time to maturity (years)
                    </span>
                  </div>
                  <div className="flex items-start gap-2">
                    <InlineMath math="r" /> <span>:</span>
                    <span className="text-slate-700">
                      Risk-free interest rate
                    </span>
                  </div>
                  <div className="flex items-start gap-2">
                    <InlineMath math="\sigma" /> <span>:</span>
                    <span className="text-slate-700">
                      Volatility (annualized)
                    </span>
                  </div>
                  <div className="flex items-start gap-2">
                    <InlineMath math="\mathcal{N}(\cdot)" /> <span>:</span>
                    <span className="text-slate-700">
                      Cumulative standard normal distribution function
                    </span>
                  </div>
                </div>
              </div>

              <div className="border-t pt-4 bg-blue-50 p-4 rounded">
                <p className="text-sm text-slate-700">
                  <strong>Note:</strong> The Black-Scholes model assumes
                  continuous trading, no transaction costs, constant volatility,
                  and log-normal distribution of stock prices. It is exact only
                  for European options.
                </p>
              </div>
            </div>
          </section>

          {/* Greeks */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              2. The Greeks - Risk Sensitivities
            </h3>
            <p className="text-slate-700 mb-4">
              The Greeks quantify how option prices change with respect to
              various market parameters. These are partial derivatives of the
              option price and are essential for risk management and hedging
              strategies.
            </p>

            <div className="bg-slate-50 rounded-lg p-6 space-y-5 overflow-x-auto">
              <div>
                <p className="font-semibold text-slate-800 mb-2">
                  <span className="text-blue-600">Delta (Δ)</span> - Rate of
                  Change w.r.t. Underlying Price
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="\Delta = \frac{\partial V}{\partial S} = \mathcal{N}(d_1) \quad \text{(for calls)}" />
                </div>
                <p className="text-sm text-slate-600">
                  Delta represents the sensitivity of the option price to
                  changes in the underlying asset price. It ranges from 0 to 1
                  for calls and -1 to 0 for puts. Delta is also the hedge ratio.
                </p>
              </div>

              <div>
                <p className="font-semibold text-slate-800 mb-2">
                  <span className="text-blue-600">Gamma (Γ)</span> - Rate of
                  Change of Delta
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="\Gamma = \frac{\partial^2 V}{\partial S^2} = \frac{n(d_1)}{S_0 \sigma \sqrt{T}}" />
                </div>
                <p className="text-sm text-slate-600 mb-1">
                  Where <InlineMath math="n(\cdot)" /> is the standard normal
                  probability density function:
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="n(x) = \frac{1}{\sqrt{2\pi}} e^{-x^2/2}" />
                </div>
                <p className="text-sm text-slate-600">
                  Gamma measures the convexity of the option's value. High gamma
                  means delta changes rapidly, requiring frequent rehedging.
                </p>
              </div>

              <div>
                <p className="font-semibold text-slate-800 mb-2">
                  <span className="text-blue-600">Theta (Θ)</span> - Time Decay
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="\Theta = \frac{\partial V}{\partial t} = -\frac{S_0 n(d_1) \sigma}{2\sqrt{T}} - rKe^{-rT}\mathcal{N}(d_2)" />
                </div>
                <p className="text-sm text-slate-600">
                  Theta measures the rate of decline in option value as time
                  passes (time decay). Expressed per day by dividing by 365.
                  Most options experience negative theta, especially near
                  expiration.
                </p>
              </div>

              <div>
                <p className="font-semibold text-slate-800 mb-2">
                  <span className="text-blue-600">Vega (ν)</span> - Volatility
                  Sensitivity
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="\nu = \frac{\partial V}{\partial \sigma} = S_0 n(d_1) \sqrt{T}" />
                </div>
                <p className="text-sm text-slate-600">
                  Vega measures sensitivity to changes in implied volatility.
                  Expressed per 1% change in volatility (divided by 100).
                  Options are most sensitive to volatility when at-the-money.
                </p>
              </div>

              <div>
                <p className="font-semibold text-slate-800 mb-2">
                  <span className="text-blue-600">Rho (ρ)</span> - Interest Rate
                  Sensitivity
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="\rho = \frac{\partial V}{\partial r} = KT e^{-rT} \mathcal{N}(d_2)" />
                </div>
                <p className="text-sm text-slate-600">
                  Rho measures sensitivity to changes in the risk-free interest
                  rate. Expressed per 1% change in rates (divided by 100). Less
                  significant for short-dated options.
                </p>
              </div>
            </div>
          </section>

          {/* Binomial Tree */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              3. Binomial Tree Model (Cox-Ross-Rubinstein)
            </h3>
            <p className="text-slate-700 mb-4">
              The Cox-Ross-Rubinstein (CRR) binomial tree model (1979) is a
              discrete-time method that models stock price evolution as a
              recombining tree. It can price both European and American options
              and converges to the Black-Scholes price as the number of steps
              increases.
            </p>

            <div className="bg-slate-50 rounded-lg p-6 space-y-6 overflow-x-auto">
              <div>
                <p className="font-semibold text-slate-800 mb-3">
                  Model Parameters:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200 space-y-3">
                  <div>
                    <p className="text-sm text-slate-600 mb-2">Time step:</p>
                    <BlockMath math="\Delta t = \frac{T}{N}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">Up factor:</p>
                    <BlockMath math="u = e^{\sigma\sqrt{\Delta t}}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">Down factor:</p>
                    <BlockMath math="d = \frac{1}{u} = e^{-\sigma\sqrt{\Delta t}}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Risk-neutral probability:
                    </p>
                    <BlockMath math="p = \frac{e^{r\Delta t} - d}{u - d}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Discount factor:
                    </p>
                    <BlockMath math="\text{disc} = e^{-r\Delta t}" />
                  </div>
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-3">
                  Algorithm: Backward Induction
                </p>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <ol className="list-decimal list-inside space-y-3 text-sm text-slate-700">
                    <li>
                      <strong>Initialize:</strong> Set{" "}
                      <InlineMath math="\Delta t = T/N" />, compute{" "}
                      <InlineMath math="u" />, <InlineMath math="d" />, and{" "}
                      <InlineMath math="p" />
                    </li>
                    <li>
                      <strong>Build Terminal Nodes:</strong> At maturity (step{" "}
                      <InlineMath math="N" />
                      ), calculate stock prices for all{" "}
                      <InlineMath math="N+1" /> nodes:
                      <div className="my-2 ml-6">
                        <BlockMath math="S_{N,j} = S_0 \cdot u^j \cdot d^{N-j}, \quad j = 0, 1, \ldots, N" />
                      </div>
                    </li>
                    <li>
                      <strong>Terminal Payoffs:</strong> Compute option values
                      at maturity:
                      <div className="my-2 ml-6">
                        <BlockMath math="V_{N,j} = \max(S_{N,j} - K, 0) \quad \text{(Call)}" />
                        <BlockMath math="V_{N,j} = \max(K - S_{N,j}, 0) \quad \text{(Put)}" />
                      </div>
                    </li>
                    <li>
                      <strong>Backward Recursion:</strong> For each step{" "}
                      <InlineMath math="i = N-1, N-2, \ldots, 0" /> and node{" "}
                      <InlineMath math="j" />:
                      <div className="my-2 ml-6">
                        <BlockMath math="V_{i,j} = e^{-r\Delta t} \left[ p \cdot V_{i+1,j+1} + (1-p) \cdot V_{i+1,j} \right]" />
                      </div>
                    </li>
                    <li>
                      <strong>American Exercise (Optional):</strong> For
                      American options, at each node check early exercise:
                      <div className="my-2 ml-6">
                        <BlockMath math="S_{i,j} = S_0 \cdot u^j \cdot d^{i-j}" />
                        <BlockMath math="V_{i,j}^{\text{American}} = \max\left(V_{i,j}^{\text{European}}, \; \text{Intrinsic Value}\right)" />
                      </div>
                    </li>
                    <li>
                      <strong>Result:</strong> Option price is{" "}
                      <InlineMath math="V_{0,0}" /> at the root node
                    </li>
                  </ol>
                </div>
              </div>

              <div className="border-t pt-4 bg-blue-50 p-4 rounded">
                <p className="text-sm text-slate-700">
                  <strong>Key Properties:</strong> The binomial tree is
                  recombining (up-then-down = down-then-up), has{" "}
                  <InlineMath math="N+1" /> nodes at each time step, and
                  converges to Black-Scholes at rate{" "}
                  <InlineMath math="O(1/\sqrt{N})" /> for European options.
                </p>
              </div>
            </div>
          </section>

          {/* Trinomial Tree */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              4. Trinomial Tree Model (Boyle)
            </h3>
            <p className="text-slate-700 mb-4">
              The Boyle (1988) trinomial tree extends the binomial model by
              adding a middle branch where the stock price remains unchanged.
              This provides better convergence properties and more flexibility
              in modeling.
            </p>

            <div className="bg-slate-50 rounded-lg p-6 space-y-6 overflow-x-auto">
              <div>
                <p className="font-semibold text-slate-800 mb-3">
                  Model Parameters (Boyle Parameterization):
                </p>
                <div className="bg-white p-4 rounded border border-slate-200 space-y-3">
                  <div>
                    <p className="text-sm text-slate-600 mb-2">Time step:</p>
                    <BlockMath math="\Delta t = \frac{T}{N}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">Up factor:</p>
                    <BlockMath math="u = e^{\sigma\sqrt{2\Delta t}}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">Down factor:</p>
                    <BlockMath math="d = \frac{1}{u} = e^{-\sigma\sqrt{2\Delta t}}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Middle factor:
                    </p>
                    <BlockMath math="m = 1 \quad \text{(no change)}" />
                  </div>
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-3">
                  Risk-Neutral Probabilities:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200 space-y-3">
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Auxiliary variables:
                    </p>
                    <BlockMath math="a = e^{r\Delta t / 2}, \quad b = e^{\sigma\sqrt{\Delta t/2}}" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Probability of up move:
                    </p>
                    <BlockMath math="p_u = \left[\frac{a - b^{-1}}{b - b^{-1}}\right]^2" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Probability of down move:
                    </p>
                    <BlockMath math="p_d = \left[\frac{b - a}{b - b^{-1}}\right]^2" />
                  </div>
                  <div>
                    <p className="text-sm text-slate-600 mb-2">
                      Probability of middle move:
                    </p>
                    <BlockMath math="p_m = 1 - p_u - p_d" />
                  </div>
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-3">
                  Algorithm: Trinomial Backward Induction
                </p>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <ol className="list-decimal list-inside space-y-3 text-sm text-slate-700">
                    <li>
                      <strong>Initialize:</strong> Set{" "}
                      <InlineMath math="\Delta t = T/N" />, compute{" "}
                      <InlineMath math="u" />, <InlineMath math="d" />,{" "}
                      <InlineMath math="p_u" />, <InlineMath math="p_d" />, and{" "}
                      <InlineMath math="p_m" />
                    </li>
                    <li>
                      <strong>Build Terminal Nodes:</strong> At maturity,
                      trinomial tree has <InlineMath math="2N+1" /> nodes
                      representing <InlineMath math="j \in \{-N, \ldots, N\}" />{" "}
                      net up moves:
                      <div className="my-2 ml-6">
                        <BlockMath math="S_{N,j} = S_0 \cdot u^{\max(j,0)} \cdot d^{\max(-j,0)}" />
                      </div>
                    </li>
                    <li>
                      <strong>Terminal Payoffs:</strong>
                      <div className="my-2 ml-6">
                        <BlockMath math="V_{N,j} = \max(S_{N,j} - K, 0) \quad \text{(Call)}" />
                        <BlockMath math="V_{N,j} = \max(K - S_{N,j}, 0) \quad \text{(Put)}" />
                      </div>
                    </li>
                    <li>
                      <strong>Backward Recursion:</strong> For each step{" "}
                      <InlineMath math="i = N-1, \ldots, 0" /> with{" "}
                      <InlineMath math="2i+1" /> nodes:
                      <div className="my-2 ml-6">
                        <BlockMath math="V_{i,j} = e^{-r\Delta t} \left[ p_u \cdot V_{i+1,j+1} + p_m \cdot V_{i+1,j} + p_d \cdot V_{i+1,j-1} \right]" />
                      </div>
                    </li>
                    <li>
                      <strong>American Exercise (Optional):</strong> At each
                      node, compare with intrinsic value:
                      <div className="my-2 ml-6">
                        <BlockMath math="V_{i,j}^{\text{American}} = \max\left(V_{i,j}^{\text{European}}, \; \text{Intrinsic Value}\right)" />
                      </div>
                    </li>
                    <li>
                      <strong>Result:</strong> Option price is{" "}
                      <InlineMath math="V_{0,0}" /> at the root
                    </li>
                  </ol>
                </div>
              </div>

              <div className="border-t pt-4 bg-blue-50 p-4 rounded">
                <p className="text-sm text-slate-700">
                  <strong>Advantages:</strong> Trinomial trees typically exhibit
                  smoother convergence than binomial trees and can better model
                  path-dependent options. The additional middle branch provides
                  more accurate probability matching.
                </p>
              </div>
            </div>
          </section>

          {/* Convergence */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              5. Convergence Analysis
            </h3>
            <p className="text-slate-700 mb-4">
              As the number of time steps <InlineMath math="N" /> increases,
              both tree models converge to the continuous-time Black-Scholes
              price for European options. Understanding convergence behavior is
              crucial for selecting appropriate <InlineMath math="N" /> values.
            </p>

            <div className="bg-slate-50 rounded-lg p-6 space-y-6 overflow-x-auto">
              <div>
                <p className="font-semibold text-slate-800 mb-3">
                  Convergence Algorithm:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <ol className="list-decimal list-inside space-y-3 text-sm text-slate-700">
                    <li>
                      <strong>Define step range:</strong> Select{" "}
                      <InlineMath math="N_{\min}" /> and{" "}
                      <InlineMath math="N_{\max}" /> (e.g., 1 to 100)
                    </li>
                    <li>
                      <strong>Compute Black-Scholes benchmark:</strong>{" "}
                      Calculate exact European option price{" "}
                      <InlineMath math="V_{\text{BS}}" />
                    </li>
                    <li>
                      <strong>Iterate over steps:</strong> For each{" "}
                      <InlineMath math="N \in [N_{\min}, N_{\max}]" />:
                      <div className="my-2 ml-6">
                        <p>
                          a) Run binomial tree with <InlineMath math="N" />{" "}
                          steps → <InlineMath math="V_{\text{binom}}(N)" />
                        </p>
                        <p>
                          b) Run trinomial tree with <InlineMath math="N" />{" "}
                          steps → <InlineMath math="V_{\text{trinom}}(N)" />
                        </p>
                      </div>
                    </li>
                    <li>
                      <strong>Compute errors:</strong> Calculate absolute
                      errors:
                      <div className="my-2 ml-6">
                        <BlockMath math="\epsilon_{\text{binom}}(N) = |V_{\text{binom}}(N) - V_{\text{BS}}|" />
                        <BlockMath math="\epsilon_{\text{trinom}}(N) = |V_{\text{trinom}}(N) - V_{\text{BS}}|" />
                      </div>
                    </li>
                    <li>
                      <strong>Visualize:</strong> Plot{" "}
                      <InlineMath math="V(N)" /> vs <InlineMath math="N" /> with
                      Black-Scholes reference line
                    </li>
                  </ol>
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-3">
                  Convergence Properties:
                </p>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <ul className="space-y-3 text-sm text-slate-700">
                    <li>
                      <strong>Rate of Convergence:</strong>
                      <div className="my-2 ml-4">
                        <p>
                          • Binomial tree: <InlineMath math="O(1/\sqrt{N})" />{" "}
                          for European options
                        </p>
                        <p>
                          • Trinomial tree: Generally{" "}
                          <InlineMath math="O(1/N)" />, faster convergence
                        </p>
                      </div>
                    </li>
                    <li>
                      <strong>Oscillatory Behavior:</strong> Tree prices
                      oscillate around the Black-Scholes value due to discrete
                      time approximation. Oscillations dampen as{" "}
                      <InlineMath math="N \to \infty" />.
                    </li>
                    <li>
                      <strong>Even/Odd Effect:</strong> Some tree models exhibit
                      different convergence patterns for even vs. odd{" "}
                      <InlineMath math="N" /> when <InlineMath math="S_0 = K" />{" "}
                      (at-the-money).
                    </li>
                    <li>
                      <strong>Practical Considerations:</strong>
                      <div className="my-2 ml-4">
                        <p>
                          • <InlineMath math="N = 50-100" />: Good balance of
                          accuracy and speed
                        </p>
                        <p>
                          • <InlineMath math="N > 500" />: Diminishing returns,
                          increased computation
                        </p>
                        <p>
                          • For American options: Higher <InlineMath math="N" />{" "}
                          often needed near exercise boundary
                        </p>
                      </div>
                    </li>
                  </ul>
                </div>
              </div>

              <div className="border-t pt-4 bg-amber-50 p-4 rounded">
                <p className="text-sm text-slate-700">
                  <strong>Richardson Extrapolation:</strong> To improve
                  convergence, advanced techniques like Richardson extrapolation
                  can be applied: Combine results from <InlineMath math="N" />{" "}
                  and <InlineMath math="2N" /> steps to achieve{" "}
                  <InlineMath math="O(1/N^2)" /> convergence.
                </p>
              </div>
            </div>
          </section>

          {/* Validation */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              6. Model Validation Tests
            </h3>
            <p className="text-slate-700 mb-4">
              The application performs comprehensive validation tests to ensure
              numerical accuracy and theoretical consistency of the implemented
              models.
            </p>

            <div className="bg-slate-50 rounded-lg p-6 space-y-5">
              <div>
                <p className="font-semibold text-slate-800 mb-2">
                  1. Put-Call Parity (European Options):
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="C - P = S_0 - K e^{-rT}" />
                </div>
                <p className="text-sm text-slate-600">
                  Verifies the fundamental no-arbitrage relationship between
                  European call and put prices with the same strike and
                  maturity. Any deviation indicates pricing errors.
                </p>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-2">
                  2. American Early Exercise Premium:
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="V_{\text{American}} \geq V_{\text{European}}" />
                </div>
                <p className="text-sm text-slate-600">
                  American options must be worth at least as much as their
                  European counterparts due to the early exercise feature.
                  Violations suggest algorithmic errors.
                </p>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-2">
                  3. Tree-BS Convergence:
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="\lim_{N \to \infty} V_{\text{tree}}(N) = V_{\text{BS}}" />
                </div>
                <p className="text-sm text-slate-600">
                  For European options, tree model prices should converge to the
                  Black-Scholes analytical solution as the number of steps
                  increases. Typical tolerance: <InlineMath math="< 0.01" /> for{" "}
                  <InlineMath math="N \geq 100" />.
                </p>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-2">
                  4. Boundary Conditions:
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2 space-y-2">
                  <BlockMath math="C(S_0, T) \geq \max(S_0 - Ke^{-rT}, 0)" />
                  <BlockMath math="P(S_0, T) \geq \max(Ke^{-rT} - S_0, 0)" />
                </div>
                <p className="text-sm text-slate-600">
                  Option prices must satisfy lower bounds to prevent arbitrage.
                  Calls and puts must be worth at least their intrinsic values.
                </p>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-2">
                  5. Probability Validity:
                </p>
                <div className="bg-white p-3 rounded border border-slate-200 mb-2">
                  <BlockMath math="0 \leq p, p_u, p_m, p_d \leq 1 \quad \text{and} \quad p_u + p_m + p_d = 1" />
                </div>
                <p className="text-sm text-slate-600">
                  Risk-neutral probabilities must be valid (non-negative and sum
                  to 1). Violations may occur for extreme parameter
                  combinations.
                </p>
              </div>
            </div>
          </section>

          {/* Implementation */}
          <section className="border-t pt-8">
            <h3 className="text-2xl font-bold text-slate-900 mb-4">
              7. Implementation & Technology Stack
            </h3>
            <div className="bg-slate-50 rounded-lg p-6 space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="bg-white p-4 rounded border border-slate-200">
                  <p className="font-semibold text-slate-800 mb-2">Backend</p>
                  <ul className="text-sm text-slate-700 space-y-1">
                    <li>• Python 3.10+</li>
                    <li>• FastAPI for REST API</li>
                    <li>• NumPy for vectorized computations</li>
                    <li>• SciPy for statistical functions</li>
                  </ul>
                </div>
                <div className="bg-white p-4 rounded border border-slate-200">
                  <p className="font-semibold text-slate-800 mb-2">Frontend</p>
                  <ul className="text-sm text-slate-700 space-y-1">
                    <li>• Next.js 14 with TypeScript</li>
                    <li>• Tailwind CSS for styling</li>
                    <li>• Plotly.js for charts</li>
                    <li>• KaTeX for LaTeX rendering</li>
                  </ul>
                </div>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-2">
                  Key Assumptions:
                </p>
                <ul className="text-sm text-slate-700 space-y-1">
                  <li>
                    • No dividends (<InlineMath math="q = 0" />)
                  </li>
                  <li>
                    • Constant volatility <InlineMath math="\sigma" />
                  </li>
                  <li>
                    • Constant risk-free rate <InlineMath math="r" />
                  </li>
                  <li>• Frictionless markets (no transaction costs)</li>
                  <li>• Continuous trading (for Black-Scholes)</li>
                  <li>• Log-normal distribution of stock prices</li>
                </ul>
              </div>

              <div className="border-t pt-4">
                <p className="font-semibold text-slate-800 mb-2">
                  Performance Optimizations:
                </p>
                <ul className="text-sm text-slate-700 space-y-1">
                  <li>• NumPy vectorization for terminal payoffs</li>
                  <li>
                    • Efficient backward induction (no redundant calculations)
                  </li>
                  <li>• Sparse convergence sampling for large N</li>
                  <li>• Client-side caching of results</li>
                </ul>
              </div>
            </div>
          </section>

          {/* CTA */}
          <section className="border-t pt-8">
            <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-lg p-8 text-center">
              <h3 className="text-2xl font-bold text-white mb-4">
                Ready to Apply the Theory?
              </h3>
              <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
                Use our interactive calculator to price options with your own
                parameters and visualize convergence behavior
              </p>
              <Link
                href="/pricing"
                className="inline-block bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors shadow-lg"
              >
                Launch Pricing Calculator →
              </Link>
            </div>
          </section>
        </div>
      </main>
    </div>
  );
}
