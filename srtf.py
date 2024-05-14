#Shortest Remaining Time First (SRTF)

from typing import List, Tuple, Dict
from tabulate import tabulate

# Define types
GanttChartInfo = List[Dict[str, int]]
ProcessInfo = List[Dict[str, int]]

def srtf(arrival_time: List[int], burst_time: List[int]) -> Tuple[ProcessInfo, GanttChartInfo]:
    processes_info = []
    for index, (at, bt) in enumerate(zip(arrival_time, burst_time)):
        processes_info.append({'process': index + 1, 'at': at, 'bt': bt})

    processes_info.sort(key=lambda x: (x['at'], x['bt']))  # Sort processes by arrival time and burst time

    solved_processes_info = []
    gantt_chart_info = []

    current_time = 0
    remaining_time = {p['process']: p['bt'] for p in processes_info}
    ready_queue = []

    while remaining_time:
        for p in processes_info:
            if p['at'] <= current_time and p['process'] in remaining_time:
                ready_queue.append(p)

        if not ready_queue:
            current_time += 1
            continue

        shortest_process = min(ready_queue, key=lambda x: remaining_time.get(x['process'], float('inf')))
        gantt_chart_info.append({
            'process': shortest_process['process'],
            'start': current_time,
            'stop': current_time + 1
        })
        remaining_time[shortest_process['process']] -= 1
        current_time += 1

        if remaining_time[shortest_process['process']] == 0:
            solved_processes_info.append({
                **shortest_process,
                'ft': current_time,
                'tat': current_time - shortest_process['at'],
                'wat': current_time - shortest_process['at'] - shortest_process['bt']
            })
            del remaining_time[shortest_process['process']]
            ready_queue.remove(shortest_process)

    return solved_processes_info, gantt_chart_info


def main():
    # Take user input for arrival time and burst time
    arrival_input = input("Enter arrival times separated by space: ")
    burst_input = input("Enter burst times separated by space: ")

    # Convert input strings to lists of integers
    arrival_time = list(map(int, arrival_input.split()))
    burst_time = list(map(int, burst_input.split()))

    # Run SRTF algorithm
    solved_processes_info, gantt_chart_info = srtf(arrival_time, burst_time)

    # Sort Processes Information by process number
    solved_processes_info.sort(key=lambda x: x['process'])

    # Calculate average Turnaround Time (TAT) and Waiting Time (WT)
    avg_tat = sum(process['tat'] for process in solved_processes_info) / len(solved_processes_info)
    avg_wt = sum(process['wat'] for process in solved_processes_info) / len(solved_processes_info)

    # Print results in table format
    headers = {'process': 'Process', 'at': 'Arrival Time', 'bt': 'Burst Time', 'wat': 'Waiting Time', 'ft': 'Finish Time', 'tat': 'Turnaround Time'}
    print(tabulate(solved_processes_info, headers=headers, tablefmt="grid"))
    print("\nAverage Turnaround Time (TAT):", avg_tat)
    print("Average Waiting Time (WT):", avg_wt)

if __name__ == "__main__":
    main()
