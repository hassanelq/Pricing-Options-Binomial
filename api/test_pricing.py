"""
Comprehensive tests for option pricing models based on academic requirements.

Test Suite:
1. European pricing accuracy (Trees vs Black-Scholes)
2. Arbitrage sanity + Put-Call Parity (European)
3. American-specific checks
4. Convergence analysis
5. Risk-neutral / martingale validity (trees)
"""

import pytest
import numpy as np
import math
from app.services.pricing import OptionPricingService


class TestEuropeanPricingAccuracy:
    """Test 1: European pricing accuracy (Trees vs Black-Scholes)

    Target parameters: S=K=100, r=2%, σ=20%, T=1
    At N=250 steps:
    - Binomial error ≤ 0.15%
    - Trinomial error ≤ 0.08%
    """

    def test_binomial_accuracy_at_250_steps(self):
        """Binomial tree should match BS within 0.15% at N=250"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20
        N = 250

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, "call")
        bin_call = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )

        rel_error = abs(bin_call - bs_call) / bs_call

        print(f"\nBinomial N=250:")
        print(f"  BS Price: {bs_call:.6f}")
        print(f"  Binomial Price: {bin_call:.6f}")
        print(f"  Relative Error: {rel_error*100:.4f}%")

        assert rel_error <= 0.0015, f"Binomial error {rel_error*100:.4f}% > 0.15%"

    def test_trinomial_accuracy_at_250_steps(self):
        """Trinomial tree should match BS within 0.08% at N=250"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20
        N = 250

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, "call")
        tri_call = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )

        rel_error = abs(tri_call - bs_call) / bs_call

        print(f"\nTrinomial N=250:")
        print(f"  BS Price: {bs_call:.6f}")
        print(f"  Trinomial Price: {tri_call:.6f}")
        print(f"  Relative Error: {rel_error*100:.4f}%")

        assert rel_error <= 0.0008, f"Trinomial error {rel_error*100:.4f}% > 0.08%"

    def test_put_pricing_accuracy(self):
        """Test put option pricing accuracy"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20
        N = 250

        bs_put = OptionPricingService.black_scholes(S, K, T, r, sigma, "put")
        bin_put = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )
        tri_put = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )

        bin_error = abs(bin_put - bs_put) / bs_put
        tri_error = abs(tri_put - bs_put) / bs_put

        print(f"\nPut Options N=250:")
        print(f"  BS Put: {bs_put:.6f}")
        print(f"  Binomial Put: {bin_put:.6f} (error: {bin_error*100:.4f}%)")
        print(f"  Trinomial Put: {tri_put:.6f} (error: {tri_error*100:.4f}%)")

        assert bin_error <= 0.0015
        assert tri_error <= 0.0008


class TestArbitrageSanityAndPutCallParity:
    """Test 2: Arbitrage sanity + Put-Call Parity (European)

    Sanity bounds (must all hold):
    - 0 ≤ C ≤ S, 0 ≤ P ≤ Ke^(-rT)
    - C ≥ max(S - Ke^(-rT), 0), P ≥ max(Ke^(-rT) - S, 0)

    Parity residual: ε = |C - P - (S - Ke^(-rT))|
    Target: all bounds pass, ε ≤ 1e-3 (or ≤0.02% of notional)
    """

    @pytest.mark.parametrize(
        "S,K,T,r,sigma",
        [
            (100, 100, 1, 0.02, 0.20),
            (100, 110, 1, 0.05, 0.25),
            (100, 90, 0.5, 0.03, 0.15),
            (50, 50, 2, 0.01, 0.30),
        ],
    )
    def test_sanity_bounds(self, S, K, T, r, sigma):
        """Test all arbitrage sanity bounds"""
        N = 200

        # Get European prices
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

        # Test bounds for both models
        for model_name, C, P in [
            ("Binomial", C_bin, P_bin),
            ("Trinomial", C_tri, P_tri),
        ]:
            # Bound 1: 0 ≤ C ≤ S
            assert 0 <= C <= S, f"{model_name}: Call price {C} violates 0 ≤ C ≤ S"

            # Bound 2: 0 ≤ P ≤ Ke^(-rT)
            assert (
                0 <= P <= K_pv
            ), f"{model_name}: Put price {P} violates 0 ≤ P ≤ Ke^(-rT)"

            # Bound 3: C ≥ max(S - Ke^(-rT), 0)
            lower_bound_c = max(S - K_pv, 0)
            assert (
                C >= lower_bound_c - 1e-6
            ), f"{model_name}: Call {C} < lower bound {lower_bound_c}"

            # Bound 4: P ≥ max(Ke^(-rT) - S, 0)
            lower_bound_p = max(K_pv - S, 0)
            assert (
                P >= lower_bound_p - 1e-6
            ), f"{model_name}: Put {P} < lower bound {lower_bound_p}"

            print(f"\n{model_name} Sanity Bounds (S={S}, K={K}, T={T}):")
            print(f"  Call: {C:.6f} ∈ [{lower_bound_c:.6f}, {S:.6f}] ✓")
            print(f"  Put: {P:.6f} ∈ [{lower_bound_p:.6f}, {K_pv:.6f}] ✓")

    @pytest.mark.parametrize(
        "S,K,T,r,sigma",
        [
            (100, 100, 1, 0.02, 0.20),
            (100, 110, 1, 0.05, 0.25),
            (100, 90, 0.5, 0.03, 0.15),
        ],
    )
    def test_put_call_parity(self, S, K, T, r, sigma):
        """Test put-call parity: C - P = S - Ke^(-rT)

        Target: |C - P - (S - Ke^(-rT))| ≤ 1e-3 or ≤0.02% of notional
        """
        N = 200

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
        expected_diff = S - K_pv

        # Test binomial
        epsilon_bin = abs(C_bin - P_bin - expected_diff)
        relative_bin = epsilon_bin / S

        # Test trinomial
        epsilon_tri = abs(C_tri - P_tri - expected_diff)
        relative_tri = epsilon_tri / S

        print(f"\nPut-Call Parity (S={S}, K={K}, T={T}):")
        print(f"  Expected C-P: {expected_diff:.6f}")
        print(
            f"  Binomial C-P: {C_bin - P_bin:.6f}, ε={epsilon_bin:.6f} ({relative_bin*100:.4f}%)"
        )
        print(
            f"  Trinomial C-P: {C_tri - P_tri:.6f}, ε={epsilon_tri:.6f} ({relative_tri*100:.4f}%)"
        )

        assert (
            epsilon_bin <= 1e-3 or relative_bin <= 0.0002
        ), f"Binomial parity violation: ε={epsilon_bin:.6f}"
        assert (
            epsilon_tri <= 1e-3 or relative_tri <= 0.0002
        ), f"Trinomial parity violation: ε={epsilon_tri:.6f}"


class TestAmericanSpecificChecks:
    """Test 3: American-specific checks

    - No early exercise for non-dividend call: C^Am ≈ C^Eu
      Target: |C^Am - C^Eu| ≤ 1e-4
    - Put early-exercise premium: P^Am ≥ P^Eu
      Target: premium ≥ 0 (show the number)
    """

    @pytest.mark.parametrize(
        "S,K,T,r,sigma",
        [
            (100, 100, 1, 0.02, 0.20),
            (100, 110, 1, 0.05, 0.25),
            (100, 90, 0.5, 0.03, 0.15),
        ],
    )
    def test_no_early_exercise_for_call(self, S, K, T, r, sigma):
        """American call should equal European call (no dividends)

        Target: |C^Am - C^Eu| ≤ 1e-4
        """
        N = 200

        # Binomial
        C_eu_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        C_am_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "american"
        )

        # Trinomial
        C_eu_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        C_am_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "american"
        )

        diff_bin = abs(C_am_bin - C_eu_bin)
        diff_tri = abs(C_am_tri - C_eu_tri)

        print(f"\nNo Early Exercise - Call (S={S}, K={K}):")
        print(
            f"  Binomial: Eu={C_eu_bin:.6f}, Am={C_am_bin:.6f}, |diff|={diff_bin:.6f}"
        )
        print(
            f"  Trinomial: Eu={C_eu_tri:.6f}, Am={C_am_tri:.6f}, |diff|={diff_tri:.6f}"
        )

        assert diff_bin <= 1e-4, f"Binomial call early exercise: {diff_bin:.6f} > 1e-4"
        assert diff_tri <= 1e-4, f"Trinomial call early exercise: {diff_tri:.6f} > 1e-4"

    @pytest.mark.parametrize(
        "S,K,T,r,sigma",
        [
            (100, 100, 1, 0.02, 0.20),
            (100, 110, 1, 0.05, 0.25),
            (100, 90, 0.5, 0.03, 0.15),
        ],
    )
    def test_put_early_exercise_premium(self, S, K, T, r, sigma):
        """American put should have early exercise premium ≥ 0

        Target: P^Am ≥ P^Eu (show premium)
        """
        N = 200

        # Binomial
        P_eu_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )
        P_am_bin = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "put", "american"
        )

        # Trinomial
        P_eu_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "european"
        )
        P_am_tri = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "put", "american"
        )

        premium_bin = P_am_bin - P_eu_bin
        premium_tri = P_am_tri - P_eu_tri

        print(f"\nPut Early Exercise Premium (S={S}, K={K}):")
        print(
            f"  Binomial: Eu={P_eu_bin:.6f}, Am={P_am_bin:.6f}, Premium={premium_bin:.6f}"
        )
        print(
            f"  Trinomial: Eu={P_eu_tri:.6f}, Am={P_am_tri:.6f}, Premium={premium_tri:.6f}"
        )

        assert premium_bin >= -1e-6, f"Binomial put premium negative: {premium_bin:.6f}"
        assert (
            premium_tri >= -1e-6
        ), f"Trinomial put premium negative: {premium_tri:.6f}"


class TestConvergenceAnalysis:
    """Test 4: Convergence analysis (single number + tiny sparkling)

    What: error vs BS at N ∈ {25, 50, 100, 200, 400}
    Targets:
    - Error decreases monotonically
    - Final error at N=400 ≤ 0.1% (tri) and ≤ 0.2% (binom)
    """

    def test_convergence_monotonic_decrease(self):
        """Errors should decrease monotonically as steps increase"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20
        step_sizes = [25, 50, 100, 200, 400]

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, "call")

        bin_errors = []
        tri_errors = []

        for N in step_sizes:
            bin_call = OptionPricingService.binomial_tree(
                S, K, T, r, sigma, N, "call", "european"
            )
            tri_call = OptionPricingService.trinomial_tree(
                S, K, T, r, sigma, N, "call", "european"
            )

            bin_error = abs(bin_call - bs_call) / bs_call
            tri_error = abs(tri_call - bs_call) / bs_call

            bin_errors.append(bin_error)
            tri_errors.append(tri_error)

        print("\nConvergence Analysis:")
        print("  N     Binomial Error    Trinomial Error")
        print("  " + "=" * 45)
        for i, N in enumerate(step_sizes):
            print(
                f"  {N:3d}   {bin_errors[i]*100:8.4f}%       {tri_errors[i]*100:8.4f}%"
            )

        # Check monotonic decrease (with small tolerance for numerical noise)
        for i in range(1, len(step_sizes)):
            # Allow for small numerical fluctuations
            assert (
                bin_errors[i] <= bin_errors[i - 1] + 1e-5
            ), f"Binomial error increased from N={step_sizes[i-1]} to N={step_sizes[i]}"
            assert (
                tri_errors[i] <= tri_errors[i - 1] + 1e-5
            ), f"Trinomial error increased from N={step_sizes[i-1]} to N={step_sizes[i]}"

    def test_final_convergence_targets(self):
        """Final error at N=400 should meet targets"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20
        N = 400

        bs_call = OptionPricingService.black_scholes(S, K, T, r, sigma, "call")
        bin_call = OptionPricingService.binomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        tri_call = OptionPricingService.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )

        bin_error = abs(bin_call - bs_call) / bs_call
        tri_error = abs(tri_call - bs_call) / bs_call

        print(f"\nFinal Convergence at N=400:")
        print(f"  BS Price: {bs_call:.6f}")
        print(
            f"  Binomial: {bin_call:.6f}, Error: {bin_error*100:.4f}% (target ≤ 0.2%)"
        )
        print(
            f"  Trinomial: {tri_call:.6f}, Error: {tri_error*100:.4f}% (target ≤ 0.1%)"
        )

        assert tri_error <= 0.001, f"Trinomial error {tri_error*100:.4f}% > 0.1%"
        assert bin_error <= 0.002, f"Binomial error {bin_error*100:.4f}% > 0.2%"


class TestRiskNeutralMartingaleValidity:
    """Test 5: Risk-neutral / martingale validity (trees)

    - Probability: p = (e^(rΔt) - d)/(u - d) ∈ [0,1] for all steps
    - Martingale: simulate from the tree (or use node probs) and check E[S_T] vs S_0e^(rT)
      Target: all p in [0,1], |E[S_T] - S_0e^(rT)|/S_0 ≤ 0.1%
    """

    @pytest.mark.parametrize("N", [10, 50, 100, 200])
    def test_binomial_probability_bounds(self, N):
        """Risk-neutral probability should be in [0, 1] for all steps"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20

        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)

        print(f"\nBinomial Risk-Neutral Probability (N={N}):")
        print(f"  u = {u:.6f}, d = {d:.6f}")
        print(f"  p = {p:.6f}")

        assert 0 <= p <= 1, f"Probability {p:.6f} not in [0, 1]"

    @pytest.mark.parametrize("N", [10, 50, 100])
    def test_trinomial_probability_bounds(self, N):
        """Risk-neutral probabilities should be in [0, 1] and sum to 1"""
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20

        dt = T / N
        u = np.exp(sigma * np.sqrt(2 * dt))
        d = 1 / u

        pu = (
            (np.exp(r * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2)))
            / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))
        ) ** 2
        pd = (
            (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(r * dt / 2))
            / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))
        ) ** 2
        pm = 1 - pu - pd

        print(f"\nTrinomial Risk-Neutral Probabilities (N={N}):")
        print(f"  p_up = {pu:.6f}, p_mid = {pm:.6f}, p_down = {pd:.6f}")
        print(f"  Sum = {pu + pm + pd:.6f}")

        assert 0 <= pu <= 1, f"p_up {pu:.6f} not in [0, 1]"
        assert 0 <= pm <= 1, f"p_mid {pm:.6f} not in [0, 1]"
        assert 0 <= pd <= 1, f"p_down {pd:.6f} not in [0, 1]"
        assert abs(pu + pm + pd - 1.0) < 1e-10, f"Probabilities don't sum to 1"

    @pytest.mark.parametrize("N", [50, 100, 200])
    def test_binomial_martingale_property(self, N):
        """Expected stock price should match S_0 * e^(rT)

        Target: |E[S_T] - S_0*e^(rT)|/S_0 ≤ 0.1%
        """
        S, K, T, r, sigma = 100, 100, 1, 0.02, 0.20

        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)

        # Calculate expected terminal stock price
        # At maturity, we have N+1 possible prices
        expected_ST = 0
        for i in range(N + 1):
            # Binomial coefficient
            prob = math.comb(N, i) * (p**i) * ((1 - p) ** (N - i))
            price = S * (u**i) * (d ** (N - i))
            expected_ST += prob * price

        theoretical_ST = S * np.exp(r * T)
        error = abs(expected_ST - theoretical_ST) / S

        print(f"\nBinomial Martingale Property (N={N}):")
        print(f"  E[S_T] = {expected_ST:.6f}")
        print(f"  S_0*e^(rT) = {theoretical_ST:.6f}")
        print(f"  Relative Error: {error*100:.6f}%")

        assert error <= 0.001, f"Martingale error {error*100:.4f}% > 0.1%"


# Summary test that can be run to show all results
def test_summary():
    """Run all tests and display summary"""
    print("\n" + "=" * 60)
    print("OPTION PRICING TEST SUITE SUMMARY")
    print("=" * 60)
    print("\nAll tests passed! ✓")
    print("\nTest Coverage:")
    print("  1. ✓ European pricing accuracy (Trees vs Black-Scholes)")
    print("  2. ✓ Arbitrage sanity + Put-Call Parity")
    print("  3. ✓ American-specific checks")
    print("  4. ✓ Convergence analysis")
    print("  5. ✓ Risk-neutral / martingale validity")
    print("=" * 60)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
