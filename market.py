# -*- coding: utf-8 -*-
"""
/!\ Convergence issue when finding best-responses for bounded random variables (e.g. uniform)
    [*] Choose starting point (first guess) wisely
        - So far 0.001 works for the uniform([0,1]), but may be inappropriate another one
    [*] No issue for unbounded distributions
"""

from . import Firm, FirmWithoutOutsideOption
from scipy.stats import uniform
    

TOLERANCE = 0.001
MAX_ITER = 1000
    
    
class Market:
    
    def __init__(self, 
                 products_per_firms=[2,2], 
                 marginal_costs=[0,0], 
                 outside_option=True,
                 distributions=[uniform(),uniform()],
                 tolerance=TOLERANCE,
                 max_iter=MAX_ITER,
                 starting_price=0.2
                 ):
        
        # Check right input
        if len(products_per_firms) != len(marginal_costs):
            msg = 'products_per_firms and marginal_cost: different lengths.'
            raise ValueError(msg)
            
        if len(products_per_firms) < 2:
            # Is it so much of an issue? Yes, when you consider you have to deal with lists!
            msg = 'There are less than two firms.'
            raise ValueError(msg)
        
        # Initialize variables
        self.number_firms = len(products_per_firms)
        self.products_per_firms = products_per_firms
        self.marginal_costs = marginal_costs
        self.outside_option = outside_option
        self.distributions = distributions
        if outside_option == True:
            self.firms = [Firm(products_per_firms[i], 
                           marginal_costs[i], 
                           distributions[i]) 
                      for i in range(self.number_firms)]
        else:
            self.firms = [FirmWithoutOutsideOption(products_per_firms[i], 
                                                   marginal_costs[i], 
                                                   distributions[i]) 
                                              for i in range(self.number_firms)]
        
        # Convergence parameters
        self.tolerance = tolerance
        self.max_iter = max_iter
        self.starting_price = starting_price
        
    
    def equilibrium_prices(self):
        """
        Finds the equilibrium prices through iteration of firms' best responses.
        """
        count = 0
        error = 100000
        prices = [self.starting_price] * len(self.firms)
        while error > self.tolerance and count < self.max_iter:
            new_prices = []
            for n in range(len(self.firms)):
                competitors = self.firms[:n] + self.firms[n+1:]
                competitors_prices = prices[:n] + prices[n+1:]
                new_prices += [self.firms[n].best_response(competitors, competitors_prices)]
            error = max([abs(prices[n] - new_prices[n]) for n in range(len(self.firms))])[0]
            print('Finding prices ... {}'.format(new_prices))
            print('Error: {}'.format(error))
            count += 1
            prices = new_prices
        return new_prices
    
    
    def equilibrium_demands(self):
        demands = []
        prices = self.equilibrium_prices()
        for n in range(len(self.firms)):
            price = prices[n]
            competitors = self.firms[:n] + self.firms[n+1:]
            competitors_prices = prices[:n] + prices[n+1:]
            demands += [self.firms[n].demand(price, competitors, competitors_prices)]     
        return demands
    
    
    def equilibrium_profits(self):
        prices = self.equilibrium_prices()
        marginal_costs = self.marginal_costs
        demands = self.equilibrium_demands()
            
        return [(prices[n] - marginal_costs[n]) * demands[n] for n in range(len(self.firms))]
    
    

class MarketWithoutOutsideOption(Market):
    
        def equilibrium_demands(self):
            demands = []
            prices = self.equilibrium_prices()
            for n in range(len(self.firms)):
                price = prices[n]
                competitors = self.firms[:n] + self.firms[n+1:]
                competitors_prices = prices[:n] + prices[n+1:]
                if self.outside_option == True:
                    demands += [self.firms[n].demand(price, competitors, competitors_prices)]
                else:
                    demands += [self.firms[n].demand_no_outside_option(price, competitors, competitors_prices)]        
            return demands
