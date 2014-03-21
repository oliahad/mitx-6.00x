lb=balance / 12
MonthlyPayment=lb
MonthlyInterestRate= (annualInterestRate) / 12
ub=(balance * (1 + MonthlyInterestRate)**12) / 12
while MonthlyPayment<=ub:
    i=1
    PreviousBalance=balance
    while i<=12:
        RBalance = (PreviousBalance - MonthlyPayment) * (1 + MonthlyInterestRate)
        PreviousBalance = RBalance
        i=i+1
    if PreviousBalance<=0:
        break
    else:
        MonthlyPayment=(lb+ub)/2
        ub=MonthlyPayment
while lb<=MonthlyPayment:
    i=1
    PreviousBalance=balance
    while i<=12:
        RBalance = (PreviousBalance - lb) * (1 + MonthlyInterestRate)
        PreviousBalance = RBalance
        i=i+1
    if PreviousBalance<=0:
        print 'Lowest Payment: ' + str(round(lb,2))
        break
    lb=lb+0.01
