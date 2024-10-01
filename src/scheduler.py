from event import Event 

class Scheduler:
    def __init__(self) -> None:
        self.events          : list = []
        self.executed_events : list = []
        self.last_event_id   : int  = 0
        
    def get_next_event(self) -> Event:
        res = None
        
        if len(self.events) > 0:
            res = self.events.pop(0)
        
        if res:
            self.executed_events.append(res)
        
        return res
    
    def add_event(self, event: Event):
        self.last_event_id += 1
        event.id = self.last_event_id
        
        self.events.append(event)
        self.events = sorted(self.events, key=lambda ev: ev.time)