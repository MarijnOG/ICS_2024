from ast import literal_eval
import numpy as np


def hamming_distance(str1: str, str2: str):
    # Convert binary strings to NumPy arrays of integers
    arr1 = np.array(list(map(int, str1)))
    arr2 = np.array(list(map(int, str2)))

    # Calculate Hamming distance using XOR and sum
    distance = np.sum(arr1 != arr2)

    return distance

def hamming_list(list: list):
    distances = []
    for i in list:
        for j in list:
            distances.append(hamming_distance(i, j))

    distances.sort()
    return distances[len(list):]

data = {}
strategies = []

with open("data_100.txt") as f:
    for line in f:
        print(line)
        if not line.strip():
            break

        key, value = line.strip().split(": ")
        data[key] = literal_eval(value)

    for line in f:
        line.strip().split(": ")
        strategies.append(line[19:].strip())


distances = hamming_list(strategies)
print(len(distances))

binary_array = np.array([list(map(int, code)) for code in strategies])

# Count the number of 1s and 0s using NumPy
num_ones = np.sum(binary_array, axis=1)
num_zeros = len(binary_array[0]) - num_ones


# Display the results
print(int(strategies[0]))
print("Number of 1s:", num_ones)
print("Number of 0s:", num_zeros)