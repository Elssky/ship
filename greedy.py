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


# Define a function to calculate the waiting time of a ship at a port
def calculate_waiting_time(ship, port):
    # Calculate the water level of the port at the time the ship arrives
    # water_level = port.water_depth + amplitude * math.sin(2 * math.pi * time / period)
    # If the ship can dock at the port immediately, return 0
    if port.width >= ship.width and port.water_depth >= ship.draft:   
        # Calculate the time when the ship can start to dock
        start_time = max(ship.arrival_time, port.available_time)
        # Calculate the time when the ship can leave the port
        end_time = start_time + ship.stay_time
        # Update the available time of the port
        port.available_time = end_time
        # Return the waiting time
        return start_time - ship.arrival_time
    else:
        return float('inf')

# Define the main function to schedule the ships
def schedule_ships(ports, ships):
    # Sort the ships by their arrival time
    ships.sort(key=lambda x: x.arrival_time)
    # Initialize the waiting time and the total waiting time
    waiting_time = [0] * len(ships)
    total_waiting_time = 0
    # Iterate through the ships
    for i, ship in enumerate(ships):
        # Find the first available port that the ship can dock at
        # available_ports = [port for port in ports if port.available_time <= ship.arrival_time]
        available_ports = [port for port in ports if port.width >= ship.width and port.water_depth >= ship.draft]
        if available_ports:
            # Choose the port with the smallest waiting time
            # chosen_port = min(available_ports, key=lambda x: pre_calculate_waiting_time(ship, x))
            chosen_port = min(available_ports, key=lambda x: x.available_time)
            # Calculate the waiting time of the ship
            waiting_time[i] = calculate_waiting_time(ship, chosen_port)
            print('ship ', ship.No,'->', 'port', chosen_port.No, ' waiting_time: ', waiting_time[i])
            #  重复计算
            # Update the total waiting time
            total_waiting_time += waiting_time[i]

        else:
            # If no available port is found, the ship has to wait
            print('ship ', ship.No, 'There are no available ports')
            waiting_time[i] = float('inf')
    # Return the waiting time and the total waiting time
    return waiting_time, total_waiting_time


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


# Define a function to print the ships' information
def print_ships(ships):
    # Sort the ships by their arrival time
    ships.sort(key=lambda x: x.arrival_time)
    # Print the header
    print('{:<10}{:<15}{:<15}{:<10}{:<10}'.format('编号', '到达时间', '停留时间', '宽度', '吃水深度'))
    # Print each ship's information
    for ship in ships:
        print('{:<10}{:<15}{:<15}{:<10}{:<10}'.format(ship.No, ship.arrival_time, ship.stay_time, ship.width, ship.draft))

    # Define the main function to test the correctness of the scheduling function
def main():
    # Define the ports
    # port1 = Port(1, 10, 5)
    # port2 = Port(2, 15, 7)
    # port3 = Port(3, 8, 4)
    # ports = [ port1, port2, port3]
    # Define the ships
    # ship1 = Ship(0, 5, 8, 3)
    # ship2 = Ship(2, 3, 10, 4)
    # ship3 = Ship(4, 4, 12, 5)
    # ships = [ship1, ship2, ship3]

    ports = read_ports('ports.txt')
    ships = read_ships('ships.txt')
    print_ships(ships)
    # Schedule the ships and get the waiting time and the total waiting time
    waiting_time, total_waiting_time = schedule_ships(ports, ships)
    # Print the waiting time and the total waiting time
    print("Waiting time:", waiting_time)
    print("Total waiting time:", total_waiting_time)

# Call the main function
main()