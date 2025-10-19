# Option Pricing Application# Quant Pricing Web App

A web application for pricing options using Black-Scholes, Binomial, and Trinomial methods.Production-ready demo stack for option pricing and tree visualization.

## Project Structure- Backend: FastAPI (Python) exposing `/api/*` for pricing (binomial/trinomial), Greeks, convergence, and calibration (implied vol + smile fit). CORS and shared-token auth supported.

- Frontend: Next.js (App Router, TypeScript) with Tailwind + minimal shadcn-style components, pages for Pricing and Trees visualization with charts via Plotly.

````- DevOps: Dockerfiles for both, docker-compose to run together, GitHub Actions CI to lint/test/build.

binomial/

├── api/                          # FastAPI Backend## Quick Start

│   ├── app/

│   │   ├── main.py              # FastAPI app entry point- Prereqs: Python 3.11+, Node 20+, Docker (optional)

│   │   ├── routers/

│   │   │   ├── pricing.py       # Pricing endpoints (3 endpoints)### Dev (local)

│   │   │   └── __init__.py

│   │   ├── schemas/Backend:

│   │   │   ├── common.py        # Enums: OptionType, ExerciseType, MethodType

│   │   │   └── pricing.py       # Request/Response models```

│   │   └── services/cd api

│   │       ├── black_scholes.py # BS pricing & analytical Greekscp .env.example .env  # set AUTH_TOKEN if desired

│   │       ├── pricing.py       # Binomial/Trinomial pricing & Greekspip install -r requirements.txt

│   │       └── convergence.py   # Convergence analysisuvicorn app.main:app --reload --port 8000

│   ├── requirements.txt         # Python dependencies```

│   └── Dockerfile              # Docker image for API

│Frontend:

├── web/                         # Next.js Frontend

│   ├── app/```

│   │   ├── page.tsx            # Home pagecd web

│   │   ├── layout.tsx          # Root layoutcp .env.example .env  # set NEXT_PUBLIC_API_BASE_URL and NEXT_PUBLIC_AUTH_TOKEN to match

│   │   └── pricing/npm install

│   │       └── page.tsx        # Main pricing page (100 lines)npm run dev

│   ├── components/```

│   │   ├── Plot.tsx            # Plotly chart wrapper

│   │   ├── TreePlot.tsx        # Tree visualizationNavigate to `http://localhost:3000/pricing` and `http://localhost:3000/trees`.

│   │   ├── pricing/            # Pricing page components (7 files)

│   │   │   ├── InputForm.tsx### Docker

│   │   │   ├── BlackScholesSection.tsx

│   │   │   ├── TreeModelSection.tsx```

│   │   │   ├── SummarySection.tsxdocker compose up --build

│   │   │   ├── GreeksCard.tsx```

│   │   │   ├── GreeksPlot.tsx

│   │   │   └── ConvergencePlot.tsx- Web at `http://localhost:3000`

│   │   └── ui/                 # Reusable UI components- API at `http://localhost:8000`

│   │       ├── button.tsx

│   │       └── input.tsx### Tests

│   ├── hooks/

│   │   └── usePricingCalculations.ts  # API calls logic```

│   ├── lib/cd api

│   │   ├── api.ts              # API clientpytest -q

│   │   └── trees.ts            # Tree building logic```

│   ├── types/                   # TypeScript definitions

│   ├── package.json            # Dependencies## API Overview

│   └── Dockerfile              # Docker image for web

│- `POST /api/pricing/option`: price under binomial/trinomial (European/American), supports dividend yield `q` and optional discrete dividends (approximate via PV adjustment).

└── docker-compose.yml          # Run both services- `POST /api/pricing/greeks`: Greeks via bump-and-reprice for tree methods.

```- `POST /api/pricing/convergence`: series of (steps, tree_price, bs_price) for plotting.

- (Optional) Calibration endpoints remain available: `/api/calibration/implied-vol` and `/api/calibration/fit-curve`.

## API Endpoints

Auth: disabled (no token required).

### Base URL: `http://localhost:8000`

