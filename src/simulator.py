from queue_1 import SimpleQueue
from scheduler import Scheduler
from enum_ import EventType
from event import Event

class Simulator:
    def __init__(self, queues: list[SimpleQueue], random_numbers : list, time_first_event : int) -> None:
        self.queues            : list[SimpleQueue] = queues
        self.scheduler         : Scheduler         = Scheduler()
        
        for i in range(len(self.queues)):
            q = self.queues[i]
            q.random_interval = self.random_interval
            q.scheduler = self.scheduler

        self.random_numbers    : list              = random_numbers
        self.last_random_index : int               = 0
        self.time_last_event   : float             = 0
        self.time              : float             = 0
        self.scheduler.add_event(Event(EventType.ARRIVE, time_first_event))
    
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
                    self.queues[0].arrive(self.time, self.queues[1])
                elif event.type == EventType.LEAVE:
                    self.queues[1].leave(self.time)
                else:
                    self.queues[0].pass_to_queue(self.time, event.dest_queue)
            else:
                self.running = False
    
    def __acummulate_time_to_queues(self, delta_time : float):
        for q in self.queues:
            q.acummulate_time(delta_time=delta_time)
    
    def __all_random_used(self) -> bool:
        return self.last_random_index >= len(self.random_numbers)
    
    def random_interval(self, a : int, b : int) -> float:
        if self.last_random_index < len(self.random_numbers):
            random_number = self.random_numbers[self.last_random_index]
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
            res += f"{q};\n"
        
        res += f"]\n"
        
        return res