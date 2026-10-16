# Process Synchronization Module

## 1. Introduction
The Process Synchronization Module is a Python-based GUI project that demonstrates how multiple processes or threads share resources safely.

It helps prevent race conditions and shows how synchronization works in an Operating System.

## 2. Features
- Simple Graphical User Interface (GUI)
- Demonstrates process synchronization
- Shows thread execution
- Uses Lock to protect shared resources
- Prevents race conditions
- Displays execution results

## 3. Technologies Used
- Python 3
- Tkinter (GUI)
- Threading module

## 4. Requirements
- Python 3 installed on your computer
- Visual Studio Code (VS Code)
- No additional libraries are required if Python includes Tkinter.

## 5. How to Run the Project

**Step 1:** Open the project folder in VS Code.

**Step 2:** Open the terminal from the Terminal menu.

**Step 3:** Run the following command:

```bash
python process_synchronization.py
```

If your system uses the Python launcher, try:

```bash
py process_synchronization.py
```

**Step 4:** The GUI window will open.

**Step 5:** Use the available controls to start the simulation and observe the results.

## 6. Working Principle
Process synchronization controls access to shared resources when multiple threads execute at the same time.

A Lock allows only one thread at a time to access a protected section of code. This helps prevent incorrect results caused by simultaneous access.

## 7. Applications
- Operating Systems
- Multithreading
- Shared memory management
- Resource sharing
- Race condition prevention

## 8. Conclusion
This project provides a simple demonstration of process synchronization in an Operating System. It helps students understand how locks and threads work together to manage shared resources safely.
