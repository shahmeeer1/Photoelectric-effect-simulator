

class Queue:
    def __init__(self, length, active):
        # Initialise queue
        self.Length = length
        self.Queue = ['' for x in range(self.Length)] # Initialize queue with empty strings
        self.FrontPointer = 0 # Pointer to the front of the queue
        self.RearPointer = 0 # Pointer to the rear of the queue
        self.Active = active # Indicates if the queue is active (being modified)

    def display(self):
        # Display contents and active status of queue
        if self.Active:
            print(self.Queue)

    def reset(self):
        # Resets pointers and reversed status of queue
        self.FrontPointer = 0
        self.RearPointer = 0

    def empty(self):
        # Checks if queue is empty
        return not self.FrontPointer != self.RearPointer

    def is_full(self):
        # Checks if queue is full
        return self.RearPointer >= self.Length

    def is_active(self):
        # Checks if the current queue is active
        return self.Active

    def enqueue(self, Metal):
        # Adds elements to queue
        if self.is_full():
            print("QUEUE IS FULL")
            return False

        # Add element to queue and update pointers
        self.Queue[self.RearPointer] = Metal
        self.RearPointer += 1
        return

    def dequeue(self, Inactive, Metal):
        # Remove metal from queue and update active status
        if self.empty():
            print("QUEUE IS EMPTY")
            return

        # Reset inactive queue
        Inactive.reset()

        while True:
            if self.empty():
                # If the queue is empty, update the active status and break
                self.Active = False
                Inactive.Active = True
                break

            if self.Active:
                if self.Queue[self.FrontPointer] == Metal:
                    # If unwanted metal is found, dequeue it
                    self.Queue[self.FrontPointer] = ""
                    self.FrontPointer += 1
                else:
                    # Move wanted elements to other queue and update pointers
                    Inactive.enqueue(self.Queue[self.FrontPointer])
                    self.Queue[self.FrontPointer] = ""
                    self.FrontPointer += 1
        return


class QueueManager:
    # class to manage and maintain queues
    def __init__(self, length):
        # Initialize a queue manager with two queues.
        self.queue1 = Queue(length, True) # Initialize first queue as active
        self.queue2 = Queue(length, False) # Initialize second queue as inactive
        self.QueueList = [self.queue1, self.queue2] # List to manage both queues

    def enqueue(self, Metal):
        # Add an element in the active queue
        for queue in self.QueueList:
            if queue.is_active():
                queue.enqueue(Metal)

    def dequeue(self, Metal):
        # Remove an element from the active queue.
        active_queue = None
        inactive_queue = None
        for queue in self.QueueList:
            # Update the active and inactive status of queues
            if queue.is_active():
                active_queue = queue
            else:
                inactive_queue = queue

        if active_queue and inactive_queue:
            # recursively shifts elements from inactive queue to active queue
            active_queue.dequeue(inactive_queue, Metal)

    def display(self):
        # Display the contents of both queues.
        for i in self.QueueList:
            i.display()

    def elements(self):
        # Get the elements of the active queue
        for queue in self.QueueList:
            if queue.is_active():
                return queue.Queue

