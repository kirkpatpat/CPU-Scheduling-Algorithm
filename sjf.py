#Shortest Job First (SJF)

from typing import List, Dict, Tuple
from tabulate import tabulate

# Define types
GanttChartInfo = List[Dict[str, int]]
ProcessInfo = List[Dict[str, int]]

def sjf(arrival_time: List[int], burst_time: List[int]) -> Tuple[ProcessInfo, GanttChartInfo]:
    processes_info = []
    for index, (at, bt) in enumerate(zip(arrival_time, burst_time)):
        processes_info.append({'process': index + 1, 'at': at, 'bt': bt})

    processes_info.sort(key=lambda x: (x['at'], x['bt']))  # Sort processes by arrival time and burst time

    finish_time = []
    gantt_chart_info = []
    solved_processes_info = []
    ready_queue = []
    finished_jobs = []

    for i, process in enumerate(processes_info):
        if i == 0:
            ready_queue.append(process)
            finish_time.append(process['at'] + process['bt'])
            solved_processes_info.append({
                **process,
                'ft': finish_time[i],
                'tat': finish_time[i] - process['at'],
                'wat': finish_time[i] - process['at'] - process['bt']
            })

            for p in processes_info:
                if p['at'] <= finish_time[0] and p not in ready_queue:
                    ready_queue.append(p)

            ready_queue.pop(0)
            finished_jobs.append(processes_info[0])

            gantt_chart_info.append({
                'process': processes_info[0]['process'],
                'start': processes_info[0]['at'],
                'stop': finish_time[0],
            })
        else:
            if len(ready_queue) == 0 and len(finished_jobs) != len(processes_info):
                unfinished_jobs = [p for p in processes_info if p not in finished_jobs]
                unfinished_jobs.sort(key=lambda x: (x['at'], x['bt']))
                ready_queue.append(unfinished_jobs[0])

            rq_sorted_by_bt = sorted(ready_queue, key=lambda x: (x['bt'], x['at']))
            process_to_execute = rq_sorted_by_bt[0]
            previous_finish_time = finish_time[-1]

            if process_to_execute['at'] > previous_finish_time:
                finish_time.append(process_to_execute['at'] + process_to_execute['bt'])
                newest_finish_time = finish_time[-1]
                gantt_chart_info.append({
                    'process': process_to_execute['process'],
                    'start': process_to_execute['at'],
                    'stop': newest_finish_time,
                })
            else:
                finish_time.append(previous_finish_time + process_to_execute['bt'])
                newest_finish_time = finish_time[-1]
                gantt_chart_info.append({
                    'process': process_to_execute['process'],
                    'start': previous_finish_time,
                    'stop': newest_finish_time,
                })

            solved_processes_info.append({
                **process_to_execute,
                'ft': newest_finish_time,
                'tat': newest_finish_time - process_to_execute['at'],
                'wat': newest_finish_time - process_to_execute['at'] - process_to_execute['bt']
            })

            for p in processes_info:
                if p['at'] <= newest_finish_time and p not in ready_queue and p not in finished_jobs:
                    ready_queue.append(p)

            ready_queue.remove(process_to_execute)
            finished_jobs.append(process_to_execute)

    return solved_processes_info, gantt_chart_info

def main():
    # Take user input for arrival time and burst time
    arrival_input = input("Enter Arrival Times separated by space: ")
    burst_input = input("Enter Burst Times separated by space: ")

    # Convert input strings to lists of integers
    arrival_time = list(map(int, arrival_input.split()))
    burst_time = list(map(int, burst_input.split()))

    # Run SJF algorithm
    solved_processes_info, gantt_chart_info = sjf(arrival_time, burst_time)

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
