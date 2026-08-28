# Actuarial Option Pricing & Risk Model

An Object-Oriented Programming (OOP) portfolio featuring both standard derivative pricing and actuarial risk modeling in Python. This repository includes a closed-form Black-Scholes-Merton model and a stochastic Monte Carlo engine designed to price Guaranteed Minimum Accumulation Benefits (GMAB) for life insurance products.

**Key Features**
* **Actuarial Risk Modeling:** Simulates Geometric Brownian Motion to calculate expected costs of Variable Annuity guarantees and visualize tail risk scenarios.
* **Risk Sensitivities:** Computes finite-difference Greeks (Delta) to measure portfolio sensitivity to market shocks.
* **OOP Architecture:** Encapsulates complex pricing logic inside reusable, production-grade Python classes.

**Project Structure**
```text
option-pricing-model/
├── src/
│   ├── black_scholes.py    # Standard European Call/Put pricing
│   └── monte_carlo.py      # Actuarial GMAB pricing and risk histograms
├── requirements.txt        # Project dependencies (numpy, scipy, matplotlib)
└── .gitignore