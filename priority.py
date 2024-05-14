# Priority scheduling

from tabulate import tabulate
# Function to find the waiting time for all processes
def find_waiting_time(processes, n, wt):
    wt[0] = 0

    # Calculate waiting time for all other processes
    for i in range(1, n):
        wt[i] = processes[i - 1][1] + wt[i - 1]  # Burst time + previous waiting time

# Function to calculate turnaround time
def find_turnaround_time(processes, n, wt, tat):
    # Turnaround time is burst time + waiting time
    for i in range(n):
        tat[i] = processes[i][1] + wt[i]  # Burst time + waiting time

# Function to calculate average waiting and turnaround times
def find_avg_time(processes, n):
    wt = [0] * n
    tat = [0] * n
    find_waiting_time(processes, n, wt)
    find_turnaround_time(processes, n, wt, tat)

    total_wt = sum(wt)
    total_tat = sum(tat)

    avg_waiting_time = total_wt / n  # Calculate average waiting time
    return avg_waiting_time, wt

# Priority scheduling function
def priority_scheduling(proc, n):
    # Sort processes by arrival time and then by burst time
    proc.sort(key=lambda x: x[2])  # Sort by arrival time
    avg_waiting_time, wt = find_avg_time(proc, n)

    # Prepare data for tabulate
    table_data = []
    for i in range(n):
        table_data.append([proc[i][0], proc[i][1], proc[i][2], wt[i]])

    headers = ["Process ID", "Burst Time", "Arrival Time", "Waiting Time"]
    table = tabulate(table_data, headers, tablefmt="grid")

    print(table)
    print(f"\nAverage Waiting Time = {avg_waiting_time:.3f}")

# Driver code
if __name__ == "__main__":
    n = int(input("Enter the number of processes: "))
    proc = []
    for i in range(n):
        burst_time = int(input(f"Enter burst time for process {i + 1}: "))
        arrival_time = int(input(f"Enter arrival time for process {i + 1}: "))
        proc.append([i + 1, burst_time, arrival_time])

    priority_scheduling(proc, n)