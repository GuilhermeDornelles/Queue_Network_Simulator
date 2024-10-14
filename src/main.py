# type: ignore
from simulator import Simulator
from event import Event, EventType
import utils

def main():
    queues, random_numbers, time_first_event = utils.parse_definition()
    
    first_event = Event(EventType.ARRIVE, time_first_event, None, queues[1])

    simulator = Simulator(queues=queues, random_numbers=random_numbers, first_event=first_event)
    
    simulator.simulate()
    print(f"{utils.bold}######### RESULTS #########{utils.reset}")
    print(simulator)

if __name__ == '__main__':
    main()