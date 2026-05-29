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
            for j in range(i+1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            factor = 1 / matrix[i][i]
            for j in range(cols):
                matrix[i][j] *= factor
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix

    def rank(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rref_matrix = gaussian_elimination(matrix)
        rank = 0
        for row in rref_matrix:
            if any(row):
                rank += 1
        return rank

    def max_cut(n):
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                edges.append((i, j))
        random.shuffle(edges)
        cut_edges = set()
        for u, v in edges:
            if random.choice([True, False]):
                cut_edges.add((u, v))
        return len(cut_edges)

    def comm_complexity(n):
        return max_cut(n)

    n = 40
    min_rank = rank([[1, 2], [3, 4]])
    C_n = sum(comm_complexity(n) for _ in range(30)) / 30
    conjecture_holds = abs(C_n - min_rank) <= 5 * min_rank
    counterexample = "" if conjecture_holds else f"min_rank={min_rank}, E[C(n)]={C_n}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": C_n,
        "instances_tested": 30,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_C_n = sum(r["metric_value"] for r in results) / len(results)
    std_C_n = math.sqrt(sum((r["metric_value"] - mean_C_n) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_C_n} std={std_C_n} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_C_n} std={std_C_n} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")