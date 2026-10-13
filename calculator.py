
import tkinter as tk
import ast
import operator

# Create the main window
root = tk.Tk()
root.title("Python Calculator")
root.geometry("360x520")
root.resizable(False, False)
root.configure(bg="#1E1E2F")

expression = ""

# Supported arithmetic operations
OPERATIONS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv
}


# Safely calculate the expression
def calculate(node):
    if isinstance(node, ast.Expression):
        return calculate(node.body)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise ValueError("Invalid number")

    if isinstance(node, ast.BinOp):
        operation = type(node.op)

        if operation not in OPERATIONS:
            raise ValueError("Invalid operator")

        left = calculate(node.left)
        right = calculate(node.right)

        return OPERATIONS[operation](left, right)

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -calculate(node.operand)

        if isinstance(node.op, ast.UAdd):
            return calculate(node.operand)

    raise ValueError("Invalid expression")


# Display area
display = tk.Entry(
    root,
    font=("Arial", 27, "bold"),
    bg="#292940",
    fg="white",
    insertbackground="white",
    justify="right",
    bd=0
)

display.pack(
    fill="x",
    padx=16,
    pady=(25, 20),
    ipady=16
)


# Update the display
def show_display(text):
    display.delete(0, tk.END)
    display.insert(0, text)


# Handle button clicks
def button_click(value):
    global expression

    if value == "C":
        expression = ""
        show_display("")

    elif value == "⌫":
        expression = expression[:-1]
        show_display(expression)

    elif value == "=":
        if not expression:
            return

        try:
            tree = ast.parse(expression, mode="eval")
            result = calculate(tree)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            expression = str(result)
            show_display(expression)

        except ZeroDivisionError:
            expression = ""
            show_display("Cannot divide by zero")

        except (
            SyntaxError, ValueError, TypeError,
            OverflowError, RecursionError
        ):
            expression = ""
            show_display("Invalid calculation")

    else:
        expression += value
        show_display(expression)


# Keyboard support
def handle_key(event):
    key = event.keysym
    char = event.char

    if key in ("Return", "KP_Enter", "equal"):
        button_click("=")
        return "break"

    if key == "BackSpace":
        button_click("⌫")
        return "break"

    if key == "Escape":
        button_click("C")
        return "break"

    if char and char in "0123456789.+-*/":
        button_click(char)
        return "break"

    if char in ("x", "X"):
        button_click("*")
        return "break"


root.bind_all("<Key>", handle_key)


# Calculator buttons
button_rows = [
    [("C", "C"), ("⌫", "⌫"), ("/", "/"), ("×", "*")],
    [("7", "7"), ("8", "8"), ("9", "9"), ("−", "-")],
    [("4", "4"), ("5", "5"), ("6", "6"), ("+", "+")],
    [("1", "1"), ("2", "2"), ("3", "3"), ("=", "=")],
    [("0", "0"), (".", ".")]
]

button_frame = tk.Frame(root, bg="#1E1E2F")
button_frame.pack(
    expand=True,
    fill="both",
    padx=12,
    pady=5
)

# Create buttons automatically
for row_index, row in enumerate(button_rows):

    for col_index, (label, value) in enumerate(row):

        if value == "=":
            bg = "#6C63FF"
        elif value in ("C", "⌫"):
            bg = "#B33A50"
        elif value in ("+", "-", "*", "/"):
            bg = "#41415D"
        else:
            bg = "#303047"

        button = tk.Button(
            button_frame,
            text=label,
            font=("Arial", 18, "bold"),
            bg=bg,
            fg="white",
            activebackground="#7770FF",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            command=lambda v=value: button_click(v)
        )

        # Make zero wider
        if value == "0":
            button.grid(
                row=row_index,
                column=col_index,
                columnspan=2,
                sticky="nsew",
                padx=5,
                pady=5
            )

        # Make equals taller
        elif value == "=":
            button.grid(
                row=3,
                column=3,
                rowspan=2,
                sticky="nsew",
                padx=5,
                pady=5
            )

        # Place other buttons
        else:
            if value == ".":
                button.grid(
                    row=row_index,
                    column=2,
                    columnspan=2,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )
            elif not (
                row_index == 3 and col_index == 3
            ):
                button.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=5,
                    pady=5
                )


# Equal spacing for rows and columns
for i in range(4):
    button_frame.columnconfigure(i, weight=1)

for i in range(5):
    button_frame.rowconfigure(i, weight=1)

# Start the application
root.mainloop()