import numpy as np
import matplotlib.pyplot as plt

class ActuarialMonteCarlo:
    """
    Actuarial Monte Carlo engine for pricing Variable Annuities (GMAB) 
    and calculating risk sensitivities (Delta).
    """
    def __init__(self, S, K, T, r, sigma, num_simulations=10000, num_steps=252):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.num_simulations = num_simulations
        self.num_steps = num_steps
        self.dt = T / num_steps

    def generate_paths(self, S_initial=None):
        """Simulates equity paths using Geometric Brownian Motion."""
        S0 = S_initial if S_initial is not None else self.S
        Z = np.random.standard_normal((self.num_steps, self.num_simulations))
        paths = np.zeros((self.num_steps + 1, self.num_simulations))
        paths[0] = S0
        for t in range(1, self.num_steps + 1):
            paths[t] = paths[t - 1] * np.exp((self.r - 0.5 * self.sigma ** 2) * self.dt + 
                                             self.sigma * np.sqrt(self.dt) * Z[t - 1])
        return paths

    def price_gmab(self, paths):
        """Calculates the expected cost of a Guaranteed Minimum Accumulation Benefit."""
        terminal_prices = paths[-1]
        shortfall = np.maximum(self.K - terminal_prices, 0)
        discount_factor = np.exp(-self.r * self.T)
        return discount_factor * np.mean(shortfall)

    def calculate_delta(self):
        """Calculates Delta using the finite difference method."""
        bump = 1.0
        paths_up = self.generate_paths(S_initial=self.S + bump)
        paths_down = self.generate_paths(S_initial=self.S - bump)
        
        price_up = self.price_gmab(paths_up)
        price_down = self.price_gmab(paths_down)
        
        return (price_up - price_down) / (2 * bump)

    def plot_risk_distribution(self, paths):
        """Plots the terminal value distribution and highlights insurer tail risk."""
        terminal_prices = paths[-1]
        plt.figure(figsize=(10, 6))
        n, bins, patches = plt.hist(terminal_prices, bins=100, alpha=0.75, color='blue', edgecolor='black')
        
        for c, p in zip(bins, patches):
            if c < self.K:
                plt.setp(p, 'facecolor', 'red')
                
        plt.axvline(self.K, color='black', linestyle='dashed', linewidth=2, label=f'GMAB Guarantee (${self.K:,.0f})')
        plt.title('Variable Annuity Portfolio Value Distribution\n(Red indicates Insurer Payout/Tail Risk)')
        plt.xlabel('Portfolio Value at Maturity ($)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    model = ActuarialMonteCarlo(S=100000.0, K=100000.0, T=10.0, r=0.04, sigma=0.15, num_simulations=50000)
    
    print("Simulating 50,000 portfolio paths...")
    base_paths = model.generate_paths()
    
    gmab_cost = model.price_gmab(base_paths)
    print(f"Expected Cost of GMAB Guarantee: ${gmab_cost:,.2f}")
    
    delta = model.calculate_delta()
    print(f"Risk Sensitivity (Delta): {delta:.4f}")
    
    print("Generating risk distribution chart...")
    model.plot_risk_distribution(base_paths)