import numpy as np
from scipy.stats import norm
from typing import List


class OptionPricingService:
    """Service for calculating option prices using models"""

    @staticmethod
    def _validate_inputs(
        S: float, K: float, T: float, r: float, sigma: float, N: int = None
    ):
        """Validate input parameters"""
        if S <= 0:
            raise ValueError("Stock price S must be positive")
        if K <= 0:
            raise ValueError("Strike price K must be positive")
        if T < 0:
            raise ValueError("Time to maturity T must be non-negative")
        if sigma < 0:
            raise ValueError("Volatility sigma must be non-negative")
        if N is not None and N < 1:
            raise ValueError("Number of steps N must be at least 1")

    @staticmethod
    def black_scholes(
        S: float, K: float, T: float, r: float, sigma: float, option_type: str = "call"
    ) -> float:
        """Calculate Black-Scholes option price"""
        OptionPricingService._validate_inputs(S, K, T, r, sigma)

        # Handle edge case: at maturity
        if T == 0:
            if option_type == "call":
                return max(S - K, 0)
            else:
                return max(K - S, 0)

        # Handle edge case: zero volatility
        if sigma == 0:
            if option_type == "call":
                return max(S - K * np.exp(-r * T), 0)
            else:
                return max(K * np.exp(-r * T) - S, 0)

        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if option_type == "call":
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:  # put
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return price

    @staticmethod
    def calculate_greeks(S: float, K: float, T: float, r: float, sigma: float) -> dict:
        """Calculate option Greeks for a call option"""
        OptionPricingService._validate_inputs(S, K, T, r, sigma)

        # Handle edge cases
        if T == 0 or sigma == 0:
            return {
                "delta": 1.0 if S > K else 0.0,
                "gamma": 0.0,
                "theta": 0.0,
                "vega": 0.0,
                "rho": 0.0,
            }

        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = (
            -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * norm.cdf(d2)
        ) / 365
        vega = S * norm.pdf(d1) * np.sqrt(T) / 100
        rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100

        return {
            "delta": delta,
            "gamma": gamma,
            "theta": theta,
            "vega": vega,
            "rho": rho,
        }

    @staticmethod
    def binomial_tree(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int,
        option_type: str = "call",
        exercise_type: str = "european",
    ) -> float:
        """Calculate option price using binomial tree model (CRR)"""
        OptionPricingService._validate_inputs(S, K, T, r, sigma, N)

        dt = T / N
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp(r * dt) - d) / (u - d)
        discount = np.exp(-r * dt)

        # Initialize asset prices at maturity
        asset_prices = S * (u ** np.arange(N, -1, -1)) * (d ** np.arange(0, N + 1))

        # Initialize option values at maturity
        if option_type == "call":
            option_values = np.maximum(asset_prices - K, 0)
        else:  # put
            option_values = np.maximum(K - asset_prices, 0)

        # Backward induction
        for j in range(N - 1, -1, -1):
            # Update asset prices for this time step
            asset_prices = S * (u ** np.arange(j, -1, -1)) * (d ** np.arange(0, j + 1))

            # Discounted expected value
            option_values = discount * (
                p * option_values[:-1] + (1 - p) * option_values[1:]
            )

            # For American options, check early exercise
            if exercise_type == "american":
                if option_type == "call":
                    intrinsic = np.maximum(asset_prices - K, 0)
                else:
                    intrinsic = np.maximum(K - asset_prices, 0)
                option_values = np.maximum(option_values, intrinsic)

        return float(option_values[0])

    @staticmethod
    def trinomial_tree(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int,
        option_type: str = "call",
        exercise_type: str = "european",
    ) -> float:
        """Calculate option price using trinomial tree model (Boyle method)"""
        OptionPricingService._validate_inputs(S, K, T, r, sigma, N)

        dt = T / N
        u = np.exp(sigma * np.sqrt(2 * dt))
        d = 1 / u
        m = 1  # middle node stays at current price

        # Boyle (1988) probabilities - corrected formulas
        pu = (
            (np.exp(r * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2)))
            / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))
        ) ** 2
        pd = (
            (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(r * dt / 2))
            / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2)))
        ) ** 2
        pm = 1 - pu - pd

        # Validate probabilities
        if not (0 <= pu <= 1 and 0 <= pd <= 1 and 0 <= pm <= 1):
            raise ValueError(
                f"Invalid probabilities: pu={pu:.4f}, pm={pm:.4f}, pd={pd:.4f}"
            )

        discount = np.exp(-r * dt)

        # Initialize option values at maturity (step N)
        option_values = np.zeros(2 * N + 1)

        for i in range(2 * N + 1):
            j = i - N  # net number of up moves
            stock_price = S * (u ** max(j, 0)) * (d ** max(-j, 0))

            if option_type == "call":
                option_values[i] = max(stock_price - K, 0)
            else:
                option_values[i] = max(K - stock_price, 0)

        # Backward induction through the tree
        for step in range(N - 1, -1, -1):
            new_values = np.zeros(2 * step + 1)

            for i in range(2 * step + 1):
                # This node connects to nodes i, i+1, i+2 in the next level
                new_values[i] = discount * (
                    pu * option_values[i + 2]
                    + pm * option_values[i + 1]
                    + pd * option_values[i]
                )

                # For American options, check early exercise
                if exercise_type == "american":
                    j = i - step
                    stock_price = S * (u ** max(j, 0)) * (d ** max(-j, 0))

                    if option_type == "call":
                        intrinsic = max(stock_price - K, 0)
                    else:
                        intrinsic = max(K - stock_price, 0)

                    new_values[i] = max(new_values[i], intrinsic)

            option_values = new_values

        return float(option_values[0])

    @staticmethod
    def calculate_convergence(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        max_steps: int,
        model: str = "binomial",
    ) -> List[dict]:
        """Calculate convergence to Black-Scholes as steps increase"""
        convergence = []

        # Determine step sizes for better visualization
        if max_steps <= 500:
            step_sizes = list(range(1, max_steps + 1, 1))
        else:
            step_sizes = list(range(1, max_steps + 1, 3))

        for steps in step_sizes:
            try:
                if model == "binomial":
                    price = OptionPricingService.binomial_tree(
                        S, K, T, r, sigma, steps, "call", "european"
                    )
                else:  # trinomial
                    price = OptionPricingService.trinomial_tree(
                        S, K, T, r, sigma, steps, "call", "european"
                    )
                convergence.append({"steps": steps, "price": float(price)})
            except ValueError as e:
                # Skip steps that produce invalid probabilities
                continue

        return convergence

    @classmethod
    def calculate_all(
        cls, S: float, K: float, T: float, r: float, sigma: float, N: int
    ) -> dict:
        """Calculate all pricing models and return results"""
        cls._validate_inputs(S, K, T, r, sigma, N)

        # Black-Scholes
        bs_call = cls.black_scholes(S, K, T, r, sigma, "call")
        bs_put = cls.black_scholes(S, K, T, r, sigma, "put")
        greeks = cls.calculate_greeks(S, K, T, r, sigma)

        # Binomial Tree
        binomial_euro_call = cls.binomial_tree(S, K, T, r, sigma, N, "call", "european")
        binomial_euro_put = cls.binomial_tree(S, K, T, r, sigma, N, "put", "european")
        # American call = European call for non-dividend stocks
        binomial_amer_call = binomial_euro_call
        binomial_amer_put = cls.binomial_tree(S, K, T, r, sigma, N, "put", "american")
        binomial_convergence = cls.calculate_convergence(
            S, K, T, r, sigma, N, "binomial"
        )

        # Trinomial Tree
        trinomial_euro_call = cls.trinomial_tree(
            S, K, T, r, sigma, N, "call", "european"
        )
        trinomial_euro_put = cls.trinomial_tree(S, K, T, r, sigma, N, "put", "european")
        trinomial_amer_call = trinomial_euro_call
        trinomial_amer_put = cls.trinomial_tree(S, K, T, r, sigma, N, "put", "american")
        trinomial_convergence = cls.calculate_convergence(
            S, K, T, r, sigma, N, "trinomial"
        )

        return {
            "black_scholes": {
                "call_price": float(bs_call),
                "put_price": float(bs_put),
                "greeks": greeks,
            },
            "binomial": {
                "european_call": float(binomial_euro_call),
                "european_put": float(binomial_euro_put),
                "american_call": float(binomial_amer_call),
                "american_put": float(binomial_amer_put),
                "convergence": binomial_convergence,
            },
            "trinomial": {
                "european_call": float(trinomial_euro_call),
                "european_put": float(trinomial_euro_put),
                "american_call": float(trinomial_amer_call),
                "american_put": float(trinomial_amer_put),
                "convergence": trinomial_convergence,
            },
        }
