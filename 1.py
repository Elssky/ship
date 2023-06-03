with open('real_port.txt', 'r+') as file:
    lines = file.readlines()
    file.seek(0)
    for line in lines:
        numbers = line.strip().split(',')
        numbers[1] = str(float(numbers[1]) * 1.2)
        file.write(','.join(numbers) + '\n')
    file.truncate()