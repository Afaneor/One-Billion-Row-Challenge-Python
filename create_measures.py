import os
import sys
import random
import time
from logger import logger

def build_weather_station_name_list():
    """
    Получает имена метеостанций из примера данных в репозитории и удаляет дубликаты
    """
    station_names = []
    with open('weather_stations.csv', 'r', encoding="utf-8") as file:
        file_contents = file.read()
    for station in file_contents.splitlines():
        if "#" in station:
            continue  # Пропускаем строки с комментариями
        station_names.append(station.split(';')[0])
    return list(set(station_names))  # Возвращаем список уникальных названий станций


def convert_bytes(num):
    """
    Преобразует байты в удобочитаемый формат (например, КиБ, МиБ, ГиБ)
    """
    for x in ['bytes', 'KiB', 'MiB', 'GiB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def format_elapsed_time(seconds):
    """
    Форматирует прошедшее время в удобочитаемом формате
    """
    if seconds < 60:
        return f"{seconds:.3f} секунд"
    elif seconds < 3600:
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)} минут {int(seconds)} секунд"
    else:
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if minutes == 0:
            return f"{int(hours)} часов {int(seconds)} секунд"
        else:
            return f"{int(hours)} часов {int(minutes)} минут {int(seconds)} секунд"


def estimate_file_size(weather_station_names, num_rows_to_create):
    """
    Пытается оценить, какого размера будет файл с тестовыми данными
    """
    max_string = float('-inf')
    min_string = float('inf')
    per_record_size = 0

    for station in weather_station_names:
        if len(station) > max_string:
            max_string = len(station)
        if len(station) < min_string:
            min_string = len(station)
        per_record_size = ((max_string + min_string * 2) + len(",-123.4")) / 2

    total_file_size = num_rows_to_create * per_record_size
    human_file_size = convert_bytes(total_file_size)

    return f"Предполагаемый размер файла: {human_file_size}"


def build_test_data(weather_station_names, num_rows_to_create):
    """
    Генерирует и записывает в файл запрошенное количество тестовых данных
    """
    start_time = time.time()
    coldest_temp = -99.9
    hottest_temp = 99.9
    station_names_10k_max = random.choices(weather_station_names, k=10_000)
    batch_size = 10000  # Обработка партии станций перед записью в файл вместо записи по одной строке

    try:
        with open("measurements.txt", 'w', encoding="utf-8") as file:
            for s in range(0, num_rows_to_create // batch_size):
                logger.info(f'пачка {s + 1} из {num_rows_to_create // batch_size}')
                batch = random.choices(station_names_10k_max, k=batch_size)
                prepped_deviated_batch = '\n'.join(
                    [f"{station};{random.uniform(coldest_temp, hottest_temp):.1f}" for station in
                     batch])  # :.1f быстрее, чем round на большом масштабе, потому что round использует математические операции
                file.write(prepped_deviated_batch + '\n')

        sys.stdout.write('\n')
    except Exception as e:
        logger.error(e)
        exit()

    end_time = time.time()
    elapsed_time = end_time - start_time
    file_size = os.path.getsize("measurements.txt")
    human_file_size = convert_bytes(file_size)

    logger.info("Файл успешно записан в data/measurements.txt")
    logger.info(f"Итоговый размер: {human_file_size}")
    logger.info(f"Затраченное время: {format_elapsed_time(elapsed_time)}")


def main():
    num_rows_to_create = 10000000
    weather_station_names = build_weather_station_name_list()
    logger.info(estimate_file_size(weather_station_names, num_rows_to_create))
    build_test_data(weather_station_names, num_rows_to_create)
    logger.info("Тестовый файл завершен.")


if __name__ == "__main__":
    main()
