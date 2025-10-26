import { useState } from 'react';
import { apiPost } from '@/lib/api';

interface Greeks {
  delta: number;
  gamma: number;
  theta: number;
  vega: number;
  rho: number;
}

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

interface BoundaryPoint {
  time: number;
  stock_price: number;
  time_to_maturity: number;
}

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

interface ApiResponse {
  black_scholes: {
    call_price: number;
    put_price: number;
    greeks: Greeks;
  };
  binomial: {
    european_call: number;
    european_put: number;
    american_call: number;
    american_put: number;
    convergence: Array<{ steps: number; price: number }>;
    boundary_put: BoundaryPoint[];
    boundary_call: BoundaryPoint[];
  };
  trinomial: {
    european_call: number;
    european_put: number;
    american_call: number;
    american_put: number;
    convergence: Array<{ steps: number; price: number }>;
    boundary_put: BoundaryPoint[];
    boundary_call: BoundaryPoint[];
  };
  trees: {
    put: {
      binomial: TreeLattice;
      trinomial: TreeLattice;
    };
    call: {
      binomial: TreeLattice;
      trinomial: TreeLattice;
    };
  };
  validation: ValidationResults;
}

interface Results {
  blackScholes: {
    callPrice: number;
    putPrice: number;
    callGreeks: Greeks;
    putGreeks: Greeks;
  } | null;
  binomial: {
    europeanCall: number;
    europeanPut: number;
    americanCall: number;
    americanPut: number;
    convergence: Array<{ steps: number; price: number; error: number }>;
    boundaryPut: BoundaryPoint[];
    boundaryCall: BoundaryPoint[];
  } | null;
  trinomial: {
    europeanCall: number;
    europeanPut: number;
    americanCall: number;
    americanPut: number;
    convergence: Array<{ steps: number; price: number; error: number }>;
    boundaryPut: BoundaryPoint[];
    boundaryCall: BoundaryPoint[];
  } | null;
  trees: {
    put: {
      binomial: TreeLattice;
      trinomial: TreeLattice;
    };
    call: {
      binomial: TreeLattice;
      trinomial: TreeLattice;
    };
  } | null;
  validation: ValidationResults | null;
}export function usePricingCalculations() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<Results>({
    blackScholes: null,
    binomial: null,
    trinomial: null,
    trees: null,
    validation: null,
  });

  const calculateAll = async (form: {
    s0: number;
    k: number;
    t: number;
    r: number;
    sigma: number;
    steps: number;
    q: number;
  }) => {
    setLoading(true);
    setResults({ blackScholes: null, binomial: null, trinomial: null, trees: null, validation: null });

    try {
      const response = await apiPost<ApiResponse>('/api/calculate', {
        spotPrice: +form.s0,
        strike: +form.k,
        timeToMaturity: +form.t,
        riskFreeRate: +form.r,
        volatility: +form.sigma,
        treeSteps: +form.steps,
        dividendYield: +form.q,
      });

      // Extract Black-Scholes data
      const callGreeks = response.black_scholes.greeks;
      const bsCallPrice = response.black_scholes.call_price;
      
      // Calculate put Greeks using put-call parity relationships with dividends
      // With dividends: C - P = S*e^(-qT) - K*e^(-rT)
      // Delta_put = Delta_call - e^(-qT)
      // Rho_put = Rho_call - K*T*e^(-rT)
      const putGreeks: Greeks = {
        delta: callGreeks.delta - Math.exp(-form.q * form.t),
        gamma: callGreeks.gamma,
        theta: callGreeks.theta,
        vega: callGreeks.vega,
        rho: callGreeks.rho - form.k * form.t * Math.exp(-form.r * form.t) / 100,
      };

      // Convergence data now comes with steps and prices directly from API
      // Calculate error percentage for display
      const binConvergence = response.binomial.convergence.map((point) => ({
        steps: point.steps,
        price: point.price,
        error: ((point.price - bsCallPrice) / bsCallPrice) * 100,
      }));

      const triConvergence = response.trinomial.convergence.map((point) => ({
        steps: point.steps,
        price: point.price,
        error: ((point.price - bsCallPrice) / bsCallPrice) * 100,
      }));

      // Set results
      setResults({
        blackScholes: {
          callPrice: response.black_scholes.call_price,
          putPrice: response.black_scholes.put_price,
          callGreeks,
          putGreeks,
        },
        binomial: {
          europeanCall: response.binomial.european_call,
          europeanPut: response.binomial.european_put,
          americanCall: response.binomial.american_call,
          americanPut: response.binomial.american_put,
          convergence: binConvergence,
          boundaryPut: response.binomial.boundary_put,
          boundaryCall: response.binomial.boundary_call,
        },
        trinomial: {
          europeanCall: response.trinomial.european_call,
          europeanPut: response.trinomial.european_put,
          americanCall: response.trinomial.american_call,
          americanPut: response.trinomial.american_put,
          convergence: triConvergence,
          boundaryPut: response.trinomial.boundary_put,
          boundaryCall: response.trinomial.boundary_call,
        },
        trees: response.trees,
        validation: response.validation,
      });
    } catch (error: any) {
      console.error('Calculation error:', error);
      alert('Error: ' + (error.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  };

  return { loading, results, calculateAll };
}
