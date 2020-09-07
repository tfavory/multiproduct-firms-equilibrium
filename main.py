# -*- coding: utf-8 -*-

from . import Market
from scipy.stats import uniform, norm, expon, gumbel_r

number_firms = 3
products_per_firms = [1] * number_firms
marginal_costs = [0] * number_firms
distributions = [gumbel_r()] * number_firms

market = Market(products_per_firms=products_per_firms,
                marginal_costs=marginal_costs,
                distributions=distributions,
                outside_option=False)


print(market.equilibrium_prices())
