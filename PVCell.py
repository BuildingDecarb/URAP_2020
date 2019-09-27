import pandas as pd
import numpy as np
from numpy import *

class PVCell:
    def __init__(self, ef, C, s1, s2, vintage, lt, IC, OM):
        self.name = "PVCell"
        self.ef = ef
        self.C = C
        self.s1 = s1
        self.s2 = s2
        self.vintage = vintage
        self.lt = lt
        self.IC = IC 
        self.OM = OM 
