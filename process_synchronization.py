
import tkinter as tk
from tkinter import ttk, messagebox


# FCFS Algorithm
def fcfs(requests, head):
    order = [head] + requests[:]
    movement = sum(
        abs(order[i] - order[i - 1])
        for i in range(1, len(order))
    )
    return order, movement


# SSTF Algorithm
def sstf(requests, head):
    pending = requests[:]
    order = [head]
    current = head

    while pending:
        nearest = min(
            pending,
            key=lambda x: abs(x - current)
        )
        order.append(nearest)
        pending.remove(nearest)
        current = nearest

    movement = sum(
        abs(order[i] - order[i - 1])
        for i in range(1, len(order))
    )
    return order, movement


# SCAN Algorithm
def scan(requests, head, maximum, direction):
    left = sorted([x for x in requests if x < head])
    right = sorted([x for x in requests if x >= head])

    order = [head]

    if direction == "Right":
        order += right

        if order[-1] != maximum:
            order.append(maximum)

        order += left[::-1]

    else:
        order += left[::-1]

        if order[-1] != 0:
            order.append(0)

        order += right

    movement = sum(
        abs(order[i] - order[i - 1])
        for i in range(1, len(order))
    )
    return order, movement


# C-SCAN Algorithm
def cscan(requests, head, maximum, direction):
    left = sorted([x for x in requests if x < head])
    right = sorted([x for x in requests if x >= head])

    order = [head]

    if direction == "Right":
        order += right

        if order[-1] != maximum:
            order.append(maximum)

        if left:
            order.append(0)
            order += left

    else:
        order += left[::-1]

        if order[-1] != 0:
            order.append(0)

        if right:
            order.append(maximum)
            order += right[::-1]

    movement = sum(
        abs(order[i] - order[i - 1])
        for i in range(1, len(order))
    )
    return order, movement


# GUI Application
def run_scheduling():
    try:
        requests = [
            int(x.strip())
            for x in request_entry.get().split(",")
            if x.strip()
        ]

        head = int(head_entry.get())
        maximum = int(max_entry.get())
        direction = direction_box.get()

        if not requests:
            raise ValueError("Enter at least one request.")

        if maximum < 1:
            raise ValueError("Maximum cylinder must be positive.")

        if not 0 <= head <= maximum:
            raise ValueError("Invalid initial head position.")

        if any(x < 0 or x > maximum for x in requests):
            raise ValueError(
                "Requests must be between 0 and maximum cylinder."
            )

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))
        return

    algorithms = [
        ("FCFS", lambda: fcfs(requests, head)),
        ("SSTF", lambda: sstf(requests, head)),
        ("SCAN", lambda: scan(
            requests, head, maximum, direction
        )),
        ("C-SCAN", lambda: cscan(
            requests, head, maximum, direction
        ))
    ]

    for item in result_table.get_children():
        result_table.delete(item)

    details.delete("1.0", tk.END)

    results = []

    for name, algorithm in algorithms:
        order, movement = algorithm()

        result_table.insert(
            "",
            tk.END,
            values=(
                name,
                " -> ".join(map(str, order)),
                movement
            )
        )

        details.insert(
            tk.END,
            f"{name}\n"
            f"Head Movement: {' -> '.join(map(str, order))}\n"
            f"Total Movement: {movement} cylinders\n\n"
        )

        results.append((name, movement))

    best = min(results, key=lambda x: x[1])

    details.insert(
        tk.END,
        f"Lowest head movement: {best[0]} "
        f"({best[1]} cylinders)"
    )


# Main Window
root = tk.Tk()
root.title("Disk Scheduling Simulator")
root.geometry("950x650")
root.configure(bg="#edf2f7")

title = tk.Label(
    root,
    text="DISK SCHEDULING SIMULATOR",
    font=("Arial", 20, "bold"),
    bg="#173b67",
    fg="white",
    pady=15
)
title.pack(fill="x")

subtitle = tk.Label(
    root,
    text="Operating System Project | FCFS | SSTF | SCAN | C-SCAN",
    font=("Arial", 11),
    bg="#edf2f7"
)
subtitle.pack(pady=10)

input_frame = tk.LabelFrame(
    root,
    text="Input Details",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=10,
    bg="#edf2f7"
)
input_frame.pack(fill="x", padx=20, pady=5)

tk.Label(
    input_frame,
    text="Disk Requests (comma separated):",
    bg="#edf2f7"
).grid(row=0, column=0, sticky="w", pady=6)

request_entry = tk.Entry(input_frame, width=55)
request_entry.grid(row=0, column=1, padx=10, pady=6)
request_entry.insert(
    0, "98, 183, 37, 122, 14, 124, 65, 67"
)

tk.Label(
    input_frame,
    text="Initial Head Position:",
    bg="#edf2f7"
).grid(row=1, column=0, sticky="w", pady=6)

head_entry = tk.Entry(input_frame, width=15)
head_entry.grid(row=1, column=1, sticky="w", padx=10)
head_entry.insert(0, "53")

tk.Label(
    input_frame,
    text="Maximum Cylinder:",
    bg="#edf2f7"
).grid(row=2, column=0, sticky="w", pady=6)

max_entry = tk.Entry(input_frame, width=15)
max_entry.grid(row=2, column=1, sticky="w", padx=10)
max_entry.insert(0, "199")

tk.Label(
    input_frame,
    text="Initial Direction:",
    bg="#edf2f7"
).grid(row=3, column=0, sticky="w", pady=6)

direction_box = ttk.Combobox(
    input_frame,
    values=["Right", "Left"],
    state="readonly",
    width=12
)
direction_box.grid(row=3, column=1, sticky="w", padx=10)
direction_box.set("Right")

run_button = tk.Button(
    root,
    text="Run All Algorithms",
    command=run_scheduling,
    bg="#173b67",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=7
)
run_button.pack(pady=12)

result_frame = tk.LabelFrame(
    root,
    text="Results",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=10,
    bg="#edf2f7"
)
result_frame.pack(fill="both", expand=True, padx=20, pady=5)

result_table = ttk.Treeview(
    result_frame,
    columns=("Algorithm", "Order", "Movement"),
    show="headings",
    height=5
)

result_table.heading("Algorithm", text="Algorithm")
result_table.heading("Order", text="Head Movement Order")
result_table.heading("Movement", text="Total Movement")

result_table.column("Algorithm", width=100, anchor="center")
result_table.column("Order", width=600)
result_table.column("Movement", width=150, anchor="center")

result_table.pack(fill="x", pady=5)

details = tk.Text(
    result_frame,
    height=8,
    font=("Consolas", 10),
    wrap="word"
)
details.pack(fill="both", expand=True, pady=5)

root.mainloop()
