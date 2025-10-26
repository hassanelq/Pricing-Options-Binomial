"""
Validation service for running option pricing tests
"""

import numpy as np
from .pricing import OptionPricingService


class ValidationService:
    """Service for validating option pricing models"""

    # -------------------- Public API --------------------

    @staticmethod
    def run_all_validations(
        S: float, K: float, T: float, r: float, sigma: float, N: int, q: float = 0.0
    ) -> dict:
        """Run all validation tests and return results"""
        categories = [
            ValidationService._test_convergence(S, K, T, r, sigma, N, q),
            ValidationService._test_european_pricing_accuracy(S, K, T, r, sigma, N, q),
            ValidationService._test_arbitrage_and_parity(S, K, T, r, sigma, N, q),
            ValidationService._test_american_checks(S, K, T, r, sigma, N, q),
            ValidationService._test_risk_neutral(S, K, T, r, sigma, N, q),
        ]

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

    # -------------------- Tests --------------------

    @staticmethod
    def _test_european_pricing_accuracy(
        S: float, K: float, T: float, r: float, sigma: float, N: int, q: float = 0.0
    ) -> dict:
        """Test 1: European pricing accuracy (Trees vs Black-Scholes)"""

        # Reference prices (once)
        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, q, "call")
        bs_put = OptionPricingService.black_scholes(S, K, T, r, sigma, q, "put")

        # Trees (once)
        bin_call = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "call", "european"
        )
        bin_put = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "put", "european"
        )
        tri_call = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "call", "european"
        )
        tri_put = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "put", "european"
        )

        # Percentage errors (protect against division by ~0 using tiny eps)
        eps = 1e-16
        bin_call_error = abs(bin_call - bs_call) / max(abs(bs_call), eps) * 100.0
        bin_put_error = abs(bin_put - bs_put) / max(abs(bs_put), eps) * 100.0
        tri_call_error = abs(tri_call - bs_call) / max(abs(bs_call), eps) * 100.0
        tri_put_error = abs(tri_put - bs_put) / max(abs(bs_put), eps) * 100.0

        # Targets scaled with N (unchanged)
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
        S: float, K: float, T: float, r: float, sigma: float, N: int, q: float = 0.0
    ) -> dict:
        """Test 2: Arbitrage sanity + Put-Call Parity"""

        # Prices once per model
        C_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "call", "european"
        )
        P_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "put", "european"
        )
        C_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "call", "european"
        )
        P_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "put", "european"
        )

        K_pv = K * np.exp(-r * T)
        S_pv = S * np.exp(-q * T)  # Dividend-adjusted spot price
        expected_diff = S_pv - K_pv  # C - P = S*e^(-qT) - K*e^(-rT)

        # Absolute parity gap, reported as % of S for readability
        epsilon_bin_pct = abs((C_bin - P_bin) - expected_diff) / S * 100.0
        epsilon_tri_pct = abs((C_tri - P_tri) - expected_diff) / S * 100.0

        tests = [
            {
                "name": "Call Lower Bound (C ≥ max(S*e^(-qT)-Ke^(-rT), 0))",
                "passed": C_bin >= max(S_pv - K_pv, 0.0) - 1e-6,
                "value": float(C_bin),
                "target": float(max(S_pv - K_pv, 0.0)),
                "unit": "$",
            },
            {
                "name": "Put  Lower Bound (P ≥ max(Ke^(-rT)-S*e^(-qT), 0))",
                "passed": P_bin >= max(K_pv - S_pv, 0.0) - 1e-6,
                "value": float(P_bin),
                "target": float(max(K_pv - S_pv, 0.0)),
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
        S: float, K: float, T: float, r: float, sigma: float, N: int, q: float = 0.0
    ) -> dict:
        """Test 3: American-specific checks"""

        # Binomial EU vs AM
        P_eu_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "put", "european"
        )
        P_am_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "put", "american"
        )

        # Trinomial EU vs AM
        P_eu_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "put", "european"
        )
        P_am_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "put", "american"
        )

        premium_put_bin = P_am_bin - P_eu_bin
        premium_put_tri = P_am_tri - P_eu_tri

        tests = [
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
        S: float, K: float, T: float, r: float, sigma: float, N: int, q: float = 0.0
    ) -> dict:
        """Test 4: Convergence analysis"""

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, q, "call")
        bin_call = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, q, "call", "european"
        )
        tri_call = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, q, "call", "european"
        )

        eps = 1e-16
        bin_error = abs(bin_call - bs_call) / max(abs(bs_call), eps) * 100.0
        tri_error = abs(tri_call - bs_call) / max(abs(bs_call), eps) * 100.0

        # Targets scale with N (unchanged)
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
        S: float, K: float, T: float, r: float, sigma: float, N: int, q: float = 0.0
    ) -> dict:
        """Test 5: Risk-neutral / martingale validity"""

        dt = T / N

        # Binomial parameters (with dividend yield)
        u_bin = np.exp(sigma * np.sqrt(dt))
        d_bin = 1.0 / u_bin
        p_bin = (np.exp((r - q) * dt) - d_bin) / (u_bin - d_bin)

        # Trinomial (Boyle) parameters (with dividend yield)
        u_tri = np.exp(sigma * np.sqrt(2.0 * dt))
        d_tri = 1.0 / u_tri
        a = np.exp((r - q) * dt / 2.0)
        b = np.exp(sigma * np.sqrt(dt / 2.0))
        invb = 1.0 / b
        denom = b - invb
        pu_tri = ((a - invb) / denom) ** 2
        pd_tri = ((b - a) / denom) ** 2
        pm_tri = 1.0 - pu_tri - pd_tri

        # Analytical martingale check (faster, no loop):
        # E[S_T] under binomial = S * (p*u + (1-p)*d)^N, target = S*exp((r-q)T)
        if N <= 100:  # keep same gating behavior
            expected_ST = S * (p_bin * u_bin + (1.0 - p_bin) * d_bin) ** N
            theoretical_ST = S * np.exp((r - q) * T)
            martingale_error = abs(expected_ST - theoretical_ST) / S * 100.0
        else:
            martingale_error = 0.0  # not computed for large N (same output semantics)

        tests = [
            {
                "name": "Binomial Probability in [0,1]",
                "passed": 0.0 <= p_bin <= 1.0,
                "value": float(p_bin),
                "target": 0.5,
                "unit": "",
            },
            {
                "name": "Trinomial p_up in [0,1]",
                "passed": 0.0 <= pu_tri <= 1.0,
                "value": float(pu_tri),
                "target": 0.33,
                "unit": "",
            },
            {
                "name": "Trinomial p_mid in [0,1]",
                "passed": 0.0 <= pm_tri <= 1.0,
                "value": float(pm_tri),
                "target": 0.33,
                "unit": "",
            },
            {
                "name": "Trinomial p_down in [0,1]",
                "passed": 0.0 <= pd_tri <= 1.0,
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
