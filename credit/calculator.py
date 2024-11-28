import argparse

def final_amount(initial_amount, annual_interest, months):
  """Calculates the final amount after applying compound interest.

  Args:
    initial_amount: The initial amount of money.
    annual_interest: The annual interest rate (as a decimal, e.g., 0.05 for 5%).
    months: The number of months for which interest is applied.

  Returns:
    The final amount of money after applying compound interest.
  """

  # Calculate the monthly interest rate (CORRECTED)
  monthly_rate = (1 + annual_interest) ** (1/12) - 1

  # Calculate the final amount using the compound interest formula
  final_amount = initial_amount * (1 + monthly_rate) ** months

  return final_amount

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate compound interest.")
    parser.add_argument("initial_amount", type=float, help="The initial amount of money.")
    parser.add_argument("annual_interest", type=float, help="The annual interest rate (as a decimal).")
    parser.add_argument("months", type=int, help="The number of months for which interest is applied.")

    args = parser.parse_args()

    final_amount = final_amount(args.initial_amount, args.annual_interest, args.months)
    print(f"The final amount is: {final_amount:.2f}")
