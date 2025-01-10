'''
Jett Kopalek
CSCI342
This program is an example of using the os module of python to compare types of 
CPU scheduling and places the values in a csv file.
Processes include First Come First Serve, Shortest Remaining Job, Shortest Remaining 
Time Next, and Round Robin. Time Quantum is preset to 2,3,6 
'''
#Get dependencies 
import random 
import csv
from copy import deepcopy

class Process:
#Initalize class variables via constructor
    def __init__(self, pid, arrivalTime, burstTime, priority=0):
        self.pid = pid                
        self.arrivalTime = arrivalTime
        self.burstTime = burstTime
        self.remainingTime = burstTime
        self.priority = priority
        self.startTime = None
        self.completionTime = None
        self.waitingTime = 0
        self.turnaroundTime = 0
#String version of class
    def __repr__(self):
        return (f"PID={self.pid}, AT={self.arrivalTime}, BT={self.burstTime}, "
                f"P={self.priority}, WT={self.waitingTime}, TT={self.turnaroundTime}")

#Implemented First Come First Serve
def fcfsScheduling(processes):
#Interface with processes
    processes = sorted(processes, key=lambda x: x.arrivalTime)
    currentTime = 0
#Get Time
    for process in processes:
        if currentTime < process.arrivalTime:
            currentTime = process.arrivalTime
        process.startTime = currentTime
        process.waitingTime = currentTime - process.arrivalTime
        currentTime += process.burstTime
        process.completionTime = currentTime
        process.turnaroundTime = process.completionTime - process.arrivalTime
    averageWaitingTime = sum(p.waitingTime for p in processes) / len(processes)
    return averageWaitingTime

#Implemented Shortest Job Next
def sjnScheduling(processes):
#Interface with process and initialize storage variables
    processes = sorted(processes, key = lambda x: (x.arrivalTime, x.burstTime))
    completed = []
    readyQueue = []
    currentTime = 0
#Get time
    while processes or readyQueue:
#Wait to check first element of processes
        while processes and processes[0].arrivalTime <= currentTime:
            readyQueue.append(processes.pop(0))
        if readyQueue:
            readyQueue = sorted(readyQueue, key=lambda x: x.burstTime)
            currentProcess = readyQueue.pop(0)
            if currentTime < currentProcess.arrivalTime:
                currentTime = currentProcess.arrivalTime
            currentProcess.startTime = currentTime
            currentProcess.waitingTime = currentTime - currentProcess.arrivalTime
            currentTime += currentProcess.burstTime
            currentProcess.completionTime = currentTime
            currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
            completed.append(currentProcess)
        else:
            currentTime = processes[0].arrivalTime
    averageWaitingTime = sum(p.waitingTime for p in completed) / len(completed)
    return averageWaitingTime

#Implemented Shortest Remaining Time Next
def srtnScheduling(processes):
#Interface with processes and initialize storage variables
    processes = sorted(processes, key = lambda x: x.arrivalTime)
    readyQueue = []
    completed = []
    currentTime = 0
#Get time
    while processes or readyQueue:
#Wait to checkfirst element of processes
        while processes and processes[0].arrivalTime <= currentTime:
            readyQueue.append(processes.pop(0))
        if readyQueue:
            readyQueue = sorted(readyQueue, key = lambda x: x.remainingTime)
            currentProcess = readyQueue[0]
            if currentProcess.startTime is None:
                currentProcess.startTime = currentTime
            currentProcess.remainingTime -= 1
            currentTime += 1
            if currentProcess.remainingTime == 0:
                currentProcess.completionTime = currentTime
                currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.burstTime
                completed.append(currentProcess)
                readyQueue.pop(0)
        else:
            if processes:
                currentTime = processes[0].arrivalTime
    averageWaitingTime = sum(p.waitingTime for p in completed) / len(completed)
    return averageWaitingTime

#Implemented Round Robin
def roundRobinScheduling(processes, quantum):
#Interface with processes and initialize storage variables
    processes = sorted(processes, key = lambda x: x.arrivalTime)
    readyQueue = []
    completed = []
    currentTime = 0
    i = 0  # Index for processes
    while i < len(processes) or readyQueue:
        while i < len(processes) and processes[i].arrivalTime <= currentTime:
            readyQueue.append(processes[i])
            i += 1
        if readyQueue:
            currentProcess = readyQueue.pop(0)
            if currentProcess.startTime is None:
                currentProcess.startTime = currentTime
            execTime = min(quantum, currentProcess.remainingTime)
            currentProcess.remainingTime -= execTime
            currentTime += execTime
#Wait to check if before current time
            while i < len(processes) and processes[i].arrivalTime <= currentTime:
                readyQueue.append(processes[i])
                i += 1
            if currentProcess.remainingTime == 0:
                currentProcess.completionTime = currentTime
                currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
                currentProcess.waitingTime = currentProcess.turnaroundTime - currentProcess.burstTime
                completed.append(currentProcess)
            else:
                readyQueue.append(currentProcess)
        else:
            if i < len(processes):
                currentTime = processes[i].arrivalTime
    averageWaitingTime = sum(p.waitingTime for p in completed) / len(completed)
    return averageWaitingTime

