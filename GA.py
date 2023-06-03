import random
from test import sort_list
import os.path
from greedy_alg import schedule_ships
import time
import matplotlib.pyplot as plt
import matplotlib
import math
from matplotlib import ticker
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter
from draw import draw_schedule
import multiprocessing
import concurrent.futures
import itertools
import pickle
import sys

# Define the data structure of the ship
class Ship:
    def __init__(self, No, arrival_time, stay_time, width, draft):
        self.No = No
        self.arrival_time = arrival_time
        self.stay_time = stay_time
        self.width = width
        self.draft = draft
        self.priority = 0

# Define the data structure of the port
class Port:
    def __init__(self, No, width, water_depth):
        self.No = No
        self.width = width
        self.water_depth = water_depth
        self.available_time = 0

 

best_waiting_time = sys.maxsize
best_waiting_time_list = []
best_working_time = sys.maxsize


# 目标函数计算水位变化   
def f(x):
    return amplitude * math.sin(2 * math.pi * x / period)

def fitness_function(individual):
        global best_waiting_time
        global best_working_time
        total_waiting_time = 0
        total_working_time = 0
        # sorted_ships = [x for _, x in sorted(zip(individual[0], ships), key=lambda x: x[0])]
        for ship in ships:
            ship.priority = individual[1][ship.No - 1]
        schedule = {port.No: [] for port in ports}


        for i in range(len(individual[1])):
            schedule[individual[1][i]].append(i + 1)
        # print(individual)
        # print(schedule)

        for port_no, port_schedule in schedule.items():
            # print(f'port_no{port_no}')
            waiting_time, working_time = calculate_waiting_time_in_one_port(port_schedule, ships, port_no)
            total_working_time += working_time
            total_waiting_time += waiting_time
        if(best_waiting_time > total_waiting_time):
            best_waiting_time = total_waiting_time
            best_working_time = total_working_time
        return total_waiting_time

def calculate_waiting_time(ships_in, port):
    total_waiting_time = 0
    previous_departure_time = 0
    
    working_time = 0
    for ship in ships_in:
        waiting_time = max(0, previous_departure_time - ship.arrival_time)
        ship_start_time = ship.arrival_time + waiting_time
        while(f(ship_start_time) < ship.draft - port.water_depth):
            # if ship_start_time > 100000:
            #     print("here")
            ship_start_time += 30
        total_waiting_time += waiting_time
        previous_departure_time = ship_start_time + ship.stay_time
        while(f(previous_departure_time) < ship.draft - port.water_depth):
            # if previous_departure_time > 100000:
            #     print("there")
            previous_departure_time += 30
            total_waiting_time += 30
        # working_time += start_time - previous_departure_time
    return total_waiting_time, working_time

def calculate_waiting_time_in_one_port(port_schedule, ships, port_no):
    # print(port_schedule)
    ships_in_port = [ships[i-1] for i in port_schedule]
    ships_in_port = sorted(ships_in_port, key=lambda x:x.priority)
    port = ports[port_no - 1]
    # print(port.No)
    waiting_time, working_time = calculate_waiting_time(ships_in_port, port)
    return waiting_time, working_time



available_ports = []

