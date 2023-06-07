import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import math

matplotlib.rc("font", family='simsun')
matplotlib.rcParams['axes.unicode_minus']=False

def draw_schedule(initial_depths, schedule, amplitude, period, ships, ports):
    # Set the font size to 16
    font_size = 20

    # ports_index = list(schedule.keys())
    max_time = int(1.1 * max([max(schedule[port.No][:][-1], default=0) for port in ports if len(schedule[port.No]) != 0]))
    fig, ax = plt.subplots(figsize=(10, 5))
    y_ticks = [0]
    hlines = []
    sum_len = 0
    for i, port in enumerate(ports):
        if(i == 0):
            hlines.append(sum_len + ports[i].width/2)
            sum_len += (ports[i].width + ports[i + 1].width)/2
            y_ticks.append(sum_len)
            
            
        elif(i == len(ports) - 1):
            # y_ticks.append(port.width/2)
            continue
        else:
            hlines.append(sum_len + ports[i].width/2)
            sum_len += (port.width + ports[i + 1].width)/2
            y_ticks.append(sum_len)
       
    
    max_interval = max([port.width for port in ports])
    y_ticks = [i/ max_interval * 1.8  for i in y_ticks]
    hlines = [i/ max_interval * 1.8  for i in hlines]
    
    # y_ticks /= min(y_ticks) * 2.5        

    # y_ticks = [0, 2, 7, 12]
    # y_ticks = range(len(ports))
    ax.set_ylim([y_ticks[0] - ports[0].width/2/max_interval * 1.8, y_ticks[-1] + ports[-1].width/2/max_interval * 1.8])
    
    ax.set_yticks(y_ticks)
    
    ax.set_yticklabels([str(port.No) +'/' +str(port.width) for port in ports])
    ax.invert_yaxis()
    # ax.xaxis.grid(True)
    ax.set_xlabel('时间(min)', fontsize=font_size)
    ax.set_ylabel('泊位编号/长度(m)', fontsize=font_size)
    # ax.set_title('Schedule of Ships')
    ax.set_xticks(range(0, max_time, period * 2))
    average_width = sum([port.width for port in ports]) / len(ports)
    min_width = min([port.width for port in ports])
    # widths = [0.5, 1, 2] # list of widths for each bar
    for i, port in enumerate(ports):
        for j in range(len(schedule[port.No])):
            start_time = schedule[port.No][j][1]
            end_time = schedule[port.No][j][2]
            # bar_width = widths[j]
            ship_num = schedule[port.No][j][0]
            barh_width = ships[ship_num - 1].width/ max_interval * 1.8
    
            ax.barh(y_ticks[i], end_time - start_time, left=start_time, height=barh_width, align='center', color='white', alpha=1)
            ax.vlines(x=start_time, ymin=y_ticks[i]-barh_width/2, ymax=y_ticks[i]+barh_width/2, color='black', linewidth=2)
            ax.vlines(x=end_time, ymin=y_ticks[i]-barh_width/2, ymax=y_ticks[i]+barh_width/2, color='black', linewidth=2)
            ax.axhline(xmin=start_time/max_time, xmax=end_time/max_time, y=y_ticks[i]+barh_width/2, color='black', linewidth=2)
            ax.axhline(xmin=start_time/max_time, xmax=end_time/max_time, y=y_ticks[i]-barh_width/2, color='black', linewidth=2)
            
            ax.text(start_time + (end_time - start_time)/2, y_ticks[i], '$S_{'+ str(ship_num) +'}$', ha='center', va='center', color='black',  fontsize=12)
        if(i < len(ports) - 1):
            ax.axhline(y= hlines[i] , color='black', linewidth=2, linestyle='--')

    # Define the function for the water depth at each port over time
    def water_depth(initial_depth, time, amplitude, period):
         initial_depth = 0
         return initial_depth + amplitude *  np.sin(2 * math.pi * time / period)

    time = np.arange(max_time+1)

     # Create a list of water depths for each port over time
    water_depths = [water_depth(depth, time, amplitude, period) for depth in initial_depths]

    im = plt.imshow(water_depths, extent=[0, max_time+1, y_ticks[-1] + ports[-1].width/2/max_interval * 1.8,y_ticks[0] - ports[0].width/2/max_interval * 1.8], cmap='Blues', aspect='auto')
    cbar = fig.colorbar(im)
    cbar.set_label('水深变化(m)', fontsize = 16)
    cbar.ax.tick_params(labelsize=font_size)
    # plt.ylim([y_ticks[0] - ports[0].width/2/max_interval * 1.8, y_ticks[-1] + ports[-1].width/2/max_interval * 1.8])
    plt.xticks(fontsize=font_size)
    plt.yticks(fontsize=font_size)
    plt.tight_layout()
    plt.savefig("../schedule.svg")
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