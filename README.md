# BaseCalc (Multi-Number GUI)

An interactive, graphical desktop calculator written in Python using Tkinter. It supports left-to-right reduction operations across sequences of multiple numbers simultaneously and includes built-in history tracking.

## Features

* **Graphical User Interface:** Built with Tkinter featuring a dark-themed, responsive layout.
* **Multi-Number Processing:** Computes mathematical operations across sequences of numbers (e.g., inputting `10, 20.5 5` to process all three at once).
* **Sequential Reduction:** Processes numerical strings from left to right using sequential reduction rules.
* **Input Flexibility:** Parses strings separated by commas, spaces, or a combination of both.
* **Live Calculation History:** * Tracks up to 50 past sessions inside an active scrollable list.
    * Supports session recovery: Double-clicking a history log automatically reloads its numbers and operation mode into the editor.
    * Export functionality to save logs into timestamped text files.
* **Error Prevention:** Displays precise error dialogs for empty inputs, insufficient numbers (minimum of 2 required), syntax issues, and runtime boundaries like dividing or factoring modulus by zero.
* **Supported Operations:**
    * Addition (`+`)
    * Subtraction (`-`)
    * Multiplication (`*`)
    * Division (`/`)
    * Exponentiation (`**`)
    * Modulus (`%`)
