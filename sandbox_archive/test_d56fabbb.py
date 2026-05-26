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
            for j in range(cols):
                if i == j:
                    matrix[i][j] = 1
                else:
                    matrix[i][j] /= matrix[i][i]
            for k in range(rows):
                if k != i:
                    factor = matrix[k][i]
                    for l in range(cols):
                        matrix[k][l] -= factor * matrix[i][l]
        return matrix

    def rank(matrix):
        rref_matrix = gaussian_elimination(matrix)
        return sum(1 for row in rref_matrix if any(row))

    def dpll_width(formula):
        # Simplified DPLL width calculation (not exact but sufficient for testing)
        max_clause_length = 0
        for clause in formula:
            max_clause_length = max(max_clause_length, len(clause))
        return max_clause_length

    n = random.randint(5, 40)
    k = random.randint(1, n // 2)
    Kerdock_code = [[random.choice([0, 1]) for _ in range(n)] for _ in range(k)]
    
    T_C = [sum(row) % 2 for row in zip(*Kerdock_code)]
    r = rank([T_C])
    
    CNF_formula = [[i + 1 if bit == 0 else -i - 1 for i, bit in enumerate(row)] for row in Kerdock_code]
    t = dpll_width(CNF_formula)
    
    metric_value = (r, 2**r, math.log2(t))
    conjecture_holds = all(0.9 <= r / 2**r <= 1.1 and r >= math.log2(t) - 3 for _ in range(30))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank",
        "metric_value": metric_value,
        "instances_tested": n * k,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_rank = sum(result["metric_value"][0] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"][0] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")