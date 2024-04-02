from logger import logger
import time
class Solution(object):
    @staticmethod
    def solve():
        pass


def main():
    logger.info("Starting the solution")
    start = time.time()
    Solution.solve()
    logger.info(f"Solution finished, {time.time() - start:} seconds elapsed")


if __name__ == "__main__":
    main()
