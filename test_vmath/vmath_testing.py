from datetime import datetime, timezone
import vestingmath

df = vestingmath.default_period
print(vestingmath.ceildiv(2,1))

amount = 10
total = 100
l = vestingmath.linearFrom(amount, total)
print(l/df)

cliffDate = datetime(2021, 9, 20, tzinfo=timezone.utc)
cliff = datetime.timestamp(cliffDate)
# print((ut2-ut)/df)

cliff = int(cliff)
print("cliff ",cliff)

end = vestingmath.getEndTime(cliff, amount, total)
print(end)

enddt = datetime.fromtimestamp(int(end))
es = enddt.strftime('%Y-%m-%d %H:%M:%S')
print(">> ",es)

amount = 10
total = 100
periods = int(total/amount)

d1 = datetime(2022, 1, 27, tzinfo=timezone.utc)
now = datetime.timestamp(d1)
print(now)

end = vestingmath.getEndTime(cliff, amount, total) 
x = vestingmath.getVestedAmountPeriod(now, cliff, end, amount, total)
print(x)

from datetime import timedelta

start  = datetime(2021, 9, 1)
for z in range(11):
    d = timedelta(days=z*30)
    bt = start + d
    x = bt.timestamp()
    # print(bt)
    v = vestingmath.getVestedAmountPeriod(x, cliff, end, amount, total)
    print(bt,v)