#Priority Scheduling function
def priorityScheduling(processes):
#Interface with processes and initialize variables
    processes = sorted(processes, key = lambda x: (x.arrivalTime, x.priority))
    completed = []
    readyQueue = []
    currentTime = 0
    while processes or readyQueue:
#Wait to check first process element
        while processes and processes[0].arrivalTime <= currentTime:
            readyQueue.append(processes.pop(0))
        if readyQueue:
            readyQueue = sorted(readyQueue, key=lambda x: x.priority)
            currentProcess = readyQueue.pop(0)
            if currentTime < currentProcess.arrivalTime:
                currentTime = currentProcess.arrivalTime
            currentProcess.startTime = currentTime
            currentProcess.waitingTime = currentTime - currentProcess.arrivalTime
            currentTime += currentProcess.burstTime
            currentProcess.completionTime = currentTime
            currentProcess.turnaroundTime = currentProcess.completionTime - currentProcess.arrivalTime
            completed.append(currentProcess)
        else:
            if processes:
                currentTime = processes[0].arrivalTime
    averageWaitingTime = sum(p.waitingTime for p in completed) / len(completed)
    return averageWaitingTime

'''
This section generates all of the burst in the program
TLDR: It uses many random numbers and logic to create values to put in the functions above
Notably use unpacking operator to get our ranges
'''

def generateProcessesSameBurst(n, burstTime, priorityRange = (1, 5)):
    processes = []
    for i in range(1, n + 1):
        arrivalTime = random.randint(0, 10)  # Random arrival time between 0 and 10
        priority = random.randint(*priorityRange)
        processes.append(Process(pid = i, arrivalTime = arrivalTime, burstTime = burstTime, priority = priority))
    return processes

def generateProcessesRandomBurst(n, burstTimeRange = (1, 10), priorityRange = (1, 5)):
    processes = []
    for i in range(1, n + 1):
        arrivalTime = random.randint(0, 10)
        burstTime = random.randint(*burstTimeRange)
        priority = random.randint(*priorityRange)
        processes.append(Process(pid = i, arrivalTime = arrivalTime, burstTime = burstTime, priority = priority))
    return processes

def generateProcessesIncreasingBurst(n, start = 1, increment = 1, priorityRange = (1, 5)):
    processes = []
    for i in range(1, n + 1):
        arrivalTime = random.randint(0, 10)
        burstTime = start + increment * (i - 1)
        priority = random.randint(*priorityRange)
        processes.append(Process(pid = i, arrivalTime = arrivalTime, burstTime = burstTime, priority = priority))
    return processes

def generateProcessesDecreasingBurst(n, start = 10, decrement = 1, priorityRange = (1, 5)):
    processes = []
    for i in range(1, n + 1):
        arrivalTime = random.randint(0, 10)
        burstTime = start - decrement * (i - 1)
        priority = random.randint(*priorityRange)
        processes.append(Process(pid = i, arrivalTime = arrivalTime, burstTime = burstTime, priority = priority))
    return processes

#Simulation of scheduling algorithms
def simulateSchedulingAlgorithms(processSets, quantumValues=[2, 3, 6]):
#Dictionary to run algorithms     
    algorithms = {
        'FCFS': fcfsScheduling,
        'SJN': sjnScheduling,
        'SRTN': srtnScheduling,
        'Priority': priorityScheduling
    }
    
    #Round Robin quantum value handler
    rrAlgorithms = {f'RR_Q{q}': lambda p, q = q: roundRobinScheduling(deepcopy(p), q) for q in quantumValues}
    algorithms.update(rrAlgorithms)
    
    results = {}
    
    for setName, processes in processSets.items():
        results[setName] = {}
        for algoName, algoFunc in algorithms.items():
#Deepcopy to prevent modification of original process list
            procCopy = deepcopy(processes)
            avgWait = algoFunc(procCopy)
            results[setName][algoName] = avgWait
    return results

#Make csv file and apply data frame 
def exportToCsv(results, filename):
    with open(filename, mode = 'w', newline = '') as file:
        writer = csv.writer(file)
        header = ['Dataset'] + list(next(iter(results.values())).keys())
        writer.writerow(header)
        for setName, algos in results.items():
            row = [setName] + [f"{algos[algo]:.2f}" for algo in header[1:]]
            writer.writerow(row)
    print(f"\nResults exported to {filename}")

#Driver main function
def main():
    processNumber = 10  
    quantumValues = [2, 3, 6]
    
    #create different datasets
    processSets = {
        'Same Burst Time': generateProcessesSameBurst(processNumber, burstTime = 5),
        'Random Burst Times': generateProcessesRandomBurst(processNumber, burstTimeRange = (1, 10)),
        'Increasing Burst Times': generateProcessesIncreasingBurst(processNumber, start = 3, increment = 2),
        'Decreasing Burst Times': generateProcessesDecreasingBurst(processNumber, start = 10, decrement = 1)
    }
    
#Run Simulation
    results = simulateSchedulingAlgorithms(processSets, quantumValues)
    
#Print results
    for setName, algos in results.items():
        print(f"\nDataset: {setName}")
        print("-" * (len(setName) + 10))
        for algo, avgWait in algos.items():
            print(f"{algo}: Average Waiting Time = {avgWait:.2f}")
    
#Make csv file
    exportToCsv(results, 'scheduling_simulation_results.csv')

if __name__ == "__main__":
    main()
