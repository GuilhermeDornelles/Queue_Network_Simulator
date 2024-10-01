

class Connector:
    def __init__(self, source_queue, dest_queue, probability) -> None:
        self.source_queue = source_queue
        self.dest_queue = dest_queue
        self.probability = probability
        
    def __str__(self) -> str:
        return f"Source Queue: {self.source_queue.name}; Dest Queue: {self.dest_queue.name}; Probability: {round(self.probability, 2)}"