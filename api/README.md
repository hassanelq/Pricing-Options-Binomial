# Option Pricing API

Simple FastAPI application for calculating option prices using Black-Scholes, Binomial, and Trinomial models.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the API:

```bash
cd api
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoint

### POST `/api/calculate`

Calculate option prices using all three models.

**Request Body:**

```json
{
  "spotPrice": 100,
  "strike": 100,
  "timeToMaturity": 1,
  "riskFreeRate": 0.02,
  "volatility": 0.2,
  "treeSteps": 200
}
```

**Response:**

```json
{
  "black_scholes": {
    "call_price": 10.45,
    "put_price": 8.52,
    "greeks": {
      "delta": 0.594,
      "gamma": 0.019,
      "theta": -0.012,
      "vega": 0.397,
      "rho": 0.532
    }
  },
  "binomial": {
    "european_call": 10.45,
    "european_put": 8.52,
    "american_call": 10.45,
    "american_put": 8.68,
    "convergence": [2.1, 1.3, 0.8, 0.5, 0.3, 0.2, 0.1, 0.05]
  },
  "trinomial": {
    "european_call": 10.45,
    "european_put": 8.52,
    "american_call": 10.45,
    "american_put": 8.69,
    "convergence": [1.8, 1.1, 0.7, 0.4, 0.25, 0.15, 0.08, 0.04]
  }
}
```

## Models

- **Black-Scholes**: Analytical solution for European options
- **Binomial Tree**: Discrete-time model supporting both European and American options
- **Trinomial Tree**: Three-branch tree model for better convergence

## Testing

Test the API using the provided script:

```bash
python test_api.py
```

Or visit the interactive documentation at `http://localhost:8000/docs`
