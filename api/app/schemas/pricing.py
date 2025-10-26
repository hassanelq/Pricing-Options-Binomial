from pydantic import BaseModel, Field
from typing import List


class PricingRequest(BaseModel):
    spot_price: float = Field(..., alias="spotPrice")
    strike: float = Field(..., alias="strike")
    time_to_maturity: float = Field(..., alias="timeToMaturity")
    risk_free_rate: float = Field(..., alias="riskFreeRate")
    volatility: float = Field(..., alias="volatility")
    tree_steps: int = Field(..., alias="treeSteps")
    dividend_yield: float = Field(0.0, alias="dividendYield")


class Greeks(BaseModel):
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


class BlackScholesResult(BaseModel):
    call_price: float
    put_price: float
    greeks: Greeks


class ConvergencePoint(BaseModel):
    steps: int
    price: float


class BoundaryPoint(BaseModel):
    time: float
    stock_price: float
    time_to_maturity: float


class TreeResult(BaseModel):
    european_call: float
    european_put: float
    american_call: float
    american_put: float
    convergence: List[ConvergencePoint]
    boundary_put: List[BoundaryPoint]
    boundary_call: List[BoundaryPoint]


class TestResult(BaseModel):
    name: str
    passed: bool
    value: float
    target: float
    unit: str = "%"


class TestCategory(BaseModel):
    name: str
    tests: List[TestResult]
    all_passed: bool


class ValidationResults(BaseModel):
    categories: List[TestCategory]
    overall_passed: bool
    total_tests: int
    passed_tests: int


class PricingResponse(BaseModel):
    black_scholes: BlackScholesResult
    binomial: TreeResult
    trinomial: TreeResult
    validation: ValidationResults
