from enum_ import EventType

class Event:
    def __init__(self, type : EventType, time: float, source_queue = None, dest_queue = None) -> None:
        self.type : EventType = type
        self.time : float     = time
        
        self.source_queue     = source_queue
        self.dest_queue       = dest_queue
            
        self.id   : int       = -1
        
    def __str__(self) -> str:
        return f'ID: {self.id}; Tipo: {self.type.value}; Time: {round(self.time, 2)} {f'; Source Queue: {self.source_queue.name}' if self.source_queue else ''} {f'; Dest Queue: {self.dest_queue.name}' if self.dest_queue else ''}'