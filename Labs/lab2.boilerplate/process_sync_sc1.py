class Request:
    def __init__(self, id, processing_time):
        self.id = id
        self.processing_time = processing_time
        self.remaining_time = processing_time
        self.wait_time = 0

    # TODO: Add other necessary methods if required
    def subtract_time(self, time):
        self.remaining_time -= time

def start_scheduling(requests, time_quantum, arrival_times):
    # This function will handle the scheduling algorithm
    
    # TODO: Implement the scheduling algorithm
    # Hint: You might need a queue to keep track of requests
    requests_queue = []
    turnarounds = {}
    tot_waiting_time = 0
    for req in requests:
        requests_queue.append(req)
    requests_queue.sort(key=lambda x: arrival_times[x.id])

    elapsed_time = 0
    while len(requests_queue) > 0:
        if elapsed_time < arrival_times[requests_queue[0].id]:
            elapsed_time = arrival_times[requests_queue[0].id]
            continue
        req = requests_queue.pop(0)
        if req.remaining_time > time_quantum:
            req.subtract_time(time_quantum)
            elapsed_time += time_quantum
            requests_queue.append(req)
        else:
            elapsed_time += req.remaining_time
            req.remaining_time = 0
            turnarounds[req.id] = elapsed_time - arrival_times[req.id]
            req.wait_time = turnarounds[req.id] - req.processing_time
            tot_waiting_time += req.wait_time
            # print(f"Request ID: {req.id}, Wait Time: {req.wait_time}")
            # print(f"Request ID: {req.id}, Turnaround Time: {turnarounds[req.id]}")

    # Save the info for each request at the end of the function
    for req in requests:
        req.remaining_time = req.processing_time
        req.wait_time = 0

    return turnarounds, tot_waiting_time

def scheduling_2(requests, arrival_times):
    requests_queue = []
    for req in requests:
        requests_queue.append(req)
    requests_queue.sort(key=lambda x: arrival_times[x.id])

    turnarounds = {}
    tot_wait_time = 0

    elapsed_time = 0
    while len(requests_queue) > 0:
        req = requests_queue.pop(0)
        elapsed_time += req.processing_time
        req.remaining_time = 0
        turnarounds[req.id] = elapsed_time - arrival_times[req.id]
        req.wait_time = turnarounds[req.id] - req.processing_time
        tot_wait_time += req.wait_time

    # Save the info for each request at the end of the function
    for req in requests:
        req.remaining_time = req.processing_time
        req.wait_time = 0

    return turnarounds, tot_wait_time

def generate_random_requests(num_requests=20):
    import random
    
    # Generates a list of random client requests
    requests = [Request(i, random.randint(1, 10)) for i in range(num_requests)]
    for req in requests:
        print(f"Request ID: {req.id}, Processing Time: {req.processing_time}")
    return requests

def generate_random_arrivals(requests):
    import random
    
    # Generates a list of random client requests
    arrival_times = {}
    for req in requests:
        arrival_times[req.id] = random.randint(1, 10)
    return arrival_times

def simulate_requests(requests, arrival_times):
    # Simulates the requests by printing their id and processing time
    for time in range(1, 11):
        cur_turnarounds, cur_waiting_time = start_scheduling(requests, time, arrival_times)
        avg_turnaround = sum(cur_turnarounds.values()) / len(cur_turnarounds)
        avg_waiting_time = cur_waiting_time / len(cur_turnarounds)
        print(f"The Average Turnaround at Time Quantum {time} is {avg_turnaround}")
        print(f"The Average Waiting Time at Time Quantum {time} is {avg_waiting_time}")

def simulate_requests_2(requests, arrival_times):
    # Simulates the requests by printing their id and processing time
        cur_turnarounds, cur_waiting_time = scheduling_2(requests, arrival_times)
        avg_turnaround = sum(cur_turnarounds.values()) / len(cur_turnarounds)
        avg_waiting_time = cur_waiting_time / len(cur_turnarounds)
        print(f"The Average Turnaround Time is {avg_turnaround}")
        print(f"The Average Waiting Time is {avg_waiting_time}")

def main():
    # Assume that we only want to create ONE different set of processes
    # and use it for all the scheduling algorithms with different time quantum
    requests = generate_random_requests()
    arrival_times = generate_random_arrivals(requests)

    requests_tc1 = [Request(0, 3), Request(1, 2), Request(2, 4), Request(3, 5), Request(4, 1)]
    requests_tc2 = [Request(0, 4), Request(1, 6), Request(2, 8), Request(3, 2), Request(4, 4)]

    print('\n**************Test case# 1**************\n')
    # Displaying generated requests
    for req in requests_tc1:
        print(f"Request ID: {req.id}, Processing Time: {req.processing_time}")

    time_quantum = 3  # You can adjust this value based on requirements
    start_scheduling(requests_tc1, time_quantum, arrival_times)


    print('\n**************Test case# 2**************\n')
    # Displaying generated requests
    for req in requests_tc2:
        print(f"Request ID: {req.id}, Processing Time: {req.processing_time}")

    time_quantum = 3  # You can adjust this value based on requirements
    start_scheduling(requests_tc2, time_quantum, arrival_times)

    print("------------Scheduling Algorithm 1-------------")
    simulate_requests(requests, arrival_times)

    print("------------Scheduling Algorithm 2-------------")
    simulate_requests_2(requests, arrival_times)

    # TODO: Calculate and display the average waiting time and average turnaround time

if __name__ == "__main__":
    main()
