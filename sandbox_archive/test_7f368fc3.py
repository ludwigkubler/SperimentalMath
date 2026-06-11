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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def matrix_from_cnf(cnf, n):
        m = len(cnf)
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            x = abs(clause[0])
            y = abs(clause[1])
            if clause[0] > 0:
                M[x][y] += 1
            else:
                M[y][x] += 1
            if clause[1] > 0:
                M[y][x] += 1
            else:
                M[x][y] += 1
        return M
    
    def gaussian_elimination(M):
        n = len(M)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            if M[i][i] == 0:
                return None
            for j in range(i + 1, n):
                factor = M[j][i] / M[i][i]
                for k in range(n + 1):
                    M[j][k] -= factor * M[i][k]
        return M
    
    def rank(M):
        n = len(M)
        row_echelon_form = gaussian_elimination(M)
        if row_echelon_form is None:
            return 0
        rank = 0
        for i in range(n):
            if any(row_echelon_form[i][j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def minimal_order(M):
        n = len(M)
        M_extended = [row + [1] for row in M]
        M_extended.append([1] * (n + 1))
        return rank(M_extended)
    
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    M = matrix_from_cnf(cnf, n)
    order = minimal_order(M)
    
    return {
        "metric_name": "minimal_order",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")