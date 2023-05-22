import random
from test import sort_list

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

 
# Generate instances of ship and port
ship1 = Ship(1, 10, 5, 20, 5)
port1 = Port(1, 30, 10)
best_waiting_time = float('inf')
 


# Define the genetic algorithm function
def genetic_algorithm(population_size, mutation_rate, max_generations, ships, ports):
    def fitness_function(individual):
        global best_waiting_time
        total_waiting_time = 0
        port_no = 1
        for port in ports:
            port.available_time = 0
        for i in range(len(individual)):
            if individual[i] == 0:
                port_no += 1
                continue
            ship = ships[individual[i] - 1]
            port = ports[port_no - 1]
            # if ship.width > port.width or ship.draft > port.water_depth:
            #     return float('inf')
            if port.available_time > ship.arrival_time:
                total_waiting_time += port.available_time - ship.arrival_time
            port.available_time = max(ship.arrival_time, port.available_time) + ship.stay_time
        if total_waiting_time < best_waiting_time:
            best_waiting_time = total_waiting_time
        return total_waiting_time

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

    # Initialize the population
    population = []    
    accommodate_ships = get_accommodate_ships(ports, ships)
    for i in range(population_size):
        individual = list(range(1, len(ships) + 1)) + [0] * ( len(ports) - 1)
        random.shuffle(individual)
        individual = sort_list(individual)
        population.append(individual)

    # Evolution
    for generation in range(max_generations):
        population = sorted(population, key=lambda x: fitness_function(x))
        if fitness_function(population[0]) == 0:
            return population[0]
        print(f"Generation {generation}: best Total waiting time = {fitness_function(population[0])}")
        new_population = [population[0]]
        # new_population = []
        for i in range(0, population_size):
            parent1 = population[random.randint(0, population_size // 2)]
            parent2 = population[random.randint(0, population_size // 2)]
            child = crossover(parent1, parent2)
            child = mutation(child)
            child = sort_list(child)
            new_population.append(child)
        population = new_population

    return population[0]

def get_accommodate_ships(ports, ships):
    accommodate_ships = []
    for index, port in enumerate(ports):     
        ships_list = []
        for ship in ships:
            if ship.width <= port.width or ship.draft <= port.water_depth:
                ships_list.append(ship.No)
        accommodate_ships.append(ships_list)
    return accommodate_ships 

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


ports = read_ports('ports.txt')
ships = read_ships('ships34.txt')

# Run the genetic algorithm
solution = genetic_algorithm(100, 0.06, 10000, ships, ports)

# Print the solution
port_index = 1
total_waiting_time = 0
print(f"Port {port_index}:")
for port in ports:
    port.available_time = 0
for i in range(len(solution)):
    if solution[i] == 0:
        port_index += 1
        print(f"Port {port_index}:")
    else:
        ship = ships[solution[i] - 1]
        port = ports[port_index - 1]
        if port.available_time > ship.arrival_time:
            waiting_time = port.available_time - ship.arrival_time
        else: 
            waiting_time = 0
        total_waiting_time += waiting_time
        port.available_time = max(ship.arrival_time, port.available_time) + ship.stay_time
        # print(f"Ship {ships[solution[i] - 1].No} is assigned to Port {port_index}")
        print(f" Ship {ships[solution[i] - 1].No}, waiting time {waiting_time}")


print(f"Total waiting time: {best_waiting_time}")
print(f"Total waiting time: {total_waiting_time}")