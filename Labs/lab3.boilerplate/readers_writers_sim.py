import threading
import time
import random

class ReaderWriterLock:
    def __init__(self):
        self.readers = 0
        self.writers = 0
        self.mutex = threading.Semaphore(1)
        self.writeLock = threading.Semaphore(1)
        self.readLock = threading.Semaphore(1)

    def acquire_read(self):
        # TODO: Implement the reader acquisition logic here
        pass  

    def release_read(self):
        # TODO: Implement the reader release logic here
        pass  

    def acquire_write(self):
        # TODO: Implement the writer acquisition logic here
        pass

    def release_write(self):
        # TODO: Implement the writer release logic here
        pass


class SharedBuffer:
    def __init__(self):
        self.buffer = []
        self.lock = threading.Lock()

    def add_message(self, message):
        with self.lock:
            self.buffer.append(message)

    def read_message(self):
        with self.lock:
            if self.buffer:
                return self.buffer.pop(0)
            else:
                return None

########################### SIMULATION PARAMETERS ###########################
READ_TIME = 2
WRITE_TIME = 3
NUMBER_OF_READERS = 5
NUMBER_OF_WRITERS = 2
#############################################################################

# Implement the online forum and user simulation here

lock = ReaderWriterLock()
buffer = SharedBuffer()

# Reader threads
def reader_thread(thread_id):
    # TODO: you need to do something here

    # TODO: read from the shared buffer

    print(f"Reader {thread_id} is trying to read")
    message = 'YOU SHOULD READ THE MESSAGE FROM THE BUFFER'
    time.sleep(READ_TIME)  # Simulate reading process
    print(f"Reader {thread_id} read: {message}")
    # TODO: you need to do something here


# Writer threads
def writer_thread(thread_id, message):
    # TODO: you need to do something here

    print(f"Writer {thread_id} is trying to write")
    # TODO: add the message to the shared buffer
    
    time.sleep(WRITE_TIME)  # Simulate writing process
    print(f"Writer {thread_id} wrote: {message}")
    # TODO: you need to do something here

def main():
    # Reader threads
    reader_threads = [threading.Thread(target=reader_thread, args=(i,)) for i in range(NUMBER_OF_READERS)]

    # Writer threads
    writer_threads = [threading.Thread(target=writer_thread, args=(i, f"Message {i}")) for i in range(NUMBER_OF_WRITERS)]

    # Create and start reader and writer threads
    for t in reader_threads + writer_threads:
        t.start()

    for t in reader_threads + writer_threads:
        t.join()

if __name__ == '__main__':
    main()

