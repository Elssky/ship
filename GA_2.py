import random
from test import sort_list
import os.path
from greedy_alg import schedule_ships
import time
import matplotlib.pyplot as plt
import matplotlib
from draw import draw_schedule
import multiprocessing
import concurrent.futures
import itertools
import pickle

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
best_waiting_time_list = []

def fitness_function(individual):
        global best_waiting_time
        total_waiting_time = 0
        sorted_ships =  [ships[i - 1] for i in individual]
        # for i in range(len(individual)):
        #     temp_ships.append(ships[individual[i] - 1])
        waiting_time, total_waiting_time,_, schedule = schedule_ships(ports, sorted_ships)
        if total_waiting_time < best_waiting_time:
            best_waiting_time = total_waiting_time
        return total_waiting_time

def calculate_waiting_time(ships):
    total_waiting_time = 0
    previous_departure_time = 0
    for ship in ships:
        waiting_time = max(0, previous_departure_time - ship.arrival_time)
        ship_start_time = ship.arrival_time + waiting_time
        total_waiting_time += waiting_time
        previous_departure_time = ship_start_time + ship.stay_time
    return total_waiting_time

def calculate_waiting_time_in_one_port(port_schedule, ships):
    ships_in_port = [ships[i[0]-1] for i in port_schedule]
    permutations = itertools.permutations(ships_in_port)
    min_waiting_time = float('inf')
    best_permutation = None
    for perm in permutations:
        waiting_time = calculate_waiting_time(list(perm))
        if waiting_time < min_waiting_time:
            min_waiting_time = waiting_time
            best_permutation = list(perm)
    return best_permutation, min_waiting_time

