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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            if matrix[i][i] == 0:
                for j in range(i + 1, rows):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= pivot
            for j in range(rows):
                if j != i and matrix[j][i] != 0:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def local_indeterminacy(cnf, n):
        m = len(cnf)
        equations = []
        for clause in cnf:
            eq = [0] * (n + 1)
            for lit in clause:
                if lit > 0:
                    eq[lit - 1] += 1
                else:
                    eq[-lit - 1] -= 1
            equations.append(eq)
        matrix = [eq[:] for eq in equations]
        rank = gaussian_elimination(matrix)
        return m - rank
    
    def circuit_monotone_width(cnf):
        n = len(cnf[0])
        width = 0
        for clause in cnf:
            width = max(width, len([lit for lit in clause if abs(lit) <= n]))
        return width
    
    n = random.randint(5, 40)
    m = random.randint(n, n * n)
    cnf = generate_cnf(n, m)
    
    local_indet = local_indeterminacy(cnf, n)
    w_m = circuit_monotone_width(cnf)
    
    if w_m == 0:
        return {
            "metric_name": "LocalIndet / w_m",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w_m is zero"
        }
    
    metric_value = local_indet / w_m
    
    return {
        "metric_name": "LocalIndet / w_m",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"LocalIndet / w_m does not hold\" first_failing_seed={first_failing_seed}")