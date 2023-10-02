class Request:
    def __init__(self, id, processing_time):
        self.id = id
        self.processing_time = processing_time
        self.remaining_time = processing_time
        self.wait_time = 0

    # TODO: Add other necessary methods if required
    def subtract_time(self, time):
        self.remaining_time -= time

def start_scheduling(requests, time_quantum):
    # This function will handle the scheduling algorithm
    
    # TODO: Implement the scheduling algorithm
    # Hint: You might need a queue to keep track of requests
    requests_queue = []
    turnarounds = {}
    tot_waiting_time = 0
    for req in requests:
        requests_queue.append(req)

    elapsed_time = 0
    while len(requests_queue) > 0:
        req = requests_queue.pop(0)
        if req.remaining_time > time_quantum:
            req.subtract_time(time_quantum)
            elapsed_time += time_quantum
            requests_queue.append(req)
        else:
            elapsed_time += req.remaining_time
            req.remaining_time = 0
            turnarounds[req.id] = elapsed_time
            req.wait_time = elapsed_time - req.processing_time
            tot_waiting_time += req.wait_time
            # print(f"Request ID: {req.id}, Wait Time: {req.wait_time}")
            # print(f"Request ID: {req.id}, Turnaround Time: {turnarounds[req.id]}")

    # Save the info for each request at the end of the function
    for req in requests:
        req.remaining_time = req.processing_time
        req.wait_time = 0

    return turnarounds, tot_waiting_time

def scheduling_2(requests, time_quantum):
    pass

def generate_random_requests(num_requests=20):
    import random
    
    # Generates a list of random client requests
    requests = [Request(i, random.randint(1, 10)) for i in range(num_requests)]
    for req in requests:
        print(f"Request ID: {req.id}, Processing Time: {req.processing_time}")
    return requests

def simulate_requests(requests):
    # Simulates the requests by printing their id and processing time
    for time in range(1, 11):
        cur_turnarounds, cur_waiting_time = start_scheduling(requests, time)
        avg_turnaround = sum(cur_turnarounds.values()) / len(cur_turnarounds)
        avg_waiting_time = cur_waiting_time / len(cur_turnarounds)
        print(f"The Average Turnaround at Time Quantum {time} is {avg_turnaround}")
        print(f"The Average Waiting Time at Time Quantum {time} is {avg_waiting_time}")

def main():
    # Assume that we only want to create ONE different set of processes
    # and use it for all the scheduling algorithms with different time quantum
    requests = generate_random_requests()

    requests_tc1 = [Request(0, 3), Request(1, 2), Request(2, 4), Request(3, 5), Request(4, 1)]
    requests_tc2 = [Request(0, 4), Request(1, 6), Request(2, 8), Request(3, 2), Request(4, 4)]

    print('\n**************Test case# 1**************\n')
    # Displaying generated requests
    for req in requests_tc1:
        print(f"Request ID: {req.id}, Processing Time: {req.processing_time}")

    time_quantum = 3  # You can adjust this value based on requirements
    start_scheduling(requests_tc1, time_quantum)


    print('\n**************Test case# 2**************\n')
    # Displaying generated requests
    for req in requests_tc2:
        print(f"Request ID: {req.id}, Processing Time: {req.processing_time}")

    time_quantum = 3  # You can adjust this value based on requirements
    start_scheduling(requests_tc2, time_quantum)

    print()

    simulate_requests(requests)

    # TODO: Calculate and display the average waiting time and average turnaround time

if __name__ == "__main__":
    main()