# Define the genetic algorithm function
def genetic_algorithm(population_size, mutation_rate, max_generations, ships, ports):
    

    def crossover(parent1, parent2):
        child = [-1] * len(parent1)
        start = random.randint(0, len(parent1) - 1)
        end = random.randint(start, len(parent1) - 1)
        child[start:end] = parent1[start:end]
        for i in range(len(parent2)):
            if parent2[i] not in child:
                for j in range(len(child)):
                    if child[j] == -1:
                        child[j] = parent2[i]
                        break
        return child

    def mutation(individual):
        for i in range(len(individual)):
            if random.random() < mutation_rate:
                j = random.randint(0, len(individual) - 1)
                individual[i], individual[j] = individual[j], individual[i]
        return individual

    if os.path.isfile('population.pkl'):
        with open('population.pkl', 'rb') as f:
            population = pickle.load(f)
    else:
    # Initialize the population
        population = []    
        for i in range(population_size):
            individual = list(range(1, len(ships) + 1)) 
            random.shuffle(individual)
            # individual = sort_list(individual)
            # print(fitness_function(individual))
            population.append(individual)
        with open('population.pkl', 'wb') as f:
            pickle.dump(population, f)

    # Evolution
    end_flag = 0
    record_time = 0
    best_individual = []
    for generation in range(max_generations):
        # Parallelize the calculation of the fitness function
        # with multiprocessing.Pool(processes=16) as pool:
        #     order = pool.map(fitness_function, population)

        # population = [x for _, x in sorted(zip(order, population), key=lambda x: x[0])]
        # population = sorted(population, key=lambda x: pool.map(fitness_function, population))
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     # 并行计算每个元素的fitness_function
        #     fitness_values = list(executor.map(fitness_function, population))
        # population = [x for _, x in sorted(zip(fitness_values, population))]
        population = sorted(population, key=lambda x: fitness_function(x))
        if fitness_function(population[0]) == 0:
            return population[0]
        print(f"Generation {generation}: best Total waiting time = {fitness_function(population[0])}")
        best_waiting_time_list.append(fitness_function(population[0]))
        
        if(fitness_function(population[0]) == record_time):
            end_flag += 1
            if(end_flag == 50):
                return record_time
        else:
            end_flag = 0

        record_time = fitness_function(population[0])    

        # if(best_individual != population[0]):
        #     best_individual = population[0]

        #     # Save the corresponding schedule
        #     temp_ships = []
        #     for i in range(len(best_individual)):
        #         temp_ships.append(ships[best_individual[i] - 1])
        #     _, _, _, best_schedule = schedule_ships(ports, temp_ships)
            
        #     time = 0
        #     # print(type(best_schedule))
        #     for i, value in best_schedule.items():
        #         port_schedule = value
        #         # print(f"Port {i}:")
        #         best_permutation, min_waiting_time = calculate_waiting_time_in_one_port(port_schedule, ships)
        #         # print(f"Best permutation: {best_permutation}")
        #         time += min_waiting_time
        #         # print(f"Minimum waiting time: {min_waiting_time}")
        #     print(f"waiting time: {time}")
        new_population = [population[0]]
        
        # new_population = []
        for i in range(0, population_size):
            parent1 = population[random.randint(0, population_size // 2)]
            parent2 = population[random.randint(0, population_size // 2)]
            child = crossover(parent1, parent2)
            child = mutation(child)
            # child = sort_list(child)
            new_population.append(child)
        population = new_population

    best_individual = population[0]

    # Save the corresponding schedule
    temp_ships = []
    for i in range(len(best_individual)):
        temp_ships.append(ships[best_individual[i] - 1])
    _, _, _, best_schedule = schedule_ships(ports, temp_ships)
    
    time = 0
    # print(type(best_schedule))
    for i, value in best_schedule.items():
        port_schedule = value
        # print(f"Port {i}:")
        best_permutation, min_waiting_time = calculate_waiting_time_in_one_port(port_schedule, ships)
        # print(f"Best permutation: {best_permutation}")
        time += min_waiting_time
        # print(f"Minimum waiting time: {min_waiting_time}")
    print(f"waiting time: {time}")

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
            if ship.width <= port.width and ship.draft <= port.water_depth:
                ports_list.append(port.No)
        available_ports.append(ports_list)
    return available_ports 

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
ships = read_ships('ships34.txt')

if __name__ == '__main__':
    

    start_time = time.time() # Record the start time
    # Run the genetic algorithm
    solution = genetic_algorithm(20, 0.04, 100, ships, ports)
    solution_ships = []
    for i in range(len(solution)):
        solution_ships.append(ships[solution[i] - 1])

    waiting_time, total_waiting_time, total_working_time, schedule = schedule_ships(ports, solution_ships)
    print(f"total_waiting_time:{total_waiting_time}" )
    print(f"total_working_time:{total_working_time}" )

    initial_depths = [port.water_depth for port in ports]

    # Define water_level changes
    amplitude = 5
    period = 1440





    end_time = time.time() # Record the end time
    elapsed_time = end_time - start_time # Calculate the elapsed time
    print(f"Elapsed time: {elapsed_time} seconds")

    draw_schedule(initial_depths, schedule,  amplitude, period, ships, ports)

    matplotlib.use('Agg')

    plt.plot(best_waiting_time_list)
    plt.xlabel('Generation')
    plt.ylabel('Best Total Waiting Time')
    plt.title('Genetic Algorithm Performance')
    plt.savefig('best_waiting_time.pdf')
    plt.show()

# # Print the solution
# port_index = 1
# total_waiting_time = 0
# print(f"Port {port_index}:")
# for port in ports:
#     port.available_time = 0
# for i in range(len(solution)):
#     if solution[i] == 0:
#         port_index += 1
#         print(f"Port {port_index}:")
#     else:
#         ship = ships[solution[i] - 1]
#         port = ports[port_index - 1]
#         if port.available_time > ship.arrival_time:
#             waiting_time = port.available_time - ship.arrival_time
#         else: 
#             waiting_time = 0
#         total_waiting_time += waiting_time
#         port.available_time = max(ship.arrival_time, port.available_time) + ship.stay_time
#         # print(f"Ship {ships[solution[i] - 1].No} is assigned to Port {port_index}")
#         print(f" Ship {ships[solution[i] - 1].No}, waiting time {waiting_time}")


# print(f"Total waiting time: {best_waiting_time}")
# print(f"Total waiting time: {total_waiting_time}")