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
        assignment = [[val for val in line.split() if val != "|"] for line in lines if line[0] != "-"]

        vars = []
        for i, row in enumerate(assignment):
            for j, val in enumerate(row):
                if val == ".":
                    vars.append((i, j))

        vars_idx = 0

        constraints = [[0 for j in range(9)] for i in range(3)]
        for i, row in enumerate(assignment):
            for j, val in enumerate(row):
                if val != ".":
                    constraints[0][i] |= 1 << int(val) - 1
                    constraints[1][j] |= 1 << int(val) - 1
                    constraints[2][i // 3 * 3 + j // 3] |= 1 << int(val) - 1

        domains = [[0 for j in range(9)] for i in range(9)]
        for i, row in enumerate(assignment):
            for j, val in enumerate(row):
                if val == ".":
                    domains[i][j] = constraints[0][i] | constraints[1][j] | constraints[2][i // 3 * 3 + j // 3]
                else:
                    domains[i][j] = (1 << 9) - 1

        def bts(assignment: list[list[str]],
                vars: list[tuple[int, int]],
                vars_idx: int,
                constraints: list[list[int]]) -> list[list[str]] | None:
            if vars_idx == len(vars):
                return assignment

            row = vars[vars_idx][0]
            col = vars[vars_idx][1]

            for val in range(9):
                if not (constraints[0][row] >> val & 1 or
                        constraints[1][col] >> val & 1 or
                        constraints[2][row // 3 * 3 + col // 3] >> val & 1):
                    assignment[row][col] = str(val + 1)
                    constraints[0][row] |= 1 << val
                    constraints[1][col] |= 1 << val
                    constraints[2][row // 3 * 3 + col // 3] |= 1 << val
                    result = bts(assignment, vars, vars_idx + 1, constraints)
                    if result is not None:
                        return result
                    constraints[0][row] &= ~(1 << val)
                    constraints[1][col] &= ~(1 << val)
                    constraints[2][row // 3 * 3 + col // 3] &= ~(1 << val)

        start_time = time.perf_counter()
        result = bts(assignment, vars, vars_idx, constraints)
        end_time = time.perf_counter()

        self.time = end_time - start_time

        if result is None:
            self.found = False
            return
        else:
            self.found = True

        content = ""
        for i, row in enumerate(result):
            for j, val in enumerate(row):
                content += val
                if i in [2, 5] and j == 8:
                    content += "\n------+-------+------\n"
                elif j == 8:
                    content += "\n"
                elif j in [2, 5]:
                    content += " | "
                else:
                    content += " "
        with open(self.output_file, "w", encoding="utf-8") as file:
            file.write(content)


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
        logger.info("No solution found. Over-constrained puzzle.")

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
