import unittest

# Ensure this matches your exact folder structure
from src.black_scholes import BlackScholesModel 

class TestOptionPricing(unittest.TestCase):

    def setUp(self):
        """Initialize standard parameters used across multiple tests."""
        self.S = 100.0  
        self.K = 100.0  
        self.T = 1.0    
        self.r = 0.05   
        self.sigma = 0.20 

    def test_black_scholes_call_price(self):
        """Test if the closed-form Black-Scholes call math is accurate."""
        bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma)
        
        # Calling your specific method
        call = bs_model.call_price() 
        
        # 10.4506 is the mathematically guaranteed answer for these inputs
        self.assertAlmostEqual(call, 10.4506, places=4, msg="BS Call Price calculation failed")

    def test_black_scholes_put_price(self):
        """Test if the closed-form Black-Scholes put math is accurate."""
        bs_model = BlackScholesModel(self.S, self.K, self.T, self.r, self.sigma)
        
        # Calling your specific method
        put = bs_model.put_price() 
        
        # 5.5747 is the mathematically guaranteed put answer for these inputs
        self.assertAlmostEqual(put, 5.5735, places=4, msg="BS Put Price calculation failed")

if __name__ == '__main__':
    unittest.main()