
# Disk Scheduling Simulator

## 1. Project Introduction

Disk Scheduling Simulator is an Operating System project developed
using Python and Tkinter GUI.

It demonstrates how an operating system manages disk I/O requests
using different disk scheduling algorithms.

## 2. Objectives

- Understand disk scheduling in Operating Systems.
- Implement four disk scheduling algorithms.
- Calculate total disk head movement.
- Compare the performance of different algorithms.
- Display results through a graphical user interface.

## 3. Algorithms Used

### FCFS (First Come First Serve)
Processes disk requests in the same order in which they are received.

### SSTF (Shortest Seek Time First)
Selects the pending request closest to the current disk head position.

### SCAN (Elevator Algorithm)
Moves the disk head in one direction, reaches the disk boundary
when required, and then reverses direction.

### C-SCAN (Circular SCAN)
Moves in one direction, reaches the disk boundary, and returns
to the opposite boundary before continuing.

## 4. Technologies Used

- Programming Language: Python
- GUI Library: Tkinter
- IDE: Visual Studio Code
- Subject: Operating Systems

## 5. System Requirements

- Windows, Linux, or macOS
- Python 3
- Visual Studio Code (optional)
- Tkinter library

No additional Python packages are required for the standard
Python installation that includes Tkinter.

## 6. Project Files

disk_scheduling.py
    Main Python source code containing the GUI and algorithms.

README.md
    Project description and instructions.

## 7. Installation and Execution

Step 1: Install Python from:
https://www.python.org/downloads/

Step 2: Open Visual Studio Code.

Step 3: Create a folder named:
Disk_Scheduling_Module

Step 4: Create a Python file named:
disk_scheduling.py

Step 5: Paste the project source code into the file and save it.

Step 6: Create another file named:
README.md

Step 7: Open Terminal in VS Code.

Step 8: Run the following command:

python disk_scheduling.py

On Windows, you can also try:

py disk_scheduling.py

Step 9: The Disk Scheduling Simulator GUI will open.

## 8. How to Use the Application

1. Enter disk requests separated by commas.
2. Enter the initial disk head position.
3. Enter the maximum cylinder number.
4. Select the initial direction: Right or Left.
5. Click the Run All Algorithms button.
6. View the movement order and total head movement.
7. Compare the results of all four algorithms.

## 9. Sample Input

Disk Requests:
98, 183, 37, 122, 14, 124, 65, 67

Initial Head Position:
53

Maximum Cylinder:
199

Initial Direction:
Right

## 10. Output

The application displays:

- FCFS head movement order and total movement.
- SSTF head movement order and total movement.
- SCAN head movement order and total movement.
- C-SCAN head movement order and total movement.
- The algorithm with the lowest head movement for the given input.

## 11. Conclusion

This project explains the working of four disk scheduling
algorithms used in Operating Systems. It calculates disk head
movement and provides a simple GUI to compare their results.

The project helps students understand disk scheduling concepts
through practical implementation.
