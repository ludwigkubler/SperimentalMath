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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, C):
        cnf = []
        for _ in range(C):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                cnf.append(clause)
        return cnf
    
    def density_matrix(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                M[abs(lit)-1][abs(lit)-1] += 1
        return M
    
    def geometric_entanglement(M):
        n = len(M)
        trace = sum(M[i][i] for i in range(n))
        det = determinant(M, n)
        if det == 0:
            return 0
        entanglement = (trace - det) / (n * det)
        return abs(entanglement)
    
    def determinant(matrix, size):
        if size == 1:
            return matrix[0][0]
        det = 0
        for col in range(size):
            submatrix = [row[:col] + row[col+1:] for row in matrix[1:]]
            sign = (-1) ** col
            det += sign * matrix[0][col] * determinant(submatrix, size - 1)
        return det
    
    def clause_set_complexity(cnf):
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    C_values = [random.randint(1, min(n-1, 40)) for _ in range(30)]
    E_values = []
    C_values = []
    
    for n, C in zip(n_values, C_values):
        cnf = generate_cnf(n, C)
        M = density_matrix(cnf)
        E = geometric_entanglement(M)
        E_values.append(E)
        C_values.append(C)
    
    correlation_coefficient = sum((E - mean_E) * (C - mean_C) for E, C in zip(E_values, C_values)) / len(E_values)
    mean_difference = abs(mean_E - mean_C)
    
    return {
        "metric_name": "geometric_entanglement",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8 and mean_difference <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_E = sum(r["metric_value"] for r in results) / len(results)
    std_E = math.sqrt(sum((r["metric_value"] - mean_E) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_E} std={std_E} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_E} std={std_E} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample = "correlation_coefficient=0 or mean_difference>3"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")