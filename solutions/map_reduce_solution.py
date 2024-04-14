import time
import multiprocessing
import os
from logger import logger

# Путь к файлу данных
from solutions.constants import FILE_PATH


def find_chunk_boundaries(file_path, num_chunks):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_chunks
    boundaries = [0]

    logger.info(f"Calculating chunk boundaries for the file: {file_path}")

    with open(file_path, 'rb') as f:
        for _ in range(num_chunks - 1):
            f.seek(boundaries[-1] + chunk_size)
            while True:
                byte = f.read(1)
                if byte == b'\n':
                    boundaries.append(f.tell())
                    break
    boundaries.append(file_size)
    logger.info("Chunk boundaries calculated successfully.")
    return boundaries


def process_chunk(start, end, file_path):
    """
    Обрабатывает часть файла на диске от индекса start до индекса end.
    """
    logger.info(f"Starting processing chunk from byte {start} to byte {end}.")
    data = {}
    file_pos = 0
    with open(file_path, 'rb') as file:
        file.seek(start)

        for line in file:
            logger.info(f"Processing bytes {file.tell()}/{end}")
            file_pos += len(line)
            if file_pos > end:
                break
            station, temp = str(line).strip().split(';')
            temp = temp[:-3]
            temp = float(temp)
            if station not in data:
                data[station] = [temp, temp, temp, 1]  # min, max, total, count
            else:
                data[station][0] = min(data[station][0], temp)
                data[station][1] = max(data[station][1], temp)
                data[station][2] += temp
                data[station][3] += 1
    logger.info(f"Finished processing chunk from byte {start} to byte {end}.")
    return data


def reduce_results(results):
    """
    Объединяет результаты обработки от всех процессов.
    """
    logger.info("Starting to reduce results from all processes.")
    final_result = {}
    for sub_result in results:
        for station, values in sub_result.items():
            if station not in final_result:
                final_result[station] = values
            else:
                final_result[station][0] = min(final_result[station][0], values[0])
                final_result[station][1] = max(final_result[station][1], values[1])
                final_result[station][2] += values[2]
                final_result[station][3] += values[3]
    logger.info("All results have been reduced.")
    return final_result


class Solution:
    @staticmethod
    def solve():
        logger.info("Starting multiprocessing solution.")
        num_processes = multiprocessing.cpu_count()
        boundaries = find_chunk_boundaries(FILE_PATH, num_processes)

        pool = multiprocessing.Pool(processes=num_processes)
        tasks = [(boundaries[i], boundaries[i + 1], FILE_PATH) for i in range(num_processes)]
        results = pool.starmap(process_chunk, tasks)
        pool.close()
        pool.join()

        final_results = reduce_results(results)
        for station, values in sorted(final_results.items()):
            mean_temp = values[2] / values[3]
            print(f"{station}: {round(mean_temp, 1)}, {round(values[0], 1)}, {round(values[1], 1)}")
        logger.info("Completed all processing and output.")


def main():
    logger.info("Solution initialization.")
    start = time.time()
    Solution.solve()
    elapsed_time = time.time() - start
    logger.info(f"Solution finished, total elapsed time: {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    main()
