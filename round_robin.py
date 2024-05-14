#Round Robin

from tabulate import tabulate

# Function to find the waiting time for all processes
def find_waiting_time(processes, n, bt, wt, quantum):
    rem_bt = bt.copy()
    t = 0  # Current time
    # Keep traversing processes in round-robin manner until all are finished.
    while True:
        done = True
        # Traverse all processes one by one repeatedly
        for i in range(n):
            # If burst time of a process is greater than 0, there's still more to process
            if rem_bt[i] > 0:
                done = False  # There's still a pending process
                if rem_bt[i] > quantum:
                    # Increase current time by quantum
                    t += quantum
                    # Decrease remaining burst time by quantum
                    rem_bt[i] -= quantum
                else:
                    # Increment current time by the remaining burst time
                    t += rem_bt[i]
                    # Set waiting time as current time minus original burst time
                    wt[i] = t - bt[i]
                    # Remaining burst time is now zero, as the process is finished
                    rem_bt[i] = 0
        # If all processes are done, exit the loop
        if done:
            break

# Function to calculate turnaround time
def find_turnaround_time(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]

# Function to calculate average waiting and turnaround times
def find_avg_time(processes, n, bt, quantum):
    wt = [0] * n
    tat = [0] * n
    find_waiting_time(processes, n, bt, wt, quantum)
    find_turnaround_time(processes, n, bt, wt, tat)

    # Display processes along with all details
    table_data = []
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt += wt[i]
        total_tat += tat[i]
        table_data.append([processes[i], bt[i], wt[i], tat[i]])

    # Display the table using tabulate
    headers = ["Process", "Burst Time", "Waiting Time", "Turnaround Time"]
    table = tabulate(table_data, headers, tablefmt="grid")

    print(table)

    # Display average times with 3 decimal places
    avg_wt = total_wt / n
    avg_tat = total_tat / n
    print(f"\nAverage Waiting Time = {avg_wt:.3f}")
    print(f"Average Turnaround Time = {avg_tat:.3f}")

# Driver code
if __name__ == "__main__":
    n = int(input("Enter the number of processes: "))
    proc = [i + 1 for i in range(n)]  # Process IDs
    burst_time = []
    for i in range(n):
        burst_time.append(int(input(f"Enter Burst Time for Process {i + 1}: ")))
    quantum = int(input("Enter the time quantum: "))
    find_avg_time(proc, n, burst_time, quantum)
