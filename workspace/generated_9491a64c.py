def fibonacci_sequence(n):
    """Generate the first n Fibonacci numbers."""
    if n <= 0:
        return []
    sequence = [0]
    if n == 1:
        return sequence
    sequence.append(1)
    for _ in range(2, n):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence


def fibonacci_number(n):
    """Return the n-th Fibonacci number (0-indexed)."""
    if n < 0:
        raise ValueError("n must be a non-negative integer.")
    if n == 0:
        return 0
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def main():
    count = 15
    print(f"First {count} Fibonacci numbers:")
    fib_list = fibonacci_sequence(count)
    print(fib_list)

    print("\nIndividual lookups:")
    for i in [0, 1, 5, 10, 20]:
        print(f"Fibonacci({i}) = {fibonacci_number(i)}")


if __name__ == "__main__":
    main()