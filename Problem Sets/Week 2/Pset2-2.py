MonthlyPayment=10
MonthlyInterestRate= (annualInterestRate) / 12
p=True
while p==True:
    i=1
    PreviousBalance=balance
    while i<=12:
        RBalance = (PreviousBalance - MonthlyPayment) * (1 + MonthlyInterestRate)
        PreviousBalance = RBalance
        i=i+1
    if PreviousBalance<=0:
        print 'Lowest Payment: ' + str(MonthlyPayment)
        p=False
    MonthlyPayment=MonthlyPayment+10
