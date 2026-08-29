# Actuarial Option Pricing & Risk Model

A Python-based financial engineering repository implementing both theoretical Black-Scholes pricing and stochastic Monte Carlo simulations for European options.

## Key Features
* **Black-Scholes Engine:** Calculates exact theoretical European Call and Put prices.
* **Monte Carlo Simulator:** Generates stochastic asset paths using Geometric Brownian Motion (GBM).
* **Risk Visualizations:** Outputs Matplotlib histograms and path trajectories for visual risk analysis.
* **OOP Architecture:** Encapsulates complex pricing logic inside reusable, production-grade Python classes.

## Project Structure
```text
option-pricing-model/
├── src/
│   ├── black_scholes.py    # Standard European Call/Put pricing
│   └── monte_carlo.py      # Actuarial GMAB pricing & risk
├── requirements.txt        # Project dependencies
└── .gitignore
```

## Installation and Setup

**Clone the repository and install dependencies:**
```bash
git clone [https://github.com/GiorgosChar01/Option-Pricing-Model.git](https://github.com/GiorgosChar01/Option-Pricing-Model.git)
cd Option-Pricing-Model
pip install -r requirements.txt
```

## Usage

**Run the Black-Scholes Model:**
Executes the theoretical pricing engine.
```bash
python src/black_scholes.py
```

**Run the Monte Carlo Simulator:**
Executes the stochastic pricing engine and generates pop-up Matplotlib visualizations for the asset paths and final price distribution.
```bash
python src/monte_carlo.py
```