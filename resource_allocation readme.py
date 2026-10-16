
# Resource Allocation Simulator

## Project Introduction
The Resource Allocation Simulator is a GUI-based Operating
Systems project developed using Python and Tkinter.

It demonstrates how resources are allocated to processes and
how the system checks whether the current allocation is safe.

## Objectives
- Understand resource allocation in Operating Systems.
- Calculate the Need matrix.
- Implement the Banker's safety algorithm.
- Identify safe and unsafe system states.
- Display a safe sequence when one exists.

## Algorithm
The project uses the Banker's safety algorithm.

Need = Maximum - Allocation

The algorithm checks whether each process can finish with the
currently available resources. When a process can finish, its
allocated resources are returned to the available pool.

If all processes can finish, the state is safe.

## Technologies
- Python 3
- Tkinter GUI
- Visual Studio Code

## Files
- resource_allocation.py: Main Python source code
- README.md: Project documentation

## Requirements
- Python 3
- Tkinter
- Visual Studio Code (optional)

No extra Python packages are required.

## How to Run
1. Open Visual Studio Code.
2. Create a folder named Resource_Allocation_Module.
3. Save the Python code as resource_allocation.py.
4. Save this documentation as README.md.
5. Open Terminal in VS Code.
6. Run:

   python resource_allocation.py

   Or on Windows:

   py resource_allocation.py

## Sample Input

Available:
3, 3, 2

Allocation:
0, 1, 0
2, 0, 0
3, 0, 2
2, 1, 1
0, 0, 2

Maximum:
7, 5, 3
3, 2, 2
9, 0, 2
2, 2, 2
4, 3, 3

## Output
The application displays:
- Allocation matrix
- Maximum demand matrix
- Need matrix
- Available resources
- Safe or unsafe status
- Safe sequence when available

## Conclusion
This project demonstrates resource allocation and safe-state
checking using the Banker's safety algorithm. It helps students
understand how an Operating System can avoid entering an unsafe
resource allocation state.
