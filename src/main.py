# type: ignore
from simulator import Simulator
import utils

def main():
    queues, random_numbers, time_first_event = utils.parse_definition()
    
    simulator = Simulator(queues=queues, random_numbers=random_numbers, time_first_event=time_first_event)
    
    simulator.simulate()
    print(f"{bold}######### RESULTS #########{reset}")
    print(simulator)

if __name__ == '__main__':
    main()