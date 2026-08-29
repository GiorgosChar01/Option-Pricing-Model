import numpy as np
import matplotlib.pyplot as plt

class MonteCarloPricer:
    def __init__(self, S, K, T, r, sigma, num_simulations=10000, num_steps=252):
        self.S = S          # Initial asset price
        self.K = K          # Strike price
        self.T = T          # Time to maturity (in years)
        self.r = r          # Risk-free interest rate
        self.sigma = sigma  # Volatility
        self.num_simulations = num_simulations
        self.num_steps = num_steps # Trading days in a year

    def simulate_paths(self):
        """
        Simulates asset price paths using Geometric Brownian Motion (GBM).
        Returns a 2D numpy array of shape (num_simulations, num_steps + 1)
        """
        # Time increment per step
        dt = self.T / self.num_steps
        
        # Generate a matrix of random normal shocks
        Z = np.random.standard_normal((self.num_simulations, self.num_steps))
        
        # Initialize the matrix to hold all price paths
        S_paths = np.zeros((self.num_simulations, self.num_steps + 1))
        S_paths[:, 0] = self.S # Set day 0 to the initial price
        
        # Calculate the daily price movements
        for t in range(1, self.num_steps + 1):
            drift = (self.r - 0.5 * self.sigma**2) * dt
            shock = self.sigma * np.sqrt(dt) * Z[:, t-1]
            S_paths[:, t] = S_paths[:, t-1] * np.exp(drift + shock)
            
        return S_paths

    def calculate_prices(self):
        """
        Calculates European Call and Put prices based on the simulated paths.
        """
        # 1. Generate the paths
        paths = self.simulate_paths()
        
        # 2. Extract the final prices at maturity (the last column of the matrix)
        final_prices = paths[:, -1]
        
        # 3. Calculate payoffs for both Calls and Puts
        call_payoffs = np.maximum(final_prices - self.K, 0)
        put_payoffs = np.maximum(self.K - final_prices, 0)
        
        # 4. Discount the average payoffs back to present value
        discount_factor = np.exp(-self.r * self.T)
        call_price = discount_factor * np.mean(call_payoffs)
        put_price = discount_factor * np.mean(put_payoffs)
        
        return call_price, put_price

    def plot_paths(self, paths, num_paths_to_plot=100):
        """Plots a subset of the simulated asset paths."""
        plt.figure(figsize=(10, 6))
        plt.plot(paths[:num_paths_to_plot].T, lw=1, alpha=0.8)
        plt.title(f"Monte Carlo Asset Paths ({num_paths_to_plot} Simulations)")
        plt.xlabel("Time Steps (Days)")
        plt.ylabel("Asset Price ($)")
        plt.grid(True, alpha=0.3)
        plt.show()

    def plot_price_distribution(self, paths):
        """Plots the histogram of final asset prices at maturity."""
        final_prices = paths[:, -1]
        plt.figure(figsize=(10, 6))
        plt.hist(final_prices, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        plt.axvline(self.K, color='red', linestyle='dashed', linewidth=2, label=f'Strike Price (${self.K})')
        plt.title("Distribution of Final Asset Prices at Maturity")
        plt.xlabel("Final Asset Price ($)")
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.show()

# Execution block to test the simulation
if __name__ == "__main__":
    # Standard testing parameters
    S = 100.0   
    K = 100.0   
    T = 1.0     
    r = 0.05    
    sigma = 0.2 
    
    pricer = MonteCarloPricer(S, K, T, r, sigma, num_simulations=100000)
    
    # 1. Calculate and print the prices
    call_price, put_price = pricer.calculate_prices()
    print(f"Monte Carlo Call Price: ${call_price:.2f}")
    print(f"Monte Carlo Put Price:  ${put_price:.2f}")
    
    # 2. Generate paths for visualization
    paths = pricer.simulate_paths()
    
    # 3. Trigger the pop-up graphs
    pricer.plot_paths(paths, num_paths_to_plot=150)
    pricer.plot_price_distribution(paths)