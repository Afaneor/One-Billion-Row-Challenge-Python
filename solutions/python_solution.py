from logger import logger
import time
import os
from solutions.constants import FILE_PATH


class Solution(object):
    @staticmethod
    def solve():
        # Словарь для хранения данных метеостанций
        station_data = {}

        # Чтение файла
        with open(FILE_PATH, 'r') as file:
            for line in file:
                station, temp = line.strip().split(';')
                temp = float(temp)

                if station not in station_data:
                    station_data[station] = {
                        'min_temp': temp,
                        'max_temp': temp,
                        'total_temp': temp,
                        'count': 1
                    }
                else:
                    station_data[station]['min_temp'] = min(station_data[station]['min_temp'], temp)
                    station_data[station]['max_temp'] = max(station_data[station]['max_temp'], temp)
                    station_data[station]['total_temp'] += temp
                    station_data[station]['count'] += 1

        # Вывод результатов
        for station in sorted(station_data):
            data = station_data[station]
            avg_temp = data['total_temp'] / data['count']
            print(f"{station}: {round(avg_temp, 1)}, {round(data['min_temp'], 1)}, {round(data['max_temp'], 1)}")


def main():
    logger.info("Starting the solution")
    start = time.time()
    Solution.solve()
    logger.info(f"Solution finished, {time.time() - start} seconds elapsed")


if __name__ == "__main__":
    main()
