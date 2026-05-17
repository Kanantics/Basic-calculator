**# BaseCalc (Multi-Number)**

A command-line interface (CLI) calculator written in Python that supports performing operations on multiple numbers at once, processing data from left to right.

**!!! Features !!!**

1) **Multi-Number Processing:** Handles operations across long sequences of numbers (e.g., adding or multiplying `2, 3, 4` in a single run) rather than just pairs.
2) **Left-to-Right Reduction:** Computes results sequentially from left to right using a custom reduction mechanism.
3) **Flexible Input Parsing:** Accepts numbers separated by either spaces, commas, or a combination of both.
4) **Robust Math & Input Validation**: Built-in error handling for invalid characters, empty inputs, insufficient operands, and division/modulus by zero.
5) **Clean Output Formatting:** Automatically displays results as integers if they are whole numbers, avoiding trailing decimals (e.g., showing `5` instead of `5.0`).
6) **Supported Operations:**
    a.   Addition (`+`)
    b.   Subtraction (`-`)
    c.   Multiplication (`*`)
    d.   Division (`/`)
    e.   Exponentiation (`**`)
    f.   Modulus (`%`)
