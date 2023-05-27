import math
import sys, time
from draw import draw_schedule, draw_schedule_3d
from draw_water import generate_water_depths
from scipy.optimize import minimize_scalar
from pyecharts.charts import Bar
from pyecharts.charts import HeatMap
from pyecharts import options as opts

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



# 目标函数计算水位变化   
def f(x):
    return amplitude * math.sin(2 * math.pi * x / period)

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
        return start_time, end_time, start_time - ship.arrival_time
    else:
        return float('inf')

def is_waterlevel_satisfy(ship, port):

    # Calculate the time when the ship can start to dock
    start_time = max(ship.arrival_time, port.available_time)
    # Calculate the time when the ship can leave the port
    end_time = start_time + ship.stay_time
    # Return the waiting time
    res = minimize_scalar(f, bounds=(start_time, end_time), method='bounded')
    if port.water_depth + res.fun >= ship.draft:
        return True
    else:
        return False

# Define the main function to schedule the ships
def schedule_ships(ports, ships):
    # Alg1: Sort the ships by their arrival time
    # ships.sort(key=lambda x: x.arrival_time)
    # Alg2: Sort the ships by their stay time
    # ships.sort(key=lambda x: x.stay_time)
    # Alg3: Sort the ships by their draft
    # ships.sort(key=lambda x: x.draft, reverse=True)
    
    # Alg4: Sort the ships by their width
    # ships.sort(key=lambda x: x.width, reverse=True)
    # Initialize the waiting time and the total waiting time
    my_waiting_time = [0] * len(ships)
    my_total_waiting_time = 0
    my_total_working_time = 0
    # total_start_time = sys.maxsize
    # total_end_time = 0
    # Repeated calls require initialization ports
    for port in ports:
        port.available_time = 0

    # Initialize the schedule dictionary
    schedule = {port.No: [] for port in ports}
    # Iterate through the ships
    for i, ship in enumerate(ships):
        # Find the first available port that the ship can dock at
        # available_ports = [port for port in ports if port.available_time <= ship.arrival_time]
        available_ports = [port for port in ports if port.width >= ship.width and port.water_depth >= ship.draft]
        available_ports = [port for port in available_ports if is_waterlevel_satisfy(ship, port)]
        if available_ports:
            # Choose the port with the smallest waiting time
            chosen_port = min(available_ports, key=lambda x: x.available_time)
            # Calculate the waiting time of the ship
            start_time, end_time, my_waiting_time[i] = calculate_waiting_time(ship, chosen_port)
            # total_start_time = min(start_time, total_start_time)
            # total_end_time = max(end_time, total_end_time)
            # print(start_time, end_time)
            # print('ship ', ship.No,'->', 'port', chosen_port.No, ' waiting_time: ', my_waiting_time[i])
            #  重复计算
            # Update the total waiting time
            my_total_waiting_time += my_waiting_time[i]
            schedule[chosen_port.No].append([ship.No, start_time, end_time])
            my_total_working_time += end_time - ship.arrival_time
        else:
            # If no available port is found, the ship has to wait
            # print('ship ', ship.No, 'There are no available ports')
            print(ship.No)
            my_waiting_time[i] = float('inf')
  
  
    # Return the waiting time and the total waiting time
    return my_waiting_time, my_total_waiting_time, my_total_working_time, schedule

