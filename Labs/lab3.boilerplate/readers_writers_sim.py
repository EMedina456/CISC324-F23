import threading
import time
import random

class ReaderWriterLock:
    def __init__(self):
        self.readers = 0
        self.writers = 0
        self.mutex = threading.Semaphore(1)
        self.writeLock = threading.Semaphore(1)
        self.readLock = threading.Semaphore(5)

    def acquire_read(self):
        self.readLock.acquire()
        self.mutex.acquire()
        self.readers += 1
        if self.readers == 1:
            self.writeLock.acquire()
        self.mutex.release()

    def release_read(self):
        self.readLock.release()
        self.mutex.acquire()
        self.readers -= 1
        if self.readers == 0:
            self.writeLock.release()
        self.mutex.release()

    def acquire_write(self):
        self.writeLock.acquire()
        self.mutex.acquire()

    def release_write(self):
        self.mutex.release()
        self.writeLock.release()


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
READ_TIME = random.randint(1, 4)
WRITE_TIME = random.randint(1, 4)
NUMBER_OF_READERS = random.randint(1, 4)
NUMBER_OF_WRITERS = random.randint(1, 4)
#############################################################################

# Implement the online forum and user simulation here

lock = ReaderWriterLock()
buffer = SharedBuffer()

# Reader threads
def reader_thread(thread_id):
    lock.acquire_read()

    message = buffer.read_message()

    print(f"Reader {thread_id} is trying to read")
    # message = 'YOU SHOULD READ THE MESSAGE FROM THE BUFFER'
    time.sleep(READ_TIME)  # Simulate reading process
    print(f"Reader {thread_id} read: {message}")

    lock.release_read()


# Writer threads
def writer_thread(thread_id, message):
    lock.acquire_write()

    print(f"Writer {thread_id} is trying to write")
    buffer.add_message(message)
    time.sleep(WRITE_TIME)  # Simulate writing process
    print(f"Writer {thread_id} wrote: {message}")
    lock.release_write()

def main():
    # Reader threads
    reader_threads = [threading.Thread(target=reader_thread, args=(i,)) for i in range(NUMBER_OF_READERS)]

    # Writer threads
    writer_threads = [threading.Thread(target=writer_thread, args=(i, f"Message {i}")) for i in range(NUMBER_OF_WRITERS)]

    # Create and start reader and writer threads
    for t in writer_threads + reader_threads:
        t.start()

    for t in writer_threads + reader_threads:
        t.join()

if __name__ == '__main__':
    main()

