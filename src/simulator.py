from queue_1 import SimpleQueue
from scheduler import Scheduler
from enum_ import EventType
from event import Event

class Simulator:
    def __init__(self, queues: list[SimpleQueue], random_numbers : list, first_event : Event) -> None:
        self.queues            : list[SimpleQueue] = queues
        self.scheduler         : Scheduler         = Scheduler()
        
        for i in range(len(self.queues)):
            q = self.queues[i]
            q.random_interval = self.random_interval
            q.next_random     = self.get_next_random_number
            q.scheduler = self.scheduler

        self.random_numbers    : list              = random_numbers
        self.last_random_index : int               = 0
        self.time_last_event   : float             = 0
        self.time              : float             = 0
        self.scheduler.add_event(first_event)
    
    def simulate(self):
        self.running = True
        while(self.running):
            if not self.__all_random_used():
                event : Event = self.scheduler.get_next_event()
            else:
                event = None
                
            if event:
                self.time_last_event = self.time
                self.time = event.time
                
                self.__acummulate_time_to_queues(self.time)

                if event.type == EventType.ARRIVE:
                    event.dest_queue.arrive(self.time)
                else:
                    event.source_queue.pass_to(self.time_last_event)
            else:
                self.running = False
    
    def __acummulate_time_to_queues(self, delta_time : float):
        for q in self.queues:
            if q.name != 'EXIT':
                q.acummulate_time(delta_time=delta_time)
    
    def __all_random_used(self) -> bool:
        return self.last_random_index >= len(self.random_numbers)
    
    def get_next_random_number(self):
        if self.last_random_index < len(self.random_numbers):
            random_number = self.random_numbers[self.last_random_index]
            self.last_random_index += 1
            return random_number

        self.running = False
        return -1
    
    def random_interval(self, a : int, b : int) -> float:
        random_number = self.get_next_random_number()
        if random_number > 0:
            self.last_random_index += 1
            return a + ((b-a)*random_number)
        else:
            self.running = False
            return -1
        
    def __str__(self) -> str:
        res = ""
        
        res += f"Simulation Time: {round(self.time, 2)}"
        res += f"\nqueues\n[\n"
        
        for q in self.queues:
            if q.name != 'EXIT':
                res += f"{q};\n"
        
        res += f"]\n"
        
        return res