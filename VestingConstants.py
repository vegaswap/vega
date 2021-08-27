# the s for vesting schedule and tokeneconomics
# Vestings
days = 86400
DEFAULT_PERIOD = 30 * days

K = 10**3
M = 10**6

#funding prices
#multiple is 1/price
seedMultiple = 125 #0.008$
privateMultiple = 100 #0.01$
publicMultiple = 84 #0.0119$

#1000M supply allocate to 11 buckets
#total amounts, no decimals
seedAmount = 12 * M + 500 * K
privateAmount = 65 * M
publicAmount = 16 * M + 800 * K
publicAmountB = 4 * M + 200 * K
liqAmount = 150 * M
lprewardsAmount = 200 * M
lpgrantsAmount = 50 * M
ecoAmount = 100 * M
trademiningAmount = 200 * M
teamAmount = 150 * M
advisoryAmount = 50 * M
#treasury is the rest
treasuryAmount = 1 * M + 500 * K

#cliffs
seedCliff = 0 * days #33%
privateCliff = 0 * days
publicCliff = 0 * days
liqCliff = 30 * days
lpwRewardsCliff = 30 * days
lpgrantsCliff = 60 * days
ecoCliff = 120 * days
trademiningCliff = 10 * days
teamCliff = 180 * days
advisoryCliff = 60 * days
treasuryCliff = 30 * days

#durations
seedPeriods = 6
privatePeriods = 6
publicPeriods = 3
liqPeriods = 2
lprewardsPeriods = 3
lpgrantsPeriods = 3
ecoPeriods = 6
trademiningPeriods = 3
teamPeriods = 12
advisorsPeriods = 12
treasuryPeriods = 1
