# -*- coding: utf-8 -*-

from . import Market
from scipy.stats import uniform, norm, expon, gumbel_r


market = Market(products_per_firms=[1,1,1],
                marginal_costs=[0,0,0],
                distributions=[uniform(), uniform(), uniform()],
                outside_option=False)


print(market.equilibrium_prices())