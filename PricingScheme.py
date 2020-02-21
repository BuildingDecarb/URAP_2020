import numpy as np
import pandas as pd
from datetime import datetime, date
from calendar import monthrange
from Calculator import date_to_range, daterange

# pricing scheme has a flat rate,
# tiers is a list of two-tuples: (monthly threshold: price above that threshold)
# tou is a list of 3-tuples: (begin_time, end_time, rate)
class PricingScheme:
    def __init__(self, scheme, flat_rate=None, tiers=None, tou=None):
        self.scheme = scheme
        self.flat_rate = flat_rate
        self.tiers = tiers
        self.tou = tou

    def cost(self, data, climate_zone, begin_date, end_date):
        total = 0
        if self.scheme == 'flat_rate':
            for d in daterange(begin_date, end_date):
                for idx in date_to_range(d):
                    total += self.flat_rate * data.loc[idx].iloc[climate_zone]
        elif self.scheme == 'tiered':
            pass
        elif self.scheme == 'tou':
            pass
