i=1
MonthlyInterestRate= (annualInterestRate) / 12
PreviousBalance=balance
Total = 0
while i<=12:
    MinimumMonthlyPayment = (monthlyPaymentRate) * (PreviousBalance)
    RBalance = (PreviousBalance - MinimumMonthlyPayment) * (1 + MonthlyInterestRate)
    print 'Month: '+ str(i)
    print 'Minimum monthly payment: ' + str(round(MinimumMonthlyPayment,2))
    print 'Remaining balance: ' + str(round(RBalance,2))
    PreviousBalance = RBalance
    i=i+1
    Total = Total + MinimumMonthlyPayment
print 'Total paid: ' + str(round(Total,2))
print 'Remaining balance: ' + str(round(PreviousBalance,2))
