from typing import List
from enum_ import EventType
from scheduler import Scheduler
from event import Event
from connector import Connector

class SimpleQueue:
    def __init__(self, name: str, capacity : int, servers : int, min_arrival : int, max_arrival : int, min_service : int, max_service : int) -> None:
        self.name            : str             = name

        self.capacity        : int             = capacity
        self.servers         : int             = servers
        
        self.min_arrival     : int             = min_arrival
        self.max_arrival     : int             = max_arrival
        self.min_service     : int             = min_service
        self.max_service     : int             = max_service
        self.scheduler       : Scheduler       = None

        self.time_last_event : float           = 0        
        self.customers       : int             = 0
        self.losses          : int             = 0
        self.status          : int             = 0
        self.states                            = []
        self.__init_states()
        self.random_interval                   = None
        self.next_random                       = None
        self.connectors      : List[Connector] = []

    
    def arrive(self, time: float):
        if self.capacity == -1 or self.status < self.capacity:
            self.enqueue()
            if self.status <= self.servers:
                delta_time = time + self.random_interval(self.min_service, self.max_service)
                self.scheduler.add_event(Event(type=EventType.PASS, time=delta_time, source_queue=self))
        else:
            self.loss()

        delta_time = time + self.random_interval(self.min_arrival, self.max_arrival)
        self.scheduler.add_event(Event(type=EventType.ARRIVE, time=delta_time, dest_queue=self))
        
    def pass_to(self, time: float):
        dest_queue = self.define_dest_queue(self.next_random()).dest_queue
        self.dequeue()
        
        if self.status >= self.servers:
            delta_time = time + self.random_interval(self.min_service, self.max_service)
            self.scheduler.add_event(Event(type=EventType.PASS, time=delta_time, source_queue=self)) 
        
        if dest_queue.name != 'EXIT':
            if dest_queue.capacity == -1 or dest_queue.status < dest_queue.capacity:
                dest_queue.enqueue()
                if dest_queue.status <= dest_queue.servers:
                    delta_time = time + self.random_interval(dest_queue.min_service, dest_queue.max_service)
                    self.scheduler.add_event(Event(type=EventType.PASS, time=delta_time, source_queue=dest_queue))
            else:
                dest_queue.loss()
        
    def add_connector(self, connector: Connector):
        self.connectors.append(connector)
        self.connectors.sort(key=lambda x: x.probability)
        
    def define_dest_queue(self, random_number: float):
        accum = 0

        for connector in self.connectors:
            accum += connector.probability
            if random_number <= accum:
                return connector

    def loss(self):
        self.losses += 1
    
    def acummulate_time(self, delta_time : float):
        self.states[self.status] = self.states[self.status] + (delta_time-self.time_last_event)
        self.time_last_event = delta_time
    
    def enqueue(self) -> bool:
        if self.capacity == -1 or self.status < self.capacity:
            self.status += 1
            if self.name != 'EXIT' and self.status >= (len(self.states)-1):
                self.states.append(0.0)
            return True
        return False
    
    def dequeue(self) -> bool:
        if (self.status > 0):
            self.status -= 1
            return True
        
        return False
    
    def __init_states(self):
        if self.capacity != -1:
            for i in range(self.capacity+1):
                self.states.append(0.0)
        else:
            self.states.append(0.0)
    
    def __str__(self) -> str:
        return f'Queue {self.name}\n  Parameters:\n    Capacity: {self.capacity if self.capacity > 0 else 'infinite'};\n    Servers: {self.servers};\n  Final values:\n    Losses: {self.losses};\n    States:\n{self.__states_to_str()}'
    
    def __states_to_str(self) -> str:
        res = ''
        
        res += '    Total time per state:\n'
        
        for i in range(len(self.states)):
            if self.states[i] > 0:
                res += f'      {i}: {round(self.states[i],2)}\n'
        
        if self.time_last_event > 0:
            res += '    Probability Distribution:\n'
            
            for i in range(len(self.states)):
                if self.states[i] > 0:
                    res += f'      {i}: {round((self.states[i]/self.time_last_event) * 100, 2)} %{"\n" if i < len(self.states)-1 else ""}'
        
        return res