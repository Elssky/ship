import random
from test import sort_list
from greedy_alg import schedule_ships
import time
import matplotlib.pyplot as plt
import matplotlib
from draw import draw_schedule
import multiprocessing
import concurrent.futures


# Define the data structure of the ship
class Ship:
    def __init__(self, No, arrival_time, stay_time, width, draft):
        self.No = No
        self.arrival_time = arrival_time
        self.stay_time = stay_time
        self.width = width
        self.draft = draft

# Define the data structure of the port
class Port:
    def __init__(self, No, width, water_depth):
        self.No = No
        self.width = width
        self.water_depth = water_depth
        self.available_time = 0

best_waiting_time = 0

def fitness_function(individual):
        global best_waiting_time
        total_waiting_time = 0
        temp_ships = []
        for i in range(len(individual)):
            temp_ships.append(ships[individual[i] - 1])
        waiting_time, total_waiting_time,_, schedule = schedule_ships(ports, temp_ships)
        if total_waiting_time < best_waiting_time:
            best_waiting_time = total_waiting_time
        return total_waiting_time


def read_ships(file_path):
    ships = []
    with open(file_path, 'r') as f:
        for line in f:
            ship_info = line.strip().split(',')
            ship = Ship(int(ship_info[0]), int(ship_info[1]), int(ship_info[2]), int(ship_info[3]), int(ship_info[4]))
            ships.append(ship)
    return ships

def read_ports(file_path):
    ports = []
    with open(file_path, 'r') as f:
        for line in f:
            port_info = line.strip().split(',')
            port = Port(int(port_info[0]), int(port_info[1]), int(port_info[2]))
            ports.append(port)
    return ports


# Define the ships and ports
# ships = [Ship(1, 10, 5, 20, 5), Ship(2, 20, 3, 15, 4), Ship(3, 30, 4, 18, 6)]
# ports = [Port(1, 30, 10), Port(2, 25, 8), Port(3, 20, 6)]

ports = read_ports('ports10.txt')
ships = read_ships('ships45.txt')


if __name__ == '__main__':
   
    for j in range (20):
        print(f"Generation:{j}")
        population = []
        for i in range(200):
            individual = list(range(1, 45 + 1)) 
            random.shuffle(individual)
            # individual = sort_list(individual)
            # print(fitness_function(individual))
            population.append(individual)
        start_time = time.time() # Record the start time
        with multiprocessing.Pool(processes=1) as pool:
            order = pool.map(fitness_function, population)
        population = [x for _, x in sorted(zip(order, population), key=lambda x: x[0])]
        # print(population)
        end_time = time.time() # Record the end time
        elapsed_time = end_time - start_time # Calculate the elapsed time
        print(f"Elapsed time: {elapsed_time} seconds")