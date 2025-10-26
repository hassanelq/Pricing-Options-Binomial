from fastapi import APIRouter, HTTPException
from ..schemas.pricing import PricingRequest, PricingResponse
from ..services.pricing import OptionPricingService
from ..services.validation import ValidationService

router = APIRouter(prefix="/api", tags=["pricing"])


@router.post("/calculate", response_model=PricingResponse)
async def calculate_option_prices(request: PricingRequest):
    """
    Calculate option prices using Black-Scholes, Binomial, and Trinomial models.

    Takes spot price, strike, time to maturity, risk-free rate, volatility, dividend yield, and tree steps.
    Returns pricing results from all three models including Greeks, convergence data, and validation tests.
    """
    try:
        # Calculate all pricing models
        results = OptionPricingService.calculate_all(
            S=request.spot_price,
            K=request.strike,
            T=request.time_to_maturity,
            r=request.risk_free_rate,
            sigma=request.volatility,
            N=request.tree_steps,
            q=request.dividend_yield,
        )

        # Run validation tests
        validation = ValidationService.run_all_validations(
            S=request.spot_price,
            K=request.strike,
            T=request.time_to_maturity,
            r=request.risk_free_rate,
            sigma=request.volatility,
            N=request.tree_steps,
            q=request.dividend_yield,
        )

        # Combine results
        results["validation"] = validation

        return PricingResponse(**results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Calculation error: {str(e)}")
