
from generator import Generator
import json
from queue_1 import SimpleQueue

bold = "\033[1m"
reset = "\033[0m"
    
def parse_definition():
    file = open('definition.json')
    definition = json.loads(file.read())
    print(f"{bold}######### DEFINITION #########{reset}")
    print(json.dumps(definition, indent=4))
        
    time_first_event = definition["time_first_event"]

    random_numbers = Generator().generate_numbers(total_number=definition["total_random_numbers"], seed=1234, multiplier=33, increment=44, module=99999, precision=2)
    
    queues = []
    for q in definition["queues"]:
        queues.append(SimpleQueue(name=q["name"],
                                  servers=q["servers"],
                                  capacity=q["capacity"],
                                  min_service=q["min_service"],
                                  max_service=q["max_service"],
                                  min_arrival=q["min_arrival"],
                                  max_arrival=q["max_arrival"]))
        
    for d in definition["network"]:
        # TODO: Finalizar parse
        pass
    
    return queues, random_numbers, time_first_event
    