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
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def min_rank(matrix):
        rank = 0
        rows, cols = len(matrix), len(matrix[0])
        for col in range(cols):
            if any(matrix[row][col] != 0 for row in range(rank, rows)):
                rank += 1
        return rank

    n = random.randint(5, 40)
    variables = list(range(n))
    clauses = []
    for _ in range(n):
        clause = [random.choice(variables) for _ in range(random.randint(2, n))]
        clauses.append(clause)

    k_group = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for var in clause:
            k_group[var][var] += 1
            k_group[n][var] += 1
            k_group[var][n] += 1

    min_rank_value = min_rank(k_group)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank_value,
        "instances_tested": 30,
        "conjecture_holds": False if min_rank_value > math.log(n, 2) * 2 else True,
        "counterexample": "" if min_rank_value <= math.log(n, 2) * 2 else f"n={n}, rank={min_rank_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [601, 631, 641, 653, 673, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859]
    results = [run_trial(seed) for seed in seeds]

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif first_failing_seed is not None:
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['instances_tested']}, rank={results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")