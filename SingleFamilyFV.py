import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

"""
Considers the price of houses and takes into account of mortgage, carry costs and costs.
"""
def mortgage_amortization(principal, annual_rate, total_years):

    monthly_rate = annual_rate / 100 / 12
    num_payments = total_years * 12
    monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** -num_payments)

    balance = principal
    balances = [balance]

    for month in range(1, num_payments + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment

        if month % 12 == 0:  # Track yearly balances
            balances.append(balance)

    return balances, monthly_payment


def future_house_value_with_amortization(present_value, annual_appreciation, years, mortgage_principal,
                                         total_amortization_years, annual_tax=0, mortgage_interest_rate=0,
                                         repair_percentage=0):

    mortgage_balances, monthly_payment = mortgage_amortization(mortgage_principal, mortgage_interest_rate,
                                                               total_amortization_years)

    fv = present_value
    rate_decimal = annual_appreciation / 100
    yearly_values = [fv]

    for year in range(1, years + 1):
        fv = fv * (1 + rate_decimal)
        fv -= annual_tax
        fv -= fv * (repair_percentage / 100)
        yearly_values.append(fv)

    return yearly_values, mortgage_balances, monthly_payment


def calculate_cagr(start_value, end_value, years):

    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr * 100


# Example parameters
current_value = 350000
appreciation = 1.5
years = 10
total_amortization_years = 30
annual_tax = 350
mortgage_principal = 250000
mortgage_interest_rate = 4.0
repair_percentage = 2.0

yearly_fv, mortgage_balances, monthly_payment = future_house_value_with_amortization(
    current_value, appreciation, years, mortgage_principal, total_amortization_years, annual_tax,
    mortgage_interest_rate, repair_percentage
)


print("Year | House Value | Mortgage Balance")
print("-------------------------------------")
for i in range(len(yearly_fv)):
    print(f"{i:2d}   | ${yearly_fv[i]:,.2f}     | ${mortgage_balances[i]:,.2f}")

start_value = current_value
end_value = yearly_fv[-1]  # Final house value after 'years' periods

average_yearly_return = calculate_cagr(start_value, end_value, years)

print(f"\nThe average yearly return (CAGR) is: {average_yearly_return:.2f}%")

plt.figure(figsize=(10, 6))
plt.plot(range(0, years + 1), yearly_fv, marker='o', linestyle='-', label="House Value", color='green')
plt.plot(range(0, years + 1), mortgage_balances[:years + 1], marker='x', linestyle='--', label="Mortgage Balance",
         color='red')

plt.title("House Value vs Mortgage Balance Over Time")
plt.xlabel("Year")
plt.ylabel("Amount ($)")

plt.yscale('linear')

formatter = FuncFormatter(lambda x, _: f"${x:,.0f}")
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)

plt.legend()

plt.show()