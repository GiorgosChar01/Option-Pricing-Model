import numpy as np
import matplotlib.pyplot as plt

class ActuarialMonteCarlo:
    """
    Actuarial Monte Carlo engine for pricing Variable Annuities.
    Models both Accumulation Benefits (GMAB) and Death Benefits (GMDB) 
    by integrating financial market simulations with mortality decrements.
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

    def price_gmab(self, paths, survival_probability=0.85):
        """
        Calculates GMAB cost. The insurer only pays the maturity shortfall 
        IF the policyholder survives to the end of the 10-year term.
        """
        terminal_prices = paths[-1]
        shortfall = np.maximum(self.K - terminal_prices, 0)
        discount_factor = np.exp(-self.r * self.T)
        
        # Actuarial Present Value = Financial PV * Probability of Survival (tPx)
        return discount_factor * np.mean(shortfall) * survival_probability

    def price_gmdb(self, paths, annual_mortality_rate=0.015):
        """
        Calculates GMDB cost. The insurer pays the shortfall if the market 
        is down AT THE EXACT YEAR the policyholder dies.
        """
        gmdb_cost = 0.0
        trading_days_per_year = int(self.num_steps / self.T)
        
        # Check the portfolio value and mortality risk at each annual anniversary
        for year in range(1, int(self.T) + 1):
            step = year * trading_days_per_year
            prices_at_year = paths[step]
            shortfall = np.maximum(self.K - prices_at_year, 0)
            
            discount_factor = np.exp(-self.r * year)
            
            # Probability of surviving prior years, but dying in THIS specific year (q_x)
            survival_prior = (1 - annual_mortality_rate) ** (year - 1)
            prob_death_this_year = survival_prior * annual_mortality_rate
            
            gmdb_cost += discount_factor * np.mean(shortfall) * prob_death_this_year
            
        return gmdb_cost

    def plot_portfolio_paths(self, paths, num_paths=100):
        """Visualizes the stochastic portfolio paths against the guarantee."""
        plt.figure(figsize=(10, 6))
        plt.plot(paths[:, :num_paths], lw=1, alpha=0.5)
        plt.axhline(self.K, color='black', linestyle='dashed', linewidth=2, label=f'Guarantee Level (${self.K:,.0f})')
        plt.title('Variable Annuity: Simulated Portfolio Paths (10 Years)')
        plt.xlabel('Trading Days')
        plt.ylabel('Fund Value ($)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

if __name__ == "__main__":
    # 10-year policy, $100k premium, 4% risk-free rate, 15% market volatility
    model = ActuarialMonteCarlo(S=100000.0, K=100000.0, T=10.0, r=0.04, sigma=0.15, num_simulations=50000)
    
    print("Simulating 50,000 portfolio paths...")
    base_paths = model.generate_paths()
    
    # 85% chance to survive 10 years
    gmab_cost = model.price_gmab(base_paths, survival_probability=0.85) 
    
    # 1.5% chance of death each year
    gmdb_cost = model.price_gmdb(base_paths, annual_mortality_rate=0.015)
    
    print("-" * 40)
    print(f"Expected Cost of GMAB (Survival Benefit): ${gmab_cost:,.2f}")
    print(f"Expected Cost of GMDB (Death Benefit):    ${gmdb_cost:,.2f}")
    print(f"Total Guarantee Liability:                ${(gmab_cost + gmdb_cost):,.2f}")
    print("-" * 40)
    
    print("Generating path visualization...")
    model.plot_portfolio_paths(base_paths)