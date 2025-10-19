"""
Validation service for running option pricing tests
"""

import numpy as np
import math
from .pricing import OptionPricingService


class ValidationService:
    """Service for validating option pricing models"""

    @staticmethod
    def run_all_validations(
        S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Run all validation tests and return results"""

        categories = []

        # Test 1: Convergence
        categories.append(ValidationService._test_convergence(S, K, T, r, sigma, N))
        
        # Test 2: European Pricing Accuracy
        categories.append(
            ValidationService._test_european_pricing_accuracy(S, K, T, r, sigma, N)
        )

        # Test 3: Arbitrage Sanity & Put-Call Parity
        categories.append(
            ValidationService._test_arbitrage_and_parity(S, K, T, r, sigma, N)
        )

        # Test 4: American-Specific Checks
        categories.append(ValidationService._test_american_checks(S, K, T, r, sigma, N))

        # Test 5: Risk-Neutral Probabilities
        categories.append(ValidationService._test_risk_neutral(S, K, T, r, sigma, N))

        # Calculate overall stats
        total_tests = sum(len(cat["tests"]) for cat in categories)
        passed_tests = sum(
            sum(1 for test in cat["tests"] if test["passed"]) for cat in categories
        )
        overall_passed = all(cat["all_passed"] for cat in categories)

        return {
            "categories": categories,
            "overall_passed": overall_passed,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
        }

    @staticmethod
    def _test_european_pricing_accuracy(
        S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Test 1: European pricing accuracy (Trees vs Black-Scholes)"""

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, "call")
        bs_put = OptionPricingService.black_scholes(S, K, T, r, sigma, "put")

        bin_call = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        bin_put = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )

        tri_call = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        tri_put = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )

        bin_call_error = abs(bin_call - bs_call) / bs_call * 100
        bin_put_error = abs(bin_put - bs_put) / bs_put * 100
        tri_call_error = abs(tri_call - bs_call) / bs_call * 100
        tri_put_error = abs(tri_put - bs_put) / bs_put * 100

        # Targets: Binomial ≤ 0.15%, Trinomial ≤ 0.08% at N=250
        # Scale targets based on actual N
        bin_target = 0.15 * (250 / N) if N > 0 else 0.15
        tri_target = 0.08 * (250 / N) if N > 0 else 0.08

        tests = [
            {
                "name": "Binomial Call Accuracy",
                "passed": bin_call_error <= bin_target,
                "value": float(bin_call_error),
                "target": float(bin_target),
                "unit": "%",
            },
            {
                "name": "Binomial Put Accuracy",
                "passed": bin_put_error <= bin_target,
                "value": float(bin_put_error),
                "target": float(bin_target),
                "unit": "%",
            },
            {
                "name": "Trinomial Call Accuracy",
                "passed": tri_call_error <= tri_target,
                "value": float(tri_call_error),
                "target": float(tri_target),
                "unit": "%",
            },
            {
                "name": "Trinomial Put Accuracy",
                "passed": tri_put_error <= tri_target,
                "value": float(tri_put_error),
                "target": float(tri_target),
                "unit": "%",
            },
        ]

        return {
            "name": "European Pricing Accuracy",
            "tests": tests,
            "all_passed": all(t["passed"] for t in tests),
        }

    @staticmethod
    def _test_arbitrage_and_parity(
        S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Test 2: Arbitrage sanity + Put-Call Parity"""

        C_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        P_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )
        C_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        P_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )

        K_pv = K * np.exp(-r * T)

        # Put-call parity: C - P = S - Ke^(-rT)
        expected_diff = S - K_pv
        epsilon_bin = abs(C_bin - P_bin - expected_diff)
        epsilon_tri = abs(C_tri - P_tri - expected_diff)

        # Convert to percentage of notional
        epsilon_bin_pct = (epsilon_bin / S) * 100
        epsilon_tri_pct = (epsilon_tri / S) * 100

        tests = [
            {
                "name": "Call Lower Bound (C ≥ max(S-Ke^(-rT), 0))",
                "passed": C_bin >= max(S - K_pv, 0) - 1e-6,
                "value": float(C_bin),
                "target": float(max(S - K_pv, 0)),
                "unit": "$",
            },
            {
                "name": "Put Lower Bound (P ≥ max(Ke^(-rT)-S, 0))",
                "passed": P_bin >= max(K_pv - S, 0) - 1e-6,
                "value": float(P_bin),
                "target": float(max(K_pv - S, 0)),
                "unit": "$",
            },
            {
                "name": "Put-Call Parity (Binomial)",
                "passed": epsilon_bin_pct <= 0.02,
                "value": float(epsilon_bin_pct),
                "target": 0.02,
                "unit": "%",
            },
            {
                "name": "Put-Call Parity (Trinomial)",
                "passed": epsilon_tri_pct <= 0.02,
                "value": float(epsilon_tri_pct),
                "target": 0.02,
                "unit": "%",
            },
        ]

        return {
            "name": "Arbitrage & Put-Call Parity",
            "tests": tests,
            "all_passed": all(t["passed"] for t in tests),
        }

    @staticmethod
    def _test_american_checks(
        S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Test 3: American-specific checks"""

        # Binomial
        C_eu_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        C_am_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "american"
        )
        P_eu_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )
        P_am_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "american"
        )

        # Trinomial
        C_eu_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        C_am_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "american"
        )
        P_eu_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )
        P_am_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "american"
        )

        diff_call_bin = abs(C_am_bin - C_eu_bin)
        diff_call_tri = abs(C_am_tri - C_eu_tri)
        premium_put_bin = P_am_bin - P_eu_bin
        premium_put_tri = P_am_tri - P_eu_tri

        tests = [
            {
                "name": "No Early Exercise - Call (Binomial)",
                "passed": diff_call_bin <= 1e-4,
                "value": float(diff_call_bin),
                "target": 1e-4,
                "unit": "$",
            },
            {
                "name": "No Early Exercise - Call (Trinomial)",
                "passed": diff_call_tri <= 1e-4,
                "value": float(diff_call_tri),
                "target": 1e-4,
                "unit": "$",
            },
            {
                "name": "Put Early Exercise Premium (Binomial)",
                "passed": premium_put_bin >= -1e-6,
                "value": float(premium_put_bin),
                "target": 0.0,
                "unit": "$",
            },
            {
                "name": "Put Early Exercise Premium (Trinomial)",
                "passed": premium_put_tri >= -1e-6,
                "value": float(premium_put_tri),
                "target": 0.0,
                "unit": "$",
            },
        ]

        return {
            "name": "American Option Checks",
            "tests": tests,
            "all_passed": all(t["passed"] for t in tests),
        }

    @staticmethod
    def _test_convergence(
        S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Test 4: Convergence analysis"""

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, "call")

        # Test at current N
        bin_call = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        tri_call = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )

        bin_error = abs(bin_call - bs_call) / bs_call * 100
        tri_error = abs(tri_call - bs_call) / bs_call * 100

        # Targets scale with N: at N=400 → 0.2% (bin), 0.1% (tri)
        bin_target = 0.2 * (400 / N) if N > 0 else 0.2
        tri_target = 0.1 * (400 / N) if N > 0 else 0.1

        tests = [
            {
                "name": f"Binomial Convergence (N={N})",
                "passed": bin_error <= bin_target,
                "value": float(bin_error),
                "target": float(bin_target),
                "unit": "%",
            },
            {
                "name": f"Trinomial Convergence (N={N})",
                "passed": tri_error <= tri_target,
                "value": float(tri_error),
                "target": float(tri_target),
                "unit": "%",
            },
        ]

        return {
            "name": "Convergence Analysis",
            "tests": tests,
            "all_passed": all(t["passed"] for t in tests),
        }

    @staticmethod
    def _test_risk_neutral(
        S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Test 5: Risk-neutral / martingale validity"""

        dt = T / N

        # Binomial probabilities
        u_bin = np.exp(sigma * np.sqrt(dt))
        d_bin = 1 / u_bin
        p_bin = (np.exp(r * dt) - d_bin) / (u_bin - d_bin)

        # Trinomial probabilities
        u_tri = np.exp(sigma * np.sqrt(2 * dt))
        d_tri = 1 / u_tri
        pu_tri = (
            (np.exp(r * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2)))
            / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))
        ) ** 2
        pd_tri = (
            (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(r * dt / 2))
            / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))
        ) ** 2
        pm_tri = 1 - pu_tri - pd_tri

        # Martingale property for binomial (only if N is reasonable)
        martingale_error = 0.0
        if N <= 100:  # Only compute for reasonable N
            expected_ST = 0
            for i in range(min(N + 1, 101)):  # Limit iterations
                prob = math.comb(N, i) * (p_bin**i) * ((1 - p_bin) ** (N - i))
                price = S * (u_bin**i) * (d_bin ** (N - i))
                expected_ST += prob * price
            theoretical_ST = S * np.exp(r * T)
            martingale_error = abs(expected_ST - theoretical_ST) / S * 100

        tests = [
            {
                "name": "Binomial Probability in [0,1]",
                "passed": 0 <= p_bin <= 1,
                "value": float(p_bin),
                "target": 0.5,
                "unit": "",
            },
            {
                "name": "Trinomial p_up in [0,1]",
                "passed": 0 <= pu_tri <= 1,
                "value": float(pu_tri),
                "target": 0.33,
                "unit": "",
            },
            {
                "name": "Trinomial p_mid in [0,1]",
                "passed": 0 <= pm_tri <= 1,
                "value": float(pm_tri),
                "target": 0.33,
                "unit": "",
            },
            {
                "name": "Trinomial p_down in [0,1]",
                "passed": 0 <= pd_tri <= 1,
                "value": float(pd_tri),
                "target": 0.33,
                "unit": "",
            },
        ]

        if N <= 100:
            tests.append(
                {
                    "name": "Martingale Property",
                    "passed": martingale_error <= 0.1,
                    "value": float(martingale_error),
                    "target": 0.1,
                    "unit": "%",
                }
            )

        return {
            "name": "Risk-Neutral Validity",
            "tests": tests,
            "all_passed": all(t["passed"] for t in tests),
        }
