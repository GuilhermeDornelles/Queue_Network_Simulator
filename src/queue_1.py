from enum_ import EventType
from scheduler import Scheduler
from event import Event

class SimpleQueue:
    def __init__(self, name: str, capacity : int, servers : int, min_arrival : int, max_arrival : int, min_service : int, max_service : int) -> None:
        self.name            : str       = name
        
        self.capacity        : int       = capacity
        self.servers         : int       = servers
        
        self.min_arrival     : int       = min_arrival
        self.max_arrival     : int       = max_arrival
        self.min_service     : int       = min_service
        self.max_service     : int       = max_service
        self.scheduler       : Scheduler = None

        self.time_last_event : float     = 0        
        self.customers       : int       = 0
        self.losses          : int       = 0
        self.status          : int       = 0
        self.states                      = []
        self.__init_states()
        self.random_interval             = None
    
    def leave(self, time: float):
        self.dequeue()
        
        if self.status >= self.servers:
            delta_time = time + self.random_interval(self.min_service, self.max_service)
            self.scheduler.add_event(Event(EventType.LEAVE, delta_time))
    
    def arrive(self, time: float, dest_queue):
        if self.status < self.capacity:
            self.enqueue()
            if self.status <= self.servers:
                delta_time = time + self.random_interval(self.min_service, self.max_service)
                self.scheduler.add_event(Event(EventType.PASS, delta_time, dest_queue))
        else:
            self.loss()

        delta_time = time + self.random_interval(self.min_arrival, self.max_arrival)
        self.scheduler.add_event(Event(EventType.ARRIVE, delta_time))
        
    def pass_to_queue(self, time: float, dest_queue):
        self.dequeue()
        
        if self.status >= self.servers:
            delta_time = time + self.random_interval(self.min_service, self.max_service)
            self.scheduler.add_event(Event(EventType.PASS, delta_time, dest_queue)) 
        
        if dest_queue.status < dest_queue.capacity:
            dest_queue.enqueue()
            if dest_queue.status <= dest_queue.servers:
                delta_time = time + self.random_interval(dest_queue.min_service, dest_queue.max_service)
                self.scheduler.add_event(Event(EventType.LEAVE, delta_time))
        else:
            dest_queue.loss()
        
    def loss(self):
        self.losses += 1
    
    def acummulate_time(self, delta_time : float):
        self.states[self.status] = self.states[self.status] + (delta_time-self.time_last_event)
        self.time_last_event = delta_time
    
    def enqueue(self) -> bool:
        if (self.status < self.capacity):
            self.status += 1
            return True
        return False
    
    def dequeue(self) -> bool:
        if (self.status > 0):
            self.status -= 1
            return True
        
        return False
    
    def __init_states(self):
        for i in range(self.capacity+1):
            self.states.append(0.0)
    
    def __str__(self) -> str:
        return f'Queue {self.name}\n  Parameters:\n    Capacity: {self.capacity};\n    Servers: {self.servers};\n  Final values:\n    Losses: {self.losses};\n    States:\n{self.__states_to_str()}'
    
    def __states_to_str(self) -> str:
        res = ''
        
        res += '    Total time per state:\n'
        
        for i in range(len(self.states)):
            res += f'      {i}: {round(self.states[i],4)}\n'
        
        if self.time_last_event > 0:
            res += '    Probability Distribution:\n'
            
            for i in range(len(self.states)):
                res += f'      {i}: {round((self.states[i]/self.time_last_event) * 100, 4)} %{"\n" if i < len(self.states)-1 else ""}'
        
        return res