# CPU Scheduling Simulation with Python

**Author:** Jett Kopalek  
**Course:** CSCI342  
**Project Description:**  
This program demonstrates several fundamental CPU scheduling algorithms using Python's built-in `os`, `csv`, and `random` modules. It simulates process scheduling using a variety of strategies and outputs the average waiting time for each to a CSV file.

---

## Overview

This scheduling simulator includes the following algorithms:

- **First Come First Serve (FCFS)**
- **Shortest Job Next (SJN)**
- **Shortest Remaining Time Next (SRTN)**
- **Priority Scheduling**
- **Round Robin** (Quantum values: `2`, `3`, and `6`)

Processes are simulated with different burst time patterns:
- Same burst time
- Random burst times
- Increasing burst times
- Decreasing burst times

---

## How It Works

Each scheduling algorithm is implemented as a function that calculates the average waiting time of a list of `Process` objects. 

The program:
1. Randomly generates process datasets
2. Runs each scheduling algorithm on each dataset
3. Records the average waiting times
4. Exports the results to a CSV file

---

## Concepts Demonstrated

- Process simulation and state management
- Priority and burst-time based sorting
- CPU time tracking
- Round Robin time slicing
- Algorithm benchmarking and comparison
- File output using CSV

---

##  Getting Started

### Dependencies

This script uses only built-in Python modules:

- `random`
- `csv`
- `copy`

### Running the Program

```bash
python3 scheduling_simulation.py
