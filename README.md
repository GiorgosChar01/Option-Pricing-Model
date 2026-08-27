# Option Pricing Model

A clean, Object-Oriented Programming (OOP) implementation of the Black-Scholes-Merton model in Python for pricing European Call and Put options. Designed as a quantitative finance portfolio piece.

**Key Features**
* **OOP Architecture:** Encapsulates pricing logic inside a reusable `BlackScholesModel` class.
* **Mathematical Rigor:** Computes $d_1$ and $d_2$ parameters efficiently using `numpy` and calculates cumulative normal distributions via `scipy.stats.norm`.
* **Clean Separation:** Follows a standard `src` layout for maintainable, production-grade code structure.

**Project Structure**
```text
option-pricing-model/
├── src/
│   └── black_scholes.py    # Core pricing class and execution example
├── requirements.txt        # Project dependencies
└── .gitignore              # Files excluded from version control
