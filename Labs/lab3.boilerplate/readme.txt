This module implements the readers-writers problem using semaphores.
The expected behavior is that the first writer should be written first, 
as well as the readers continuing right after.

The program creates a shared resource, represented by a list, and 
simulates multiple readers and writers accessing it concurrently. 
Readers can access the resource simultaneously, while writers have 
exclusive access to it.

The program outputs the actions performed by each thread, including 
when a thread starts reading or writing, and when it finishes. 
The output should show that the first writer is executed first, 
followed by the readers.

# output
Writer 0 is trying to write
Writer 0 wrote: Message 0
Reader 0 is trying to read
Reader 1 is trying to read
Reader 2 is trying to read
Reader 3 is trying to read
Reader 0 read: Message 0
Reader 1 read: None
Reader 3 read: None
Reader 2 read: None

As we see here, there are 3 readers and 1 writer. The reader 0
reads the message of the writer, while the other readers read None
because it is popped from the buffer list. The readers all run
concurrently, while the writer runs exclusively first. This is tested
through a number of outputs using random library.