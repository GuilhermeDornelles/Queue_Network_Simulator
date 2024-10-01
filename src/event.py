from enum_ import EventType

class Event:
    def __init__(self, type : EventType, time: float, dest_queue = None) -> None:
        self.type : EventType = type
        self.time : float     = time
        if dest_queue:
            self.dest_queue = dest_queue
        self.id   : int       = -1
        
    def __str__(self) -> str:
        return f'ID: {self.id}; Tipo: {self.type.value}; Time: {round(self.time, 2)}'