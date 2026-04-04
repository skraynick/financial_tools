import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def future_value(principal, annual_return_rate, years):
    return principal * (1 + annual_return_rate) ** years


initial_investment = 350000
property_annual_return = 0.040
sp500_annual_return = 0.08
years = 20

property_values = [future_value(initial_investment, property_annual_return, year) for year in range(years + 1)]
sp500_values = [future_value(initial_investment, sp500_annual_return, year) for year in range(years + 1)]

print("Year | Property Value | S&P 500 Value")
print("-------------------------------------")
for i in range(years + 1):
    print(f"{i:2d}   | ${property_values[i]:,.2f}     | ${sp500_values[i]:,.2f}")

plt.figure(figsize=(10, 6))
plt.plot(range(0, years + 1), property_values, marker='o', linestyle='-', label="Property Value", color='green')
plt.plot(range(0, years + 1), sp500_values, marker='x', linestyle='--', label="S&P 500 Value", color='blue')

plt.title("Property Value vs S&P 500 Value Over Time")
plt.xlabel("Year")
plt.ylabel("Value ($)")

formatter = FuncFormatter(lambda x, _: f"${x:,.0f}")
plt.gca().yaxis.set_major_formatter(formatter)

plt.grid(True)

# Add legend
plt.legend()

# Show the plot
plt.show()
