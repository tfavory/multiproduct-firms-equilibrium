from scipy.stats import uniform
from scipy import integrate
from scipy.optimize import minimize


STARTING_PRICE = 0.001


class Firm:
    
    def __init__(self, 
                 number_products=2, 
                 marginal_cost=0, 
                 distribution=uniform(),
                 starting_price=STARTING_PRICE                 
                 ):
        
        self.number_products = number_products
        self.marginal_cost = marginal_cost
        self.distribution = distribution
        self.starting_price=starting_price
        
    
    def __repr__(self):
        return "Firm: nb of products = {nb_products}, marginal cost = {mc}, distribution = {dist}".format(
                                                                nb_products=self.number_products,
                                                                mc=self.marginal_cost,
                                                                dist=self.distribution)
    
    
    def __str__(self):
        return "Firm with {nb_products} products and a {dist} distribution.".format(
                                                                nb_products=self.number_products,
                                                                dist=self.distribution)
        
    
    def pdf(self, x):
        """
        Density of distribution for the best alternative a consumer finds in the firm.
        """
        number_products = self.number_products
        distribution = self.distribution
        return number_products * distribution.pdf(x) * distribution.cdf(x) ** (number_products - 1)
        
    
    def cdf(self, x):
        """
        cumulative distribution of the best alternative a consumer finds in the firm.
        """
        number_products = self.number_products
        distribution = self.distribution
        return distribution.cdf(x) ** number_products
    
    
    def product_cdf_competitors(self, x, price, competitors, competitors_prices):
        """
        Technical function.
        Appears in the integrand of the firm's demand
        That is the term \Pi_{m \neq n} F^k(p_m - p_n + x)
        in
        \int f_{k}(x) \Pi_{m \neq n} F^k(p_m - p_n + x) dx
        """
        if len(competitors) == 1:
            # Stop the recursion if there is one competitor left.
            return competitors[0].cdf(competitors_prices[0] - price + x)
        
        # Recursive function if there are more than one competitor.
        cdf_first_competitor = competitors[0].cdf(competitors_prices[0] - price + x)
        return cdf_first_competitor * self.product_cdf_competitors(x, price, competitors[1:], 
                                                                           competitors_prices[1:])
        
    
    def demand_integrand(self, x, price, competitors, competitors_prices):
        """
        Technical function.
        It is the integrand of the firm's demand
        \int f_{k}(x) \Pi_{m \neq n} F^k(p_m - p_n + x) dx
        """
        return self.pdf(x) * self.product_cdf_competitors(x, price, competitors, competitors_prices)
    
    
    def demand(self, price, competitors, competitors_prices):
        """
        The firm's demand for given prices
        \int f_{k}(x) \Pi_{m \neq n} F^k(p_m - p_n + x) dx
        There is an outside option. (integration starts at p)
        """
        return integrate.quad(
                            lambda x: self.demand_integrand(x, price, competitors, competitors_prices), 
                            max(price, self.distribution.a), 
                            self.distribution.b)[0]

    
    def profit(self, price, competitors, competitors_prices):
        """
        The firm's profit for given prices
        """
        return (price - self.marginal_cost) * self.demand(price, competitors, competitors_prices)
    
        
    def best_response(self, competitors, competitors_prices):
        """
        Finds the unique best response that maximizes profit given competitors' prices
        """
        try:
            return minimize(lambda x: - self.profit(x, competitors, competitors_prices), 
                                                                        [self.starting_price]).x
                                
        except ZeroDivisionError:
            print('Failure to convergence to best response. Consider changing Firm\'s starting_point.')
            

class FirmWithoutOutsideOption(Firm):
    
    def demand(self, price, competitors, competitors_prices):
        """
        The firm's demand for given prices
        \int f_{k}(x) \Pi_{m \neq n} F^k(p_m - p_n + x) dx
        There is an outside option. (integration starts at p)
        """
        return integrate.quad(
                        lambda x: self.demand_integrand(x, price, competitors, competitors_prices), 
                        self.distribution.a, 
                        self.distribution.b)[0]