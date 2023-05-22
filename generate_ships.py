import random
import numpy as np

# Define the number of lines of data to generate
num_lines = 10

# max_width = 0
# max_water_level = 0

# with open('ports.txt', 'r') as f:
#     for line in f:
#         num, width, water_level = map(int, line.strip().split(','))
#         max_width = max(max_width, width)
#         max_water_level = max(max_water_level, water_level)

# # Define the range of values for each data point
# stay_time_range = (60, 1200, 10)

# Define the three classes of ships
class1_width_range = (8, 21)
class1_stay_time_range = (5*60, 15*60)
class1_water_level_range = (3, 7)
class2_width_range = (21, 30)
class2_stay_time_range = (15*60, 30*60)
class2_water_level_range = (8, 13)
class3_width_range = (30, 40)
class3_stay_time_range = (50*60, 65*60)
class3_water_level_range = (14, 20)

ships = []
for i in range(num_lines):
        # Determine the class of the ship
        class_prob = random.random()
        if class_prob < 0.6:
            width_range = class1_width_range
            stay_time_range = class1_stay_time_range
            water_level_range = class1_water_level_range
        elif class_prob < 0.9:
            width_range = class2_width_range
            stay_time_range = class2_stay_time_range
            water_level_range = class2_water_level_range
        else:
            width_range = class3_width_range
            stay_time_range = class3_stay_time_range
            water_level_range = class3_water_level_range
        
        # Generate the data for the ship
        width = random.randint(*width_range)
        stay_time = random.randrange(*stay_time_range)
        water_level = random.randint(*water_level_range)
        start_time = int(np.random.exponential(300))
        ships.append([start_time, stay_time, width, water_level])
ships.sort(key=lambda x: x[0])
# Open a file for writing
with open('ships10.txt', 'w') as f:
    # Generate the data and write it to the file
    num = 0   
    for i in range(num_lines):
        f.write(f"{num + 1}, {ships[i][0]}, {ships[i][1]}, {ships[i][2]}, {ships[i][3]}\n")
        num += 1

# import random
# import numpy as np

# # Define the number of lines of data to generate
# num_lines = 64

# max_width = 0
# max_water_level = 0

# with open('ports.txt', 'r') as f:
#     for line in f:
#         num, width, water_level = map(int, line.strip().split(','))
#         max_width = max(max_width, width)
#         max_water_level = max(water_level, water_level)

# # Define the range of values for each data point
# start_time_range = (0, 1440, 10)
# width_range = (10, max(10, max_width-2))
# stay_time_range = (60, 1200, 10)
# water_level_range = (3, max(3, max_water_level-2))


# # Open a file for writing
# with open('ships64.txt', 'w') as f:
# # Generate the data and write it to the file
#     num = 1
#     start_time = 0
#     avg_interval = 180
#     for i in range(num_lines):
#         # start_time = random.randrange(*start_time_range)
#         # This will generate a random start time that interval follows 
#         # the exponential distribution with a mean of “avg_interval” minutes.
#         start_time += int(np.random.exponential(avg_interval))

#         width = random.randint(*width_range)
#         stay_time = random.randrange(*stay_time_range)
#         water_level = random.randint(*water_level_range)
#         f.write(f"{num}, {start_time}, {stay_time}, {width}, {water_level}\n")
#         num += 1