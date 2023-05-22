import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

def draw_schedule(initial_depths, schedule, amplitude, period):

    ports = list(schedule.keys())
    max_time = int(1.1 * max([max(schedule[port][:][-1], default=0) for port in ports if len(schedule[port]) != 0]))
    fig, ax = plt.subplots(figsize=(10, 5))
    y_ticks = range(len(ports))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(ports)
    ax.invert_yaxis()
    ax.xaxis.grid(True)
    ax.set_xlabel('Time')
    ax.set_ylabel('Port Number')
    ax.set_xlim([0, max_time])
   
    for i, port in enumerate(ports):
        for j in range(len(schedule[port])):
            start_time = schedule[port][j][0]
            end_time = schedule[port][j][1]
            ax.barh(i, end_time - start_time, left=start_time, height=0.5, align='center', color='lightslategrey', alpha=0.8)
            ax.vlines(x=start_time, ymin=i-0.25, ymax=i+0.25, color='black', linewidth=2)
            ax.vlines(x=end_time, ymin=i-0.25, ymax=i+0.25, color='black', linewidth=2)
        ax.axhline(y=i+0.5, color='black', linewidth=2)

    # Define the function for the water depth at each port over time
    def water_depth(initial_depth, time, amplitude, period):
         return initial_depth + amplitude *  np.sin(2 * math.pi * time / period)

    time = np.arange(max_time+1)

     # Create a list of water depths for each port over time
    water_depths = [water_depth(depth, time, amplitude, period) for depth in initial_depths]

    plt.imshow(water_depths, cmap='Blues', aspect='auto')
    plt.colorbar()
    
    plt.savefig("../schedule.pdf")
    plt.show()


# schedule = {
#     'Port A': [[0, 5], [8, 12], [18, 20]],
#     'Port B': [[1, 4], [9, 13]],
#     'Port C': [[2, 7], [10, 15], [19, 22]],
#     'Port D': [[6, 11], [14, 17], [21, 23]],
# }





def draw_schedule_3d(schedule, initial_depths, amplitude, period):
    ports = list(initial_depths.keys())
    max_time = max([max(schedule[port][:][-1], default=0) for port in ports if len(schedule[port]) != 0])
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='3d')
    ports = list(schedule.keys())
    x_ticks = np.arange(0, 24, 2)
    y_ticks = np.arange(len(ports))
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.set_xticklabels(x_ticks)
    ax.set_yticklabels(ports)
    ax.invert_yaxis()
    ax.set_xlabel('Time')
    ax.set_ylabel('Port')
    ax.set_zlabel('Water Depth')
    ax.set_xlim([0, 1.1 * max_time])
    ax.set_ylim([len(ports)-1, 0])
    ax.set_zlim([0, 12])

    for i, port in enumerate(ports):
        # water_depth = initial_depths[port] + amplitude * np.sin(np.arange(0, max_time, 0.1) / period)
        # ax.plot(np.arange(0, max_time, 0.1), np.full_like(np.arange(0, max_time, 0.1), i), water_depth, label=port)

        for j in range(len(schedule[port])):
            
            start_time = schedule[port][j][0]
            end_time = schedule[port][j][1]
            ax.plot([start_time, end_time], [i, i], [initial_depths[port], initial_depths[port]], color='steelblue', linewidth=5)

    plt.legend()
    plt.savefig("../schedule_3d.pdf")
    plt.show()

# schedule = {
#     'Port A': [[0, 5], [8, 12], [18, 20]],
#     'Port B': [[1, 4], [9, 13]],
#     'Port C': [[2, 7], [10, 15], [19, 22]],
#     'Port D': [[6, 11], [14, 17], [21, 23]],
# }

# Define initial water depths for each port
# initial_depths = {
#     'Port A': 5,
#     'Port B': 7,
#     'Port C': 4,
#     'Port D': 6
# }

# # Draw 3D schedule
# draw_schedule_3d(schedule, initial_depths)