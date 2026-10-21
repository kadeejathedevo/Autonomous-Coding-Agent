def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if not isinstance(n, int):
        raise TypeError("Input must be an integer.")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def main():
    test_values = [0, 1, 5, 7, 10]
    print("Factorial examples:")
    for val in test_values:
        print(f"{val}! = {factorial(val)}")

    print("\nInteractive calculation:")
    try:
        user_input = input("Enter a non-negative integer (or press Enter to exit): ").strip()
        if user_input:
            num = int(user_input)
            print(f"{num}! = {factorial(num)}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()