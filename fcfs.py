#First Come First Serve (FCFS)

from typing import List, Tuple, Dict
from tabulate import tabulate

# Define types
GanttChartInfo = List[Dict[str, int]]
ProcessInfo = List[Dict[str, int]]

def fcfs(arrival_time: List[int], burst_time: List[int]) -> Tuple[ProcessInfo, GanttChartInfo]:
    processes_info = []
    for index, (at, bt) in enumerate(zip(arrival_time, burst_time)):
        processes_info.append({'process': index + 1, 'at': at, 'bt': bt})

    processes_info.sort(key=lambda x: x['at'])  # Sort processes by arrival time

    finish_time = []
    gantt_chart_info = []

    for index, process in enumerate(processes_info):
        if index == 0 or process['at'] > finish_time[index - 1]:
            finish_time.append(process['at'] + process['bt'])
        else:
            finish_time.append(finish_time[index - 1] + process['bt'])

        gantt_chart_info.append({
            'process': process['process'],
            'start': process['at'] if index == 0 else finish_time[index - 1],
            'stop': finish_time[index]

        })

        process['ct'] = finish_time[index]
        process['tat'] = finish_time[index] - process['at']
        process['wat'] = finish_time[index] - process['at'] - process['bt']

    return processes_info, gantt_chart_info

def main():
    # Take user input for arrival time and burst time
    arrival_input = input("Enter arrival times separated by space: ")
    burst_input = input("Enter burst times separated by space: ")

    # Convert input strings to lists of integers
    arrival_time = list(map(int, arrival_input.split()))
    burst_time = list(map(int, burst_input.split()))

    # Run FCFS algorithm
    solved_processes_info, gantt_chart_info = fcfs(arrival_time, burst_time)

    # Sort Processes Information by process number
    solved_processes_info.sort(key=lambda x: x['process'])

    # Calculate average Turnaround Time (TAT) and Waiting Time (WT)
    avg_tat = sum(process['tat'] for process in solved_processes_info) / len(solved_processes_info)
    avg_wt = sum(process['wat'] for process in solved_processes_info) / len(solved_processes_info)

    # Print results in table format
    headers = {'process': 'Process', 'at': 'Arrival Time', 'bt': 'Burst Time', 'wat': 'Waiting Time', 'ct': 'Completion Time', 'tat': 'Turnaround Time'}
    print(tabulate(solved_processes_info, headers=headers, tablefmt="grid"))
    print("\nAverage Turnaround Time (TAT):", avg_tat)
    print("Average Waiting Time (WT):", avg_wt)

if __name__ == "__main__":
    main()
