from AJ_SummarizeDataFrames import *

#THis function creates categories

categwh = [wh_year]
catwh = grandSum(categwh)
categWH = [catwh]

categsh = [sh_year]
catsh = grandSum(categsh)
categSH = [catsh]

categ = [sh_year, wh_year] 
heating = grandSum(categ)
categheat = [heating]

categcool = [cool_year]
cooling = grandSum(categcool)
categcool = [cooling]

categ1 = [ base_year ]
baseload = grandSum(categ1)
categbase = [baseload]

allcateg = [ sh_year, wh_year,cool_year,base_year, pv_year ]
total = grandSum(allcateg)
categtotal = [total]

pv1 = [pv_year]
pvprofile = grandSum(pv1)
categpv = [pvprofile]

#netlaod = delta(catwh,pvprofile)  #hourly diff  #ERROR in defn
#netnet = grandSum(netload)
#categnet = [netnet]

max_sh = df_sh[climatezone].max()
hr_maxsh = df_sh[climatezone].idxmax()

max_wh = df_wh[climatezone].max()
hr_maxwh = df_wh[climatezone].idxmax()

max_cool = df['cooling'].max()
hr_maxcool = df['cooling'].idxmax()

max_base = df['base'].max()
hr_maxbase = df['base'].idxmax()

#max_netload = df['netprofile'].max()
#hr_maxnetload = df['netprofile'].idmax()

maxcool =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxcool)
maxwh =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxwh)
maxsh =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxsh)
maxbase =  datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxbase)
#maxnetload = datetime(2014, 1, 1, hour=0, minute=0, second=0) + timedelta(hours=hr_maxnetload)

#print "max", max_sh, hr_maxsh, max_wh, hr_maxwh, max_cool, hr_maxcool, max_base, hr_maxbase
#print "dates",  maxsh, maxwh,maxcool, maxbase

#max_agg = categtotal['total'].max()
#print "max agg", max_agg

##categories = [sh_year, wh_year, cool_year,df_year] #  [cool_year, pool_year, df_year, sh_year, wh_year]
##total_year = grandSum(categories)
##print "test"  #, total_year
##print("Annual energy use from cooling: %f kWh" % cool_year.sumYear())
###print("Annual energy use from pool pump: %f kWh" % pool_year.sumYear())
###print("Annual energy use from base load: %f kWh" % df_year.sumYear())
##print("Annual energy use from space heating: %f kWh" % sh_year.sumYear())
##print("Annual energy use from water heating: %f kWh" % wh_year.sumYear())
###print("Annual energy use from PV: %f kWh" % pv_year.sumYear())
##print("\n")
##print("Annual energy use from all sources: %f kWh" % total_year.sumYear())

