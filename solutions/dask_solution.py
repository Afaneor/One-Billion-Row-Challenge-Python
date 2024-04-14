import time
import dask.dataframe as dd
from logger import logger
from solutions.constants import FILE_PATH


class Solution(object):
    @staticmethod
    def solve():

        # Чтение данных с использованием Dask DataFrame
        df = dd.read_csv(FILE_PATH, sep=';', header=None, names=['Station', 'Temperature'])

        # Агрегация данных по метеостанциям
        aggregated = df.groupby('Station').agg({
            'Temperature': ['mean', 'min', 'max']
        }).compute()  # Производим расчеты

        # Переименование столбцов для удобства
        aggregated.columns = ['Mean', 'Min', 'Max']

        # Округление температур до одного десятичного знака
        aggregated['Mean'] = aggregated['Mean'].round(1)
        aggregated['Min'] = aggregated['Min'].round(1)
        aggregated['Max'] = aggregated['Max'].round(1)

        # Сортировка результатов по названию станции
        aggregated = aggregated.sort_index()

        # Вывод агрегированных данных
        for station, row in aggregated.iterrows():
            print(f"{station}: {row['Mean']}, {row['Min']}, {row['Max']}")


def main():
    logger.info("Starting the solution")
    start = time.time()
    Solution.solve()
    logger.info(f"Solution finished, {time.time() - start:.2f} seconds elapsed")


if __name__ == "__main__":
    main()