# Define the genetic algorithm function
def genetic_algorithm(population_size, mutation_rate, max_generations, ships, ports):
    
    global available_ports 
    available_ports = get_available_ports(ports, ships)

    def crossover(parent1, parent2):
        child = [[-1] * len(parent1[0]), [-1] * len(parent1[1])]
        start = random.randint(0, len(parent1[0]) - 1)
        # start = 0
        end = random.randint(start, len(parent1[0]) - 1)
        child[0][start:end] = parent1[0][start:end]
        child[1][start:end] = parent1[1][start:end]
        for i in range(len(child[0])):
            if child[0][i] == -1:
                child[0][i] = parent2[0][i]
                child[1][i] = parent2[1][i]

        return child

    def mutation(individual):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(individual) - 1)
                individual[0][i], individual[0][j] = individual[0][j], individual[0][i]
                individual[1][i] = random.choice(available_ports[i])
        return individual

    def is_individual_valid(individual, available_ports):
        for i in range(len(individual)):
            if(individual[1][i] not in available_ports[i]):
                return False
        return True

    # if os.path.isfile('population1.pkl'):
    #     with open('population1.pkl', 'rb') as f:
    #         population = pickle.load(f)
    # else:

    # Initialize the population  
    population = []    
    for i in range(population_size):
        port_list = []
        ship_list = list(range(1, len(ships) + 1))
        
        for j in ship_list:
            port_list.append(random.choice(available_ports[j - 1]))
        random.shuffle(ship_list)
        
        individual = [ship_list, port_list]
        # print(is_individual_valid(individual, available_ports))
        # individual = sort_list(individual)
        # print(fitness_function(individual))
        population.append(individual)
    # with open('population1.pkl', 'wb') as f:
    #     pickle.dump(population, f)

    
   

    # Evolution
    end_flag = 0
    record_time = 0
    best_individual = []
    for generation in range(max_generations):
        
        # print("before")
        # print(population[0])
        population = sorted(population, key=lambda x: fitness_function(x))
        # for x in population:
        #     print(fitness_function(x))
        # print("after")
        # print(population[0])
        # print(is_individual_valid(population[0], available_ports))
        if fitness_function(population[0]) == 0:
            return population[0]
        print(f"Generation {generation}: best Total waiting time = {fitness_function(population[0])}")
        best_waiting_time_list.append(fitness_function(population[0]))
        
        if(fitness_function(population[0]) == record_time):
            end_flag += 1
            if(end_flag == 100):
                return record_time
        else:
            end_flag = 0

        record_time = fitness_function(population[0])    

        new_population = []
        best_individual = population[0]
        # print("here")
        # print(best_individual)
        # print("new")
        # print(new_population[0])
        for i in range(0, population_size):
            parent1 = population[random.randint(0, population_size // 2)]
            parent2 = population[random.randint(0, population_size // 2)]
            child = crossover(parent1, parent2)
            child = mutation(child)
            # child = sort_list(child)
            new_population.append(child)
        
        population = new_population
        population[0] = best_individual
        # print("finally")
        # print(best_individual)

    


    return population[0]

def get_accommodate_ships(ports, ships):
    accommodate_ships = [] 
    for port in ports:     
        ships_list = []
        for ship in ships:
            if ship.width <= port.width and ship.draft <= port.water_depth:
                ships_list.append(ship.No)

        accommodate_ships.append(ships_list)
    return accommodate_ships 

def get_available_ports(ports, ships):
    available_ports = []
    for ship in ships:
        ports_list = []
        for port in ports:      
            if ship.width <= port.width  and ship.draft <= port.water_depth + amplitude * 0.8:
                ports_list.append(port.No)
        available_ports.append(ports_list)
    return available_ports 


def read_ships(file_path):
    ships = []
    with open(file_path, 'r') as f:
        for line in f:
            ship_info = line.strip().split(',')
            ship = Ship(int(ship_info[0]), int(ship_info[1]), int(ship_info[2]), float(ship_info[3]), float(ship_info[4]))
            ships.append(ship)
    return ships

def read_ports(file_path):
    ports = []
    with open(file_path, 'r') as f:
        for line in f:
            port_info = line.strip().split(',')
            port = Port(int(port_info[0]), float(port_info[1]), float(port_info[2]))
            ports.append(port)
    return ports


# Define the ships and ports
# ships = [Ship(1, 10, 5, 20, 5), Ship(2, 20, 3, 15, 4), Ship(3, 30, 4, 18, 6)]
# ports = [Port(1, 30, 10), Port(2, 25, 8), Port(3, 20, 6)]

# 人工数据集
# ports = read_ports('ports10.txt')
# ships = read_ships('ships34.txt')
#实际数据集
ports = read_ports('real_port.txt')
ships = read_ships('real_ship.txt') 

# Define water_level changes
amplitude = 2
period = 1440

if __name__ == '__main__':
    
    schedule = []
    start_time = time.time() # Record the start time
    # Run the genetic algorithm
    solution = genetic_algorithm(10000, 0.04, 100, ships, ports)

    end_time = time.time() # Record the end time
    elapsed_time = end_time - start_time # Calculate the elapsed time
    print(f"Elapsed time: {elapsed_time} seconds")
    print(f"best_waiting_time:{best_waiting_time}" )
    print(f"best_working_time:{best_working_time}" )
    # solution_ships = []
    schedule = {port.No: [] for port in ports}
    # # Iterate through the ships
    # for i in range(len(solution)):
    #         chosen_port = solution[0][i]
    #         # Calculate the waiting time of the ship
    #         start_time, end_time, my_waiting_time[i] = calculate_waiting_time(ship, chosen_port)

    #         # Update the total waiting time
    #         my_total_waiting_time += my_waiting_time[i]
    #         schedule[chosen_port.No].append([ship.No, start_time, end_time])
    #         my_total_working_time += end_time - ship.arrival_time
    print(solution)
    sorted_ships = [x for _, x in sorted(zip(solution[0], ships), key=lambda x: x[0])]
    schedule = {port.No: [] for port in ports}
    for i in range(len(solution[1])):
        schedule[solution[1][i]].append([i + 1])
    
    for i in schedule.keys():
        for j in range(len(schedule[i])):
            ship = ships[schedule[i][j][0] - 1]
            port = ports[i - 1]
            start_time = max(ship.arrival_time, port.available_time)
                # Calculate the time when the ship can leave the port
            end_time = start_time + ship.stay_time
                # Update the available time of the port
            port.available_time = end_time
            schedule[i][j].append(start_time)
            schedule[i][j].append(end_time)
            if (end_time - start_time != ship.stay_time):
                print(ship.No)
    
    print(schedule)
        

    initial_depths = [port.water_depth for port in ports]

   


    draw_schedule(initial_depths, schedule,  amplitude, period, ships, ports)

    # matplotlib.use('SVG')
    
    plt.rcParams['font.size'] = 16
    

    plt.plot(best_waiting_time_list)
    # plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    plt.xlabel('Generation')
    plt.ylabel('Best Total Waiting Time')
    # plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    # plt.title('Genetic Algorithm Performance')

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True) 
    formatter.set_powerlimits((0,0)) 
    # formatter.set_format('%1.1f')
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%1.1f'))
    plt.gca().yaxis.set_major_formatter(formatter)
   
    

    plt.tight_layout()
    plt.savefig('best_waiting_time88.svg')
    plt.show()

