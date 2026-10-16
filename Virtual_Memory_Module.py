
# Virtual Memory Simulator

## Project Introduction
The Virtual Memory Simulator is a GUI-based Operating Systems
project developed using Python and Tkinter.

It demonstrates how page replacement algorithms manage pages
when the available memory frames are limited.

## Objectives
- Understand virtual memory and paging.
- Implement page replacement algorithms.
- Calculate page hits and page faults.
- Compare algorithm performance.
- Display simulation results in a GUI.

## Algorithms

### 1. FIFO
First In, First Out replaces the page that entered memory first.

### 2. LRU
Least Recently Used replaces the page that has not been used
for the longest time.

### 3. Optimal
Optimal replaces the page whose next use is farthest in the
future, or which will not be used again.

## Technologies
- Python 3
- Tkinter GUI
- Visual Studio Code

## Files
- virtual_memory.py — Main application source code
- README.md — Project documentation

## Requirements
- Python 3 installed
- Tkinter available with the Python installation
- Visual Studio Code (optional)

No additional Python packages are required.

## How to Run

1. Open Visual Studio Code.
2. Create a folder named Virtual_Memory_Module.
3. Create a file named virtual_memory.py.
4. Paste the Python source code into the file.
5. Create a README.md file and paste this documentation.
6. Open Terminal in VS Code.
7. Run:

   python virtual_memory.py

   Alternatively, on Windows:

   py virtual_memory.py

8. The Virtual Memory Simulator window will open.

## How to Use

1. Enter the page reference string separated by commas.
2. Enter the number of memory frames.
3. Click Run Simulation.
4. Compare page hits and page faults.
5. Review the frame history shown for each algorithm.

## Sample Input

Page Reference String:
7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2

Number of Frames:
3

## Output
The application displays:
- Page replacement history
- Page hits
- Page faults
- Total pages
- Algorithm with the lowest number of page faults

## Conclusion
This project provides a practical demonstration of virtual
memory and page replacement. It helps students understand how
FIFO, LRU, and Optimal manage memory frames.
