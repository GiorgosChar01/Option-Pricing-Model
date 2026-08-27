import numpy as np
from scipy.stats import norm

class BlackScholesModel:
    """
    Black-Scholes pricing model for European Call and Put options.
    """
    def __init__(self, S, K, T, r, sigma):
        self.S = S          
        self.K = K          
        self.T = T          
        self.r = r          
        self.sigma = sigma  

    def _d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
    
    def _d2(self):
        return self._d1() - self.sigma * np.sqrt(self.T)
    
    def call_price(self):
        return self.S * norm.cdf(self._d1()) - self.K * np.exp(-self.r * self.T) * norm.cdf(self._d2())
        
    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self._d2()) - self.S * norm.cdf(-self._d1())

if __name__ == "__main__":
    model = BlackScholesModel(S=100.0, K=100.0, T=1.0, r=0.05, sigma=0.20)
    print(f"European Call Price: ${model.call_price():.2f}")
    print(f"European Put Price: ${model.put_price():.2f}")