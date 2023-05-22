import numpy as np
import matplotlib.pyplot as plt


# # Define the initial water depths for each port
# initial_depths = [10, 8, 12, 9, 11]

# # Define the time range for the simulation
# time = np.linspace(0, 10, 100)

def generate_water_depths(initial_depths, schedule):

    # Define the function for the water depth at each port over time
    def water_depth(initial_depth, time):
        return initial_depth + np.sin(time)

    ports = list(schedule.keys())
    max_time = int(1.1 * max([max(schedule[port][:][-1], default=0) for port in ports if len(schedule[port]) != 0]))
    time = np.linspace(0, max_time, max_time//100).astype(int)
    # Create a list of water depths for each port over time
    water_depths = [water_depth(depth, time) for depth in initial_depths]

    # Create a 2D bar plot of the water depths
    plt.imshow(water_depths, cmap='Blues', aspect='auto')
    plt.colorbar()

    # Set the x-axis labels to the time values
    plt.xticks(np.arange(0, len(time), len(time)//10), time[::len(time)//10])

    # Set the y-axis labels to the port numbers
    plt.yticks(np.arange(len(initial_depths)), np.arange(1, len(initial_depths)+1))

    # Set the plot title and axis labels
    plt.title('Water Depth at Ports Over Time')
    plt.xlabel('Time')
    plt.ylabel('Port Number')

    # Show the plot
    plt.show()

# generate_water_depths(initial_depths, time)