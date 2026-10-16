
import tkinter as tk
from tkinter import ttk, messagebox


def check_safety(available, allocation, maximum):
    processes = len(allocation)
    resources = len(available)

    need = [
        [
            maximum[i][j] - allocation[i][j]
            for j in range(resources)
        ]
        for i in range(processes)
    ]

    work = available[:]
    finished = [False] * processes
    safe_sequence = []

    while len(safe_sequence) < processes:
        found = False

        for i in range(processes):
            if finished[i]:
                continue

            if all(need[i][j] <= work[j] for j in range(resources)):
                for j in range(resources):
                    work[j] += allocation[i][j]

                finished[i] = True
                safe_sequence.append(f"P{i}")
                found = True

        if not found:
            break

    return len(safe_sequence) == processes, safe_sequence, need


def run_allocation():
    try:
        available = [
            int(x.strip())
            for x in available_entry.get().split(",")
        ]

        allocation = [
            [int(x) for x in row.split(",")]
            for row in allocation_text.get("1.0", tk.END).strip().splitlines()
        ]

        maximum = [
            [int(x) for x in row.split(",")]
            for row in maximum_text.get("1.0", tk.END).strip().splitlines()
        ]

        if not available or not allocation:
            raise ValueError("Enter resources and process data.")

        if len(allocation) != len(maximum):
            raise ValueError("Allocation and maximum rows must match.")

        if any(len(row) != len(available) for row in allocation + maximum):
            raise ValueError("Each process row must match resource count.")

        if any(x < 0 for x in available):
            raise ValueError("Resource values cannot be negative.")

        if any(x < 0 for row in allocation + maximum for x in row):
            raise ValueError("Allocation values cannot be negative.")

        for i in range(len(allocation)):
            for j in range(len(available)):
                if allocation[i][j] > maximum[i][j]:
                    raise ValueError(
                        f"Allocation exceeds maximum for P{i}, resource {j}."
                    )

    except ValueError as error:
        messagebox.showerror("Input Error", str(error))
        return

    safe, sequence, need = check_safety(
        available, allocation, maximum
    )

    result_table.delete(*result_table.get_children())
    output.delete("1.0", tk.END)

    for i, row in enumerate(need):
        result_table.insert(
            "", tk.END,
            values=(f"P{i}", *allocation[i], *maximum[i], *row)
        )

    output.insert(tk.END, f"Available Resources: {available}\n\n")
    output.insert(tk.END, "Need Matrix:\n")

    for i, row in enumerate(need):
        output.insert(tk.END, f"P{i}: {row}\n")

    output.insert(tk.END, "\n")

    if safe:
        output.insert(tk.END, "SYSTEM STATUS: SAFE\n")
        output.insert(
            tk.END,
            "Safe Sequence: " + " -> ".join(sequence)
        )
    else:
        output.insert(tk.END, "SYSTEM STATUS: UNSAFE\n")
        output.insert(
            tk.END,
            "No safe sequence exists for the current state."
        )


root = tk.Tk()
root.title("Resource Allocation Simulator")
root.geometry("1000x720")
root.configure(bg="#edf2f7")

tk.Label(
    root,
    text="RESOURCE ALLOCATION SIMULATOR",
    font=("Arial", 20, "bold"),
    bg="#173b67",
    fg="white",
    pady=15
).pack(fill="x")

tk.Label(
    root,
    text="Operating Systems | Banker's Safety Algorithm",
    font=("Arial", 11),
    bg="#edf2f7"
).pack(pady=8)

input_frame = tk.LabelFrame(
    root,
    text="Resource and Process Inputs",
    font=("Arial", 11, "bold"),
    bg="#edf2f7",
    padx=12,
    pady=10
)
input_frame.pack(fill="x", padx=20, pady=5)

tk.Label(
    input_frame,
    text="Available resources (comma-separated):",
    bg="#edf2f7"
).grid(row=0, column=0, sticky="w", pady=5)

available_entry = tk.Entry(input_frame, width=35)
available_entry.grid(row=0, column=1, padx=8, pady=5)
available_entry.insert(0, "3, 3, 2")

tk.Label(
    input_frame,
    text="Allocation matrix (one process per line):",
    bg="#edf2f7"
).grid(row=1, column=0, sticky="nw", pady=5)

allocation_text = tk.Text(input_frame, width=35, height=5)
allocation_text.grid(row=1, column=1, padx=8, pady=5)
allocation_text.insert(
    "1.0",
    "0, 1, 0\n"
    "2, 0, 0\n"
    "3, 0, 2\n"
    "2, 1, 1\n"
    "0, 0, 2"
)

tk.Label(
    input_frame,
    text="Maximum demand matrix:",
    bg="#edf2f7"
).grid(row=2, column=0, sticky="nw", pady=5)

maximum_text = tk.Text(input_frame, width=35, height=5)
maximum_text.grid(row=2, column=1, padx=8, pady=5)
maximum_text.insert(
    "1.0",
    "7, 5, 3\n"
    "3, 2, 2\n"
    "9, 0, 2\n"
    "2, 2, 2\n"
    "4, 3, 3"
)

tk.Button(
    root,
    text="Check Resource Allocation",
    command=run_allocation,
    bg="#173b67",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
).pack(pady=10)

table_frame = tk.LabelFrame(
    root,
    text="Allocation, Maximum and Need Matrix",
    font=("Arial", 11, "bold"),
    bg="#edf2f7",
    padx=8,
    pady=8
)
table_frame.pack(fill="x", padx=20, pady=5)

columns = (
    "Process",
    "A1", "A2", "A3",
    "M1", "M2", "M3",
    "N1", "N2", "N3"
)

result_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=5
)

for column in columns:
    result_table.heading(column, text=column)
    result_table.column(column, width=75, anchor="center")

result_table.pack(fill="x")

output = tk.Text(
    root,
    height=8,
    font=("Consolas", 11),
    wrap="word"
)
output.pack(fill="both", expand=True, padx=20, pady=10)

root.mainloop()
