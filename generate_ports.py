import random

# Define the number of lines of data to generate
num_lines = 10

# Define the range of values for each data point
# width_range = (10, 50)
# water_level_range = (3, 20)



class1_width_range = (12, 30)
class1_water_level_range = (8, 15)
class2_width_range = (30, 50)
class2_water_level_range = (15, 25)


ports = []
for i in range(num_lines):
        # Determine the class of the ship
        class_prob = random.random()
        if class_prob < 0.7:
            width_range = class1_width_range
            water_level_range = class1_water_level_range
        else:
            width_range = class2_width_range
            water_level_range = class2_water_level_range      
        # Generate the data for the ship
        width = random.randint(*width_range)
        water_level = random.randint(*water_level_range)
        ports.append([width, water_level])

# Open a file for writing
with open('ports10.txt', 'w') as f:
# Generate the data and write it to the file
    num = 0   
    for i in range(num_lines):
        f.write(f"{num + 1}, {ports[i][0]}, {ports[i][1]}\n")
        num += 1