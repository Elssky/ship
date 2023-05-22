import random

# Define the number of lines of data to generate
num_lines = 3

# Define the range of values for each data point
width_range = (10, 50)
water_level_range = (3, 20)

# Open a file for writing
with open('ports.txt', 'w') as f:
# Generate the data and write it to the file
    num = 1
    for i in range(num_lines):
        width = random.randint(*width_range)
        water_level = random.randint(*water_level_range)
        f.write(f"{num}, {width}, {water_level}\n")
        num += 1
