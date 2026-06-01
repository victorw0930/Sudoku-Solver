#!/usr/bin/env python3

"""Sudoku solver using backtracking search."""

import logging
import sys
import time
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class Solver:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file

    def backtracking_search(self) -> None:
        try:
            with open(self.input_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            logger.error(f"'{self.input_file}' not found.")
            sys.exit(1)
        except PermissionError:
            logger.error(f"Permission denied for '{self.input_file}'.")
            sys.exit(1)
        assignment = [[num for num in line.split() if num != '|'] for line in lines if line[0] != '-']
        
        def bt(assignment: list[list[str]]) -> list[list[str]] | None:
            # complete = True
            # for row in assignment:
            #     if '.' in row:
            #         complete = False
            # if complete:
            #     return assignment

            # found = False
            # for row in assignment:
            #     for num in row:
            #         if num == '.':
            #             pass
            return assignment #TODO

        start_time = time.perf_counter()
        assignment = bt(assignment)
        end_time = time.perf_counter()

        self.time = end_time - start_time

        if assignment is None:
            self.found = False
            return
        else:
            self.found = True

        lines = ""
        for i, row in enumerate(assignment):
            for j, num in enumerate(row):
                lines += num
                if i in [2, 5] and j == 8:
                    lines += "\n------+-------+------\n"
                elif j == 8:
                    lines += "\n"
                elif j in [2, 5]:
                    lines += " | "
                else:
                    lines += " "
        with open(self.output_file, "w", encoding="utf-8") as file:
            file.writelines(lines)


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Sudoku solver.")
    parser.add_argument("input_file", help="Path to puzzle file")
    parser.add_argument("output_file", help="Path to solution file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging activated.")

    logger.info("Application started successfully.")

    solver = Solver(args.input_file, args.output_file)
    solver.backtracking_search()

    if solver.found:
        with open(solver.output_file, "r", encoding="utf-8") as file:
            content = file.read()
        logger.info(f"Solution written to {solver.output_file}:\n{content}")
    else:
        logger.info("Puzzle is over-constrained. No solution found.")

    logger.info(f"Execution time: {solver.time:.6f} seconds")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Execution interrupted by user.")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"Unhandled exception encountered: {e}", exc_info=True)
        sys.exit(1)
