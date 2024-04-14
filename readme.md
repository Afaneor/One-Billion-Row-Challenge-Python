# 1 Billion rows challenge Python

## Задача

Написать скрипт на Python, прочитает файл с миллиардом строк и выведет для каждой метеостанции среднюю температуру, 
наименьшею и наибольшею температуры за все время наблюдений.

Пример файла, который надо прочитать
```
Devi Hosūr;35.5
Taubaté;82.7
Tabūk;-62.1
Agrigento;57.9
Srbobran;-28.6
```
Названия метеостанций могут повторяться, температуры могут быть числа от -99.9 до 99.9.

Результатом должно выводиться наименование метеостанции, средняя температура, наименьшая и наибольшая температура, 
**названия метеостанций должны быть в алфавитном порядке**.

Температуры в результате должны быть округлены до "десятых", например "59.87" -> "59.9"

Например, для файла выше результат будет таким:
```
Agrigento: 57.9, 57.9, 57.9
Devi Hosūr: 35.5, 35.5, 35.5
Srbobran: -28.6, -28.6, -28.6
Tabūk: -62.1, -62.1, -62.1
Taubaté: 82.7, 82.7, 82.7
```

Для генерации файла с миллиардом строк можно использовать скрипт `create_measures.py` из репозитория
```bash
python create_measures.py
```
Это создаст файл `measures.txt` с миллиардом строк.

Для решения необходимо определить метод solve в классе Solution в файле `solution.py`.

Для проверки решения

```bash
python main.py
```

## Требования

1. Скрипт должен быть написан на Python 3.11
2. Разрешается использовать любые доступные библиотеки
3. Скрипт должен быть оформлен в виде публичного репозитория на GitHub
4. Для того, чтобы участвовать форкайте этот репозиторий, это позолит найти все решения в одном месте

## Оценка

Победит самое быстрое решение, которое сможет обработать файл наименьшее время.
Тестовый стенд для всех решений будет одинаковым, на нем точно будет минимум:
- 4 ядра
- 16 Гб оперативной памяти
- SSD диск

## Результаты

| Solution | Time in Seconds | Approach |
| --- | --- | --- |
| [https://github.com/mylittletraf/One-Billion-Row-Challenge-Python/blob/main/main.py](https://github.com/mylittletraf/One-Billion-Row-Challenge-Python/blob/main/main.py) | 614.7 | Чистый питон |
| [https://github.com/gresaggr/One-Billion-Row-Challenge-Python/blob/main/main.py](https://github.com/gresaggr/One-Billion-Row-Challenge-Python/blob/main/main.py) | \- | Чистый питон |
| [https://github.com/ash1k-dev/One-Billion-Row-Challenge-Python/blob/main/solution\_with\_duckdb.py](https://github.com/ash1k-dev/One-Billion-Row-Challenge-Python/blob/main/solution_with_duckdb.py) (duckdb) | 15 | duckdb |
| [https://github.com/ash1k-dev/One-Billion-Row-Challenge-Python/blob/main/solution\_with\_duckdb.py](https://github.com/ash1k-dev/One-Billion-Row-Challenge-Python/blob/main/solution_with_duckdb.py) (dask) | 127 | dask |
| dask\_solution.py | 109 | dask |
| duck\_db\_solution.py | 31 | duck db |
| map\_reduce\_solution.py | 1400\* | multiprocessing |
| numba\_solution.py | 1945\* | numba |
| pandas\_solution.py | 358 | pandas |
| python\_solution.py | 631 | python |

