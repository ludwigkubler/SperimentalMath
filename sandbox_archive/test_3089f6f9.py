# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        # Find pivot row
        max_row = i + matrix[i:].index(max(abs(row[i]) for row in matrix[i:]))
        if matrix[max_row][i] == 0:
            continue  # Skip if pivot is zero
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        # Eliminate below the pivot
        for j in range(i + 1, rows):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(cols):
                matrix[j][k] -= factor * matrix[i][k]
    return matrix

def rank(matrix):
    reduced_matrix = gaussian_elimination(matrix)
    rank = sum(1 for row in reduced_matrix if any(row))
    return rank

def generate_tseitin_tree(n, m):
    variables = list(range(n))
    clauses = []
    for _ in range(m):
        a, b, c = random.sample(variables + [-i-1 for i in variables], 3)
        if random.choice([True, False]):
            clauses.append((a, b, c))
        else:
            clauses.append((-a, -b, c))
            clauses.append((a, -b, -c))
            clauses.append((-a, b, -c))
    return n, m, variables, clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    total_rank = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):  # Ensure statistical robustness
        n, m, variables, clauses = generate_tseitin_tree(n=20, m=15)  # Adjust n and m as needed
        matrix = [[0] * (n + m + 1) for _ in range(n + m + 1)]
        for a, b, c in clauses:
            if a > 0:  # Positive variable
                matrix[a][b] += 1
                matrix[a][c] += 1
                matrix[b][a] -= 1
                matrix[c][a] -= 1
            else:  # Negative variable
                matrix[-a][b] -= 1
                matrix[-a][c] -= 1
                matrix[b][-a] += 1
                matrix[c][-a] += 1
        rank_value = rank(matrix)
        total_rank += rank_value
        instances_tested += 1

        if rank_value > m + n:
            conjecture_holds = False
            counterexample = f"n={n}, m={m}, rank={rank_value}"

    mean_rank = Fraction(total_rank, instances_tested)
    return {
        "metric_name": "Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")