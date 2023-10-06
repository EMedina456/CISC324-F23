The 2 scheduling algorithms were implemented according to instructions. The first algorithm, executes processes in a round-robin fashion with a specified time 
quantum, while the second algorithm executes processes in a first-in-first-out fashion, finishing the current process before executing the next. The 2nd or FIFO 
scheduling algorithm doesn't take any time quantum into account, because FIFO algorithms typically execute a process until it's finished, there is no need to test 
for different cases regarding varying time quantum. 

Running both schedulers with the same set of randomly generated processes gives us the following results:
------------Scheduling Algorithm 1-------------
The Average Turnaround at Time Quantum 1 is 68.0
The Average Waiting Time at Time Quantum 1 is 62.85
The Average Turnaround at Time Quantum 2 is 67.45
The Average Waiting Time at Time Quantum 2 is 62.3
The Average Turnaround at Time Quantum 3 is 69.5
The Average Waiting Time at Time Quantum 3 is 64.35
The Average Turnaround at Time Quantum 4 is 66.4
The Average Waiting Time at Time Quantum 4 is 61.25
The Average Turnaround at Time Quantum 5 is 65.65
The Average Waiting Time at Time Quantum 5 is 60.5
The Average Turnaround at Time Quantum 6 is 60.45
The Average Waiting Time at Time Quantum 6 is 55.3
The Average Turnaround at Time Quantum 7 is 59.15
The Average Waiting Time at Time Quantum 7 is 54.0
The Average Turnaround at Time Quantum 8 is 55.1
The Average Waiting Time at Time Quantum 8 is 49.95
The Average Turnaround at Time Quantum 9 is 52.6
The Average Waiting Time at Time Quantum 9 is 47.45
The Average Turnaround at Time Quantum 10 is 52.6
The Average Waiting Time at Time Quantum 10 is 47.45


------------Scheduling Algorithm 2-------------
The Average Turnaround Time is 52.6
The Average Waiting Time is 47.45

Multiple runs of the program give similar results. 

Based on the results of running both schedulers with the same set of data, the 2nd scheduling algorithm appears to be more appropriate for the set of processes. 
The FIFO scheduler consistently provides lower averages on both turnaround and waiting times. The FIFO scheduler consistently outperforms the round-robin scheduler
in terms of turnaround time suggesting that processes finish their execution faster in the FIFO algorithm. This is also similar regarding waiting times, it 
suggests that processes are spending less time waiting in queue before execution in the FIFO scheduler. These could be due to scenarios where both short and 
long-running processes are mixed, contributing to a longer waiting time due to context switching, which is more obvious in cases of lower time quantum. 
Looking at the results, we can see that smaller time quantum values lead to higher turnaround and waiting times due to frequent context switching. Because process
information is constantly being saved and saved information constantly loaded, time is taken each time context switching occurs. As the time quantum is increased,
average turnaround and waiting times decrease. This indicates that a longer time quantum is more effective at scheduling processes for this set of processes 
compared to a lower time quantum. At a time quantum of ten, turnaround and waiting times are equal to the results of the FIFO scheduler. This is due to the 
processes having random processing times up to 10, so with a time quantum of ten, there is no context switching occurring. 
In this context, the FIFO scheduling algorithm will always produce equal or better results(in terms of waiting and turnaround time) than the round-robin scheduling
algorithm due to context switching. The fastest time at which the round-robin scheduler executes all processes, is when no context switching occurs, and would 
behave identical to FIFO algorithm. However, it's important to note that the FIFO scheduler can't perform any time-sharing actions so it may be more appropriate
to use the round-robin scheduler in other situations. 