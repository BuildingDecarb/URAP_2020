import Inputs


# returns tons of GHG
class Refrigerant:
    def __init__(self, gwp=1, initTotal=0, initleakage=0, annualLeakage=0, eolRate=0):
        self.gwp = gwp
        self.initTotal = initTotal
        self.initleakage = initleakage
        self.annualLeakage = annualLeakage
        self.eolRate = eolRate  # EOL absorption rate

    def RefLeakage(self, OrigYear, EndLife):

        AnnualRefLeak = {}
        LeftOverRef = {}
        AnnualLeakCO2Eq = {}
        YrlyLeak = self.initTotal * self.annualLeakage

        RefillPoint = 0.1  # when the refrigerant falls to this % of initial quant, refill is assumed
        AnnualRefLeak[OrigYear] = self.initTotal * self.initleakage + YrlyLeak
        LeftOverRef[OrigYear] = self.initTotal - AnnualRefLeak[OrigYear]

        for yr in range(OrigYear + 1, EndLife + 1):

            if (LeftOverRef[yr - 1] > YrlyLeak):
                AnnualRefLeak[yr] = YrlyLeak
                LeftOverRef[yr] = LeftOverRef[yr - 1] - AnnualRefLeak[yr]
                if (yr == EndLife):
                    AnnualRefLeak[yr] = AnnualRefLeak[yr] + max(0, (1 - self.eolRate) * LeftOverRef[yr])
                    LeftOverRef[yr] = LeftOverRef[yr - 1] - AnnualRefLeak[yr]
            elif (yr < EndLife):
                #  print "Mid", yr-1, LeftOverRef[yr-1]         #and YrlyLeak*(EndLife-yr) < self.initTotal):
                LeftOverRef[yr - 1] = (self.initTotal - LeftOverRef[yr - 1])  # (end of yr-1, topping up refrigerant )
                AnnualRefLeak[yr] = YrlyLeak
                LeftOverRef[yr] = LeftOverRef[yr - 1] - AnnualRefLeak[yr]
            #    print "End", yr, LeftOverRef[yr-1], LeftOverRef[yr]
            else:
                AnnualRefLeak[yr] = max(0, LeftOverRef[yr] * (1 - self.eolRate))
            # LeftOverRef[yr] = LeftOverRef[yr-1] - AnnualRefLeak[yr-1]
        # print "LefOverRef", yr, LeftOverRef[yr] , "Annual Leak", AnnualRefLeak[yr]
        for k in range(OrigYear, EndLife + 1):
            AnnualLeakCO2Eq[k] = AnnualRefLeak[k] * self.gwp / 1000  # in tons of CO2 equiv
        #     print "Annualleak", k, AnnualLeakCO2Eq[k]
        return AnnualLeakCO2Eq

# RefType1 = Refrigerant(2000, 1, .01, .1, .7)

# print RefType1.RefLeakage(2016,2035)
