from logger import logger
import time
import duckdb

from solutions.constants import FILE_PATH


class Solution(object):
    @staticmethod
    def solve():
        # Путь к файлу данных

        # Создание или подключение к базе данных DuckDB
        con = duckdb.connect(database=':memory:')  # Используем in-memory базу для ускорения

        # Создаем таблицу и загружаем данные из файла
        con.execute(f"CREATE TABLE weather (station VARCHAR, temperature DOUBLE)")
        con.execute(f"COPY weather FROM '{FILE_PATH}' (DELIMITER ';')")

        # Выполнение SQL-запроса для агрегации данных
        result = con.execute("""
            SELECT 
                station,
                ROUND(AVG(temperature), 1) AS mean_temp,
                ROUND(MIN(temperature), 1) AS min_temp,
                ROUND(MAX(temperature), 1) AS max_temp
            FROM weather
            GROUP BY station
            ORDER BY station
        """).fetchdf()

        # Вывод результатов
        for index, row in result.iterrows():
            print(f"{row['station']}: {row['mean_temp']}, {row['min_temp']}, {row['max_temp']}")

        # Закрытие соединения с базой данных
        con.close()


def main():
    logger.info("Starting the solution")
    start = time.time()
    Solution.solve()
    elapsed_time = time.time() - start
    logger.info(f"Solution finished, {elapsed_time} seconds elapsed")


if __name__ == "__main__":
    main()
