balance=320000
annualInterestRate=0.2
low=balance/12.0
high= ((balance) * ((1 +(annualInterestRate/12))**12)) / 12
test=True
while test==True:
    ub=balance
    p0=(low+high)/2
    for month in range(1,13):
        ub=(ub-p0)*(1+(annualInterestRate/12))
    if ub>0:
        low=p0
    else:
        high=p0
    if round(ub)==0:
        test=False
print('Lowest payment: '+str(round(p0,2)))
