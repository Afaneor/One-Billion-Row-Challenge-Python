from logger import logger
import time
import pandas as pd

from solutions.constants import FILE_PATH


class Solution(object):
    @staticmethod
    def solve():
        # Путь к файлу данных

        # Чтение всего файла сразу
        data = pd.read_csv(FILE_PATH, sep=';', header=None, names=['Station', 'Temperature'])

        # Агрегация данных по метеостанциям
        summary = data.groupby('Station').agg({
            'Temperature': ['mean', 'min', 'max']
        })

        # Переименование столбцов
        summary.columns = ['Mean', 'Min', 'Max']
        summary.reset_index(inplace=True)

        # Округление значений температур
        summary['Mean'] = summary['Mean'].round(1)
        summary['Min'] = summary['Min'].round(1)
        summary['Max'] = summary['Max'].round(1)

        # Сортировка данных по названию метеостанций
        summary.sort_values('Station', inplace=True)

        # Вывод результатов
        for index, row in summary.iterrows():
            print(f"{row['Station']}: {row['Mean']}, {row['Min']}, {row['Max']}")


def main():
    logger.info("Starting the solution")
    start = time.time()
    Solution.solve()
    elapsed_time = time.time() - start
    logger.info(f"Solution finished, {elapsed_time} seconds elapsed")


if __name__ == "__main__":
    main()
