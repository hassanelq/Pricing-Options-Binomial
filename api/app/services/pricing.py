import numpy as np
from scipy.stats import norm
from typing import List


class OptionPricingService:
    """Service for calculating option prices using models with dividends."""

    # -------------------- validation --------------------

    @staticmethod
    def _validate_inputs(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
        N: int | None = None,
    ):
        """Validate input parameters."""
        if S <= 0:
            raise ValueError("Stock price S must be positive.")
        if K <= 0:
            raise ValueError("Strike price K must be positive.")
        if T < 0:
            raise ValueError("Time to maturity T must be non-negative.")
        if sigma < 0:
            raise ValueError("Volatility sigma must be non-negative.")
        if q < 0:
            raise ValueError("Dividend yield q must be non-negative.")
        if N is not None and N < 1:
            raise ValueError("Number of steps N must be at least 1.")

    # -------------------- Black–Scholes --------------------

    @staticmethod
    def black_scholes(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        q: float = 0.0,
        option_type: str = "call",
    ) -> float:
        """Black–Scholes price for European call/put with dividend yield q."""
        OptionPricingService._validate_inputs(S, K, T, r, sigma, q)

        # Maturity payoff
        if T == 0:
            return max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0)

        # Deterministic case (sigma=0)
        if sigma == 0:
            discS = S * np.exp(-q * T)
            discK = K * np.exp(-r * T)
            return (
                max(discS - discK, 0.0)
                if option_type == "call"
                else max(discK - discS, 0.0)
            )

        sqrtT = np.sqrt(T)
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
        d2 = d1 - sigma * sqrtT

        if option_type == "call":
            return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(
                -d1
            )

    # -------------------- Greeks (call, BS) --------------------

    @staticmethod
    def calculate_greeks(
        S: float, K: float, T: float, r: float, sigma: float, q: float = 0.0
    ) -> dict:
        """
        Black–Scholes Greeks for a CALL with dividend yield q.
        theta is per calendar day; vega and rho are per 1% change.
        """
        OptionPricingService._validate_inputs(S, K, T, r, sigma, q)

        # Degenerate cases
        if T == 0 or sigma == 0:
            return {
                "delta": 1.0 if S > K else 0.0,
                "gamma": 0.0,
                "theta": 0.0,
                "vega": 0.0,
                "rho": 0.0,
            }

        sqrtT = np.sqrt(T)
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma * sigma) * T) / (sigma * sqrtT)
        d2 = d1 - sigma * sqrtT

        nd1 = norm.pdf(d1)
        Nd1 = norm.cdf(d1)
        Nd2 = norm.cdf(d2)

        delta = np.exp(-q * T) * Nd1
        gamma = np.exp(-q * T) * nd1 / (S * sigma * sqrtT)
        theta = (
            -(S * np.exp(-q * T) * nd1 * sigma) / (2.0 * sqrtT)
            - r * K * np.exp(-r * T) * Nd2
            + q * S * np.exp(-q * T) * Nd1
        ) / 365.0
        vega = (S * np.exp(-q * T) * nd1 * sqrtT) / 100.0
        rho = (K * T * np.exp(-r * T) * Nd2) / 100.0

        return {
            "delta": float(delta),
            "gamma": float(gamma),
            "theta": float(theta),
            "vega": float(vega),
            "rho": float(rho),
        }

    # -------------------- Binomial (CRR) --------------------

    @staticmethod
    def binomial_tree(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int,
        q: float = 0.0,
        option_type: str = "call",
        exercise_type: str = "european",
    ) -> float:
        """CRR binomial tree for call/put, European/American with dividend yield q."""
        OptionPricingService._validate_inputs(S, K, T, r, sigma, q, N)

        if T == 0:
            return float(max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0))

        dt = T / N
        sqrt_dt = np.sqrt(dt)
        u = np.exp(sigma * sqrt_dt)
        d = 1.0 / u

        # Risk-neutral probability with dividend yield
        p = (np.exp((r - q) * dt) - d) / (u - d)
        disc = np.exp(-r * dt)

        # Terminal payoffs
        j = np.arange(N, -1, -1)
        asset = S * (u**j) * (d ** (N - j))
        vals = (
            np.maximum(asset - K, 0.0)
            if option_type == "call"
            else np.maximum(K - asset, 0.0)
        )

        # Backward induction
        for i in range(N - 1, -1, -1):
            vals = disc * (p * vals[:-1] + (1.0 - p) * vals[1:])
            if exercise_type == "american":
                asset = S * (u ** np.arange(i, -1, -1)) * (d ** np.arange(0, i + 1))
                intrinsic = (
                    np.maximum(asset - K, 0.0)
                    if option_type == "call"
                    else np.maximum(K - asset, 0.0)
                )
                vals = np.maximum(vals, intrinsic)

        return float(vals[0])

    # -------------------- Trinomial (Kamrad–Ritchken) --------------------

    @staticmethod
    def trinomial_tree(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int,
        q: float = 0.0,
        option_type: str = "call",
        exercise_type: str = "european",
    ) -> float:
        """
        Trinomial tree using Boyle (1988) parameterization with dividend yield q.
        u = exp(sigma * sqrt(2*dt)), d = 1/u, middle move m = 1
        Probabilities:
        pu = ((exp((r-q)*dt/2) - exp(-sigma*sqrt(dt/2))) /
                (exp( sigma*sqrt(dt/2)) - exp(-sigma*sqrt(dt/2))))**2
        pd = ((exp( sigma*sqrt(dt/2)) - exp((r-q)*dt/2)) /
                (exp( sigma*sqrt(dt/2)) - exp(-sigma*sqrt(dt/2))))**2
        pm = 1 - pu - pd
        """
        OptionPricingService._validate_inputs(S, K, T, r, sigma, q, N)

        if T == 0:
            return float(max(S - K, 0.0) if option_type == "call" else max(K - S, 0.0))

        dt = T / N
        if sigma == 0.0:
            # Deterministic limit consistent with BS branch
            discS = S * np.exp(-q * T)
            discK = K * np.exp(-r * T)
            return float(
                max(discS - discK, 0.0)
                if option_type == "call"
                else max(discK - discS, 0.0)
            )

        # Boyle up/down
        u = np.exp(sigma * np.sqrt(2.0 * dt))
        d = 1.0 / u

        a = np.exp((r - q) * dt / 2.0)
        b = np.exp(sigma * np.sqrt(dt / 2.0))
        invb = 1.0 / b

        denom = b - invb
        pu = ((a - invb) / denom) ** 2
        pd = ((b - a) / denom) ** 2
        pm = 1.0 - pu - pd

        # Validate probabilities with tiny tolerance
        eps = 1e-12
        if not (
            -eps <= pu <= 1.0 + eps
            and -eps <= pm <= 1.0 + eps
            and -eps <= pd <= 1.0 + eps
        ):
            raise ValueError(
                f"Invalid trinomial probabilities: pu={pu:.8f}, pm={pm:.8f}, pd={pd:.8f}. Increase N or adjust parameters."
            )

        disc = np.exp(-r * dt)

        # Terminal payoffs: size 2N+1, map idx 0..2N -> j in [-N..N]
        vals = np.empty(2 * N + 1)
        for idx in range(2 * N + 1):
            j = idx - N  # net up moves
            S_T = S * (u ** max(j, 0)) * (d ** max(-j, 0))
            vals[idx] = (
                max(S_T - K, 0.0) if option_type == "call" else max(K - S_T, 0.0)
            )

        # Backward induction
        for step in range(N - 1, -1, -1):
            new_vals = np.empty(2 * step + 1)
            for i in range(2 * step + 1):
                # Links to i (down), i+1 (mid), i+2 (up)
                cont = disc * (pu * vals[i + 2] + pm * vals[i + 1] + pd * vals[i])

                if exercise_type == "american":
                    j = i - step
                    S_it = S * (u ** max(j, 0)) * (d ** max(-j, 0))
                    intrinsic = (S_it - K) if option_type == "call" else (K - S_it)
                    intrinsic = intrinsic if intrinsic > 0.0 else 0.0
                    new_vals[i] = cont if cont > intrinsic else intrinsic
                else:
                    new_vals[i] = cont

            vals = new_vals

        return float(vals[0])

    # -------------------- Convergence curve --------------------

    @staticmethod
    def calculate_convergence(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        max_steps: int,
        q: float = 0.0,
        model: str = "binomial",
    ) -> List[dict]:
        """Compute tree price vs. steps to visualize convergence (call, European)."""
        convergence: List[dict] = []

        # Denser grid for small N, coarser for large
        step_sizes = (
            list(range(1, max_steps + 1))
            if max_steps <= 500
            else list(range(1, max_steps + 1, 3))
        )

        for steps in step_sizes:
            try:
                if model == "binomial":
                    price = OptionPricingService.binomial_tree(
                        S, K, T, r, sigma, steps, q, "call", "european"
                    )
                else:
                    price = OptionPricingService.trinomial_tree(
                        S, K, T, r, sigma, steps, q, "call", "european"
                    )
                convergence.append({"steps": steps, "price": float(price)})
            except ValueError:
                # Skip invalid parameter regions (e.g., probs out of bounds for tiny N)
                continue

        return convergence

    # -------------------- Early Exercise Boundary --------------------

    @staticmethod
    def calculate_early_exercise_boundary(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int,
        q: float = 0.0,
        option_type: str = "put",
        model: str = "binomial",
    ) -> List[dict]:
        """
        Calculate the early exercise boundary (optimal exercise frontier) for American options.
        Returns a list of critical stock prices at each time step where early exercise becomes optimal.
        """
        OptionPricingService._validate_inputs(S, K, T, r, sigma, q, N)

        dt = T / N
        boundary = []

        if model == "binomial":
            # Binomial tree parameters
            u = np.exp(sigma * np.sqrt(dt))
            d = 1.0 / u
            p = (np.exp((r - q) * dt) - d) / (u - d)
            disc = np.exp(-r * dt)

            # Build tree and find boundary
            # Terminal condition
            vals = np.zeros(N + 1)
            for i in range(N + 1):
                S_T = S * (u ** (N - i)) * (d**i)
                if option_type == "call":
                    vals[i] = max(S_T - K, 0.0)
                else:
                    vals[i] = max(K - S_T, 0.0)

            # Backward induction - find critical stock price at each time step
            for step in range(N - 1, -1, -1):
                t = step * dt
                new_vals = np.zeros(step + 1)

                # Find the critical stock price (exercise boundary) at this time step
                critical_price = None

                for i in range(step + 1):
                    S_it = S * (u ** (step - i)) * (d**i)

                    # Continuation value
                    cont = disc * (p * vals[i] + (1.0 - p) * vals[i + 1])

                    # Intrinsic value
                    if option_type == "call":
                        intrinsic = max(S_it - K, 0.0)
                    else:
                        intrinsic = max(K - S_it, 0.0)

                    # American option value
                    new_vals[i] = max(cont, intrinsic)

                    # Detect exercise boundary (where intrinsic >= continuation)
                    if intrinsic >= cont - 1e-10 and intrinsic > 0:
                        if option_type == "put":
                            # For puts, boundary is the highest S where exercise is optimal
                            if critical_price is None or S_it > critical_price:
                                critical_price = S_it
                        else:
                            # For calls, boundary is the lowest S where exercise is optimal
                            if critical_price is None or S_it < critical_price:
                                critical_price = S_it

                vals = new_vals

                if critical_price is not None:
                    boundary.append(
                        {
                            "time": float(t),
                            "stock_price": float(critical_price),
                            "time_to_maturity": float(T - t),
                        }
                    )

        else:  # trinomial
            # Trinomial tree parameters
            u = np.exp(sigma * np.sqrt(2.0 * dt))
            d = 1.0 / u
            m = 1.0

            a = np.exp((r - q) * dt / 2.0)
            b = np.exp(sigma * np.sqrt(dt / 2.0))
            pu = ((a - 1.0 / b) / (b - 1.0 / b)) ** 2
            pd = ((b - a) / (b - 1.0 / b)) ** 2
            pm = 1.0 - pu - pd
            disc = np.exp(-r * dt)

            # Build tree and find boundary
            # Terminal payoffs
            vals = np.zeros(2 * N + 1)
            for i in range(2 * N + 1):
                S_T = S * (u ** (N - i))
                if option_type == "call":
                    vals[i] = max(S_T - K, 0.0)
                else:
                    vals[i] = max(K - S_T, 0.0)

            # Backward induction
            for step in range(N - 1, -1, -1):
                t = step * dt
                new_vals = np.zeros(2 * step + 1)

                critical_price = None

                for i in range(2 * step + 1):
                    S_it = S * (u ** (step - i))

                    # Continuation value
                    cont = disc * (pu * vals[i] + pm * vals[i + 1] + pd * vals[i + 2])

                    # Intrinsic value
                    if option_type == "call":
                        intrinsic = max(S_it - K, 0.0)
                    else:
                        intrinsic = max(K - S_it, 0.0)

                    # American option value
                    new_vals[i] = max(cont, intrinsic)

                    # Detect exercise boundary
                    if intrinsic >= cont - 1e-10 and intrinsic > 0:
                        if option_type == "put":
                            if critical_price is None or S_it > critical_price:
                                critical_price = S_it
                        else:
                            if critical_price is None or S_it < critical_price:
                                critical_price = S_it

                vals = new_vals

                if critical_price is not None:
                    boundary.append(
                        {
                            "time": float(t),
                            "stock_price": float(critical_price),
                            "time_to_maturity": float(T - t),
                        }
                    )

        # Reverse to have time going forward
        boundary.reverse()
        return boundary

    # -------------------- Aggregate --------------------

    @classmethod
    def calculate_all(
        cls,
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        N: int,
        q: float = 0.0,
    ) -> dict:
        """Run BS, binomial, trinomial with dividend yield and return a summary."""
        cls._validate_inputs(S, K, T, r, sigma, q, N)

        # Black–Scholes
        bs_call = cls.black_scholes(S, K, T, r, sigma, q, "call")
        bs_put = cls.black_scholes(S, K, T, r, sigma, q, "put")
        greeks = cls.calculate_greeks(S, K, T, r, sigma, q)

        # Binomial
        bino_eu_c = cls.binomial_tree(S, K, T, r, sigma, N, q, "call", "european")
        bino_eu_p = cls.binomial_tree(S, K, T, r, sigma, N, q, "put", "european")
        # With dividends, American calls may be exercised early
        bino_am_c = cls.binomial_tree(S, K, T, r, sigma, N, q, "call", "american")
        bino_am_p = cls.binomial_tree(S, K, T, r, sigma, N, q, "put", "american")
        bino_conv = cls.calculate_convergence(S, K, T, r, sigma, N, q, "binomial")
        bino_boundary_put = cls.calculate_early_exercise_boundary(
            S, K, T, r, sigma, N, q, "put", "binomial"
        )
        bino_boundary_call = cls.calculate_early_exercise_boundary(
            S, K, T, r, sigma, N, q, "call", "binomial"
        )

        # Trinomial
        trino_eu_c = cls.trinomial_tree(S, K, T, r, sigma, N, q, "call", "european")
        trino_eu_p = cls.trinomial_tree(S, K, T, r, sigma, N, q, "put", "european")
        trino_am_c = cls.trinomial_tree(S, K, T, r, sigma, N, q, "call", "american")
        trino_am_p = cls.trinomial_tree(S, K, T, r, sigma, N, q, "put", "american")
        trino_conv = cls.calculate_convergence(S, K, T, r, sigma, N, q, "trinomial")
        trino_boundary_put = cls.calculate_early_exercise_boundary(
            S, K, T, r, sigma, N, q, "put", "trinomial"
        )
        trino_boundary_call = cls.calculate_early_exercise_boundary(
            S, K, T, r, sigma, N, q, "call", "trinomial"
        )

        return {
            "black_scholes": {
                "call_price": float(bs_call),
                "put_price": float(bs_put),
                "greeks": greeks,
            },
            "binomial": {
                "european_call": float(bino_eu_c),
                "european_put": float(bino_eu_p),
                "american_call": float(bino_am_c),
                "american_put": float(bino_am_p),
                "convergence": bino_conv,
                "boundary_put": bino_boundary_put,
                "boundary_call": bino_boundary_call,
            },
            "trinomial": {
                "european_call": float(trino_eu_c),
                "european_put": float(trino_eu_p),
                "american_call": float(trino_am_c),
                "american_put": float(trino_am_p),
                "convergence": trino_conv,
                "boundary_put": trino_boundary_put,
                "boundary_call": trino_boundary_call,
            },
        }