OpenAPI docs at `/docs`.

1. **Price Options** - `/api/pricing/option` (POST)

   - Input: method, market params, option params, steps## Environment

   - Output: option price

Backend (`api/.env`):

2. **Calculate Greeks** - `/api/pricing/greeks` (POST)

   - Input: same as above- `APP_NAME`, `APP_ENV`, `APP_HOST`, `APP_PORT`

   - Output: price + 5 Greeks (delta, gamma, theta, vega, rho)- `LOG_LEVEL` (info, debug, warning)

- `ALLOWED_ORIGINS` (comma-separated)

3. **Convergence Analysis** - `/api/pricing/convergence` (POST)- `AUTH_TOKEN` (shared password)

   - Input: method, range of steps

   - Output: array of {steps, tree_price, bs_price}Frontend (`web/.env`):



## Data Flow- `NEXT_PUBLIC_API_BASE_URL` (e.g., `http://localhost:8000`)



### Input Parameters## Deployment Notes

```typescript

form = {- API: Deploy to Render/Fly.io using the provided Dockerfile. Expose port 8000. Set `ALLOWED_ORIGINS` to your web origin and `AUTH_TOKEN`.

  s0: number      // Spot price- Web: Deploy to Vercel. Set `NEXT_PUBLIC_API_BASE_URL` to your API URL.

  k: number       // Strike price

  t: number       // Time to maturity## Project Structure

  r: number       // Risk-free rate

  sigma: number   // Volatility- `api/`: FastAPI app

  steps: number   // Tree steps  - `app/`: routers, services, schemas, config

}  - `tests/`: pytest unit tests (parity, convergence, no-arbitrage)

```  - `Dockerfile`, `requirements.txt`

- `web/`: Next.js app

### Processing  - `app/`: App Router pages (Pricing, Trees)

1. User fills form → clicks "Price Options"  - `components/`: minimal UI

2. `usePricingCalculations.calculateAll(form)` executes  - `lib/`: API client

3. Makes ~108 API calls in parallel:  - `Dockerfile`

   - 2 BS prices

   - 2 BS Greeks at spot## Notes

   - 200 BS Greeks for plots (100 call + 100 put)

   - 4 Binomial prices (Eur/Am Call/Put)- Trinomial uses Kamrad–Ritchken-style parameters; binomial uses CRR. Discrete dividends are approximated via PV spot adjustment for simplicity.

   - 1 Binomial convergence- Greeks for tree methods via finite differences; Black–Scholes used for convergence/IV.

   - 4 Trinomial prices- This is a concise demo suitable for stakeholder review; extend as needed for production requirements.

   - 1 Trinomial convergence
4. Results displayed in 4 sections

### Output Structure
```typescript
results = {
  blackScholes: {
    callPrice, putPrice,
    callGreeks, putGreeks,
    callGreeksPlot[100], putGreeksPlot[100]
  },
  binomial: {
    europeanCall, europeanPut,
    americanCall, americanPut,
    convergence[], tree
  },
  trinomial: {
    europeanCall, europeanPut,
    americanCall, americanPut,
    convergence[], tree
  }
}
````

## Quick Start

### Option 1: Docker

```bash
docker-compose up
```

- API: http://localhost:8000
- Web: http://localhost:3000

### Option 2: Local Development

**Backend:**

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd web
npm install
npm run dev
```

## Key Features

- **3 Pricing Methods**: Black-Scholes (analytical), Binomial Tree, Trinomial Tree
- **2 Exercise Types**: European, American
- **5 Greeks**: Delta, Gamma, Theta, Vega, Rho
- **Smooth Greeks Plots**: 100 points using BS analytical formulas
- **Tree Visualization**: Interactive binomial/trinomial trees
- **Convergence Analysis**: See how tree methods converge to BS

## Tech Stack

- **Backend**: FastAPI (Python 3.13), NumPy, SciPy
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Plotly.js
- **Containerization**: Docker, docker-compose
