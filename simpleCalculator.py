from __future__ import annotations
from typing import Callable, Iterable, List

Number = float

def parse_number_list(raw: str) -> List[Number]:
    raw = raw.strip()
    if not raw:
        return []
    tokens = []
    for part in raw.replace(",", " ").split():
        tokens.append(part)
    numbers: List[Number] = []
    for t in tokens:
        try:
            numbers.append(float(t))
        except ValueError as e:
            raise ValueError(f"Invalid number: '{t}'") from e
    return numbers

def require_min_numbers(nums: List[Number], min_count: int = 2) -> None:
    if len(nums) < min_count:
        raise ValueError(f"Please enter at least {min_count} number(s).")

def safe_div(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by 0")
    return a / b

def safe_mod(a: Number, b: Number) -> Number:
    if b == 0:
        raise ZeroDivisionError("Cannot mod by 0")
    return a % b

def reduce_left(nums: Iterable[Number], op: Callable[[Number, Number], Number]) -> Number:
    it = iter(nums)
    try:
        acc = next(it)
    except StopIteration:
        raise ValueError("No numbers provided")
    for x in it:
        acc = op(acc, x)
    return acc

def apply_operation(nums: List[Number], operation_key: str) -> Number:
    if operation_key == "+":
        return reduce_left(nums, lambda a, b: a + b)
    if operation_key == "-":
        return reduce_left(nums, lambda a, b: a - b)
    if operation_key == "*":
        return reduce_left(nums, lambda a, b: a * b)
    if operation_key == "/":
        return reduce_left(nums, safe_div)
    if operation_key == "**":
        return reduce_left(nums, lambda a, b: a**b)
    if operation_key == "%":
        return reduce_left(nums, safe_mod)
    raise ValueError("Unknown operation")

def print_menu() -> None:
    print("\n=== CALCULATOR MENU ===")
    print("Choose an operation:")
    print("  1) Addition        (+)")
    print("  2) Subtraction     (-)")
    print("  3) Multiplication  (*)")
    print("  4) Division        (/)")
    print("  5) Exponentiation  (**)")
    print("  6) Modulus         (%)")
    print("  X) Exit")

def operation_from_choice(choice: str) -> str:
    choice = choice.strip().upper()
    mapping = {
        "1": "+",
        "2": "-",
        "3": "*",
        "4": "/",
        "5": "**",
        "6": "%",
    }
    if choice in mapping:
        return mapping[choice]
    raise ValueError("Invalid operation choice")

def format_number(n: Number) -> str:
    if abs(n - round(n)) < 1e-12:
        return str(int(round(n)))
    return str(n)

def main() -> None:
    print("Welcome to BaseCalc (multi-number)!")
    while True:
        print_menu()
        choice = input("Enter choice (1-6 or X): ").strip()
        if choice.upper() == "X":
            print("See you later!")
            return
        try:
            operation_key = operation_from_choice(choice)
        except ValueError:
            print("Invalid operation. Please try again.")
            continue
        raw_nums = input(
            "Enter numbers separated by commas or spaces (e.g., 2, 3, 4): "
        )
        try:
            nums = parse_number_list(raw_nums)
            require_min_numbers(nums, 2)
            result = apply_operation(nums, operation_key)
            print(f"Result: {format_number(result)}")
        except ValueError as e:
            print(f"Input error: {e}")
        except ZeroDivisionError as e:
            print(f"Math error: {e}")

if __name__ == "__main__":
    main()