def schedule_ships_by_staytime(ports, ships, max_iterations):
    # Alg1: Sort the ships by their arrival time
    ships.sort(key=lambda x: x.arrival_time)
    # Initialize the waiting time and the total waiting time
    waiting_time = [0] * len(ships)
    _,total_waiting_time,_,schedule = schedule_ships(ports, ships)
    # total_waiting_time = sys.maxsize
    # Initialize the iteration counter
    iteration = 0
    # Mark how many iterations did not improve total_waiting_time
    end_flag = 0

    total_working_time = 0
    # Iterate until the maximum number of iterations is reached or the result does not improve
    while iteration < max_iterations:
        # Iterate through the ships
        for i in range(len(ships)-1):
            # Check if the stay time of ship i+1 is longer than ship i
            if ships[i+1].stay_time < ships[i].stay_time:
                # Swap the positions of ship i and ship i+1
                ships[i], ships[i+1] = ships[i+1], ships[i]
                # Call the schedule_ships() function recursively to solve
                new_waiting_time, new_total_waiting_time, new_total_working_time, new_schedule = schedule_ships(ports, ships)
                # print("iteration:", iteration, ", waiting time:", new_total_waiting_time)
                # If the total time is shortened, record the relevant configuration information
                if new_total_waiting_time < total_waiting_time:
                    total_waiting_time = new_total_waiting_time
                    total_working_time = new_total_working_time
                    schedule = new_schedule
                    waiting_time = new_waiting_time
                    end_flag = 0
                    # print("waiting time:", new_total_waiting_time)
                # If the result does not improve, terminate the algorithm
                # else:
                #     # ships[i], ships[i+1] = ships[i+1], ships[i]
                #     end_flag += 1
                #     # If continuous 10 iterations did not improve total_waiting_time
                #     if end_flag == 100:
                #         return waiting_time, total_waiting_time, schedule
        # Update the iteration counter
        print("iteration:", iteration, ", waiting time:", new_total_waiting_time)
        iteration += 1
    # Return the waiting time and the total waiting time
    return waiting_time, total_waiting_time, total_working_time, schedule


def draw_waiting_time(ports, ships, waiting_time):
  # Initialize the data for the bar chart
    x_data = [f"Ship {i+1}" for i in range(len(ships))]
    y_data = []
    for i, ship in enumerate(ships):
         y_data.append(waiting_time[i])
    bar_chart = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis("Waiting Time", y_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Ship Waiting Time"))
    )
    # Render the bar chart to an HTML file
    bar_chart.render("ship_waiting_time.html")
    


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
    ports = read_ports('ports10.txt')
    ships = read_ships('ships34.txt')  

    start_time = time.time() # Record the start time
    # print_ships(ships)
    # Schedule the ships and get the waiting time and the total waiting time
    # waiting_time, total_waiting_time, total_working_time, schedule = schedule_ships_by_staytime(ports, ships, 50)
    
    waiting_time, total_waiting_time, total_working_time, schedule = schedule_ships(ports, ships)
    # draw_waiting_time(ports, ships, waiting_time)
    # Print the waiting time and the total waiting time
    # print("Waiting time:", waiting_time)
    #ports = list(schedule.keys())

    initial_depths = [port.water_depth for port in ports]
    print(schedule)

    # schedule = {1: [[3, 73, 840], [25, 840, 1598], [33, 1598, 2127]], 2: [], 3: [[8, 121, 739], [24, 739, 1467], [29, 1467, 2114]], 4: [[22, 291, 641]], 5: [[9, 143, 844]], 6: [[2, 30, 808]], 7: [[10, 144, 611], [19, 611, 984], [27, 984, 1311], [28, 1311, 1715], [31, 1715, 2559]], 8: [[5, 75, 1009], [18, 1009, 2102], [32, 2102, 2900]], 9: [[16, 226, 856], [26, 856, 1574], [30, 1574, 2162]], 10: [[14, 211, 1190], [17, 1190, 2753]]}

    
    initial_depths = {port.No: port.water_depth for port in ports}
    
    # generate_water_depths(initial_depths, schedule)
    # draw_schedule_3d(schedule, initial_depths, amplitude, period)
    # print("Total waiting time:", total_waiting_time)
    print(f"total_waiting_time:{total_waiting_time}" )
    print(f"total_working_time:{total_working_time}" )
    # print(schedule )

    end_time = time.time() # Record the end time
    elapsed_time = end_time - start_time # Calculate the elapsed time
    print(f"Elapsed time: {elapsed_time} seconds")
    ships.sort(key=lambda x: x.arrival_time)
    draw_schedule(initial_depths, schedule,  amplitude, period, ships, ports)
    

# Define water_level changes
amplitude = 5
period = 1440

# Call the main function
if __name__ == '__main__':
    
    
    main()   
   


