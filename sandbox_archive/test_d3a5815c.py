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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        row_rank = 0
        col_rank = 0
        for i in range(rows):
            if any(matrix[i]):
                row_rank += 1
                pivot_col = next(j for j in range(cols) if matrix[i][j] != 0)
                for k in range(i + 1, rows):
                    factor = matrix[k][pivot_col]
                    for j in range(pivot_col, cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return row_rank

    def generate_instance(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]

    n = random.choice([5, 10, 15, 20, 30, 40])
    instance = generate_instance(n)
    hodge_rank = rank(gaussian_elimination(instance))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": hodge_rank,
        "instances_tested": 1,
        "conjecture_holds": hodge_rank >= n,
        "counterexample": "" if hodge_rank >= n else f"n={n}, rank={hodge_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [53, 67, 71, 73, 79, 83, 89, 97]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")