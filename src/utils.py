
from typing import List
from generator import Generator
import json
from queue_1 import SimpleQueue
from connector import Connector

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
    
    # Cria a fila de saída
    queues.append(SimpleQueue(name="EXIT",
                              servers=-1,
                              capacity=-1,
                              min_service=-1,
                              max_service=-1,
                              min_arrival=-1,
                              max_arrival=-1))
    
    for q in definition["queues"]:
        queues.append(SimpleQueue(name=q["name"],
                                  servers=q["servers"],
                                  capacity=q["capacity"],
                                  min_service=q["min_service"],
                                  max_service=q["max_service"],
                                  min_arrival=q["min_arrival"],
                                  max_arrival=q["max_arrival"]))
        
    for d in definition["network"]:
        source_name = d["source"]
        target_name = d["target"]
        probability = d["probability"]
        source_queue = find_queue_by_name(source_name, queues)
        target_queue = find_queue_by_name(target_name, queues)
        if source_queue and target_queue:
            connector = Connector(source_queue=source_queue, dest_queue=target_queue, probability=probability)
            source_queue.add_connector(connector)
        else:
            print(f"Fila {source_name} ou {target_name} não encontrada")
    
    return queues, random_numbers, time_first_event
    
def find_queue_by_name(name : str, queues : List[SimpleQueue]):
    for queue in queues:
        if queue.name == name:
            return queue