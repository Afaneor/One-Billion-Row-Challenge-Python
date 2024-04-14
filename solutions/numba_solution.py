import time
import numpy as np
from numba import njit, types
from numba.typed import Dict
from logger import logger

from solutions.constants import FILE_PATH

# Define a Numba-optimized function to process lines
@njit
def process_line(station: str, temp: float, results: Dict):
    if station not in results:
        results[station] = np.array([temp, temp, temp, 1], dtype=np.float64)  # min, max, total, count
    else:
        stats = results[station]
        stats[0] = min(stats[0], temp)
        stats[1] = max(stats[1], temp)
        stats[2] += temp
        stats[3] += 1

# Define a function to compile final results
@njit
def compile_results(results: Dict):
    output = []
    for station in results.keys():
        data = results[station]
        mean_temp = data[2] / data[3]
        output.append((station, round(mean_temp, 1), round(data[0], 1), round(data[1], 1)))
    return output


class Solution:
    @staticmethod
    def solve():
        # Initialize the results dictionary with Numba
        results = Dict.empty(
            key_type=types.unicode_type,
            value_type=types.float64[:]
        )

        # Process each line individually
        with open(FILE_PATH, 'r') as file:
            for line in file:
                station, temp = line.strip().split(';')
                temp = float(temp)
                process_line(station, temp, results)

        # Compile and print the final results
        final_output = compile_results(results)
        for item in final_output:
            print(f"{item[0]}: {item[1]}, {item[2]}, {item[3]}")


def main():
    logger.info("Starting the solution")
    start = time.time()
    Solution.solve()
    elapsed_time = time.time() - start
    logger.info(f"Solution finished, {elapsed_time:.2f} seconds elapsed")


if __name__ == "__main__":
    main()
