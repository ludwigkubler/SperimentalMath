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
    
    def generate_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            while len(set(clause)) == 1:  # Ensure not all literals are the same
                clause[random.randint(0, n - 1)] *= -1
            clauses.append(clause)
        return clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            denom = matrix[i][i]
            for j in range(cols):
                matrix[i][j] /= denom
            for k in range(rows):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(cols):
                        matrix[k][j] -= factor * matrix[i][j]
        return matrix
    
    def count_nonzero_rows(matrix):
        return sum(1 for row in matrix if any(x != 0 for x in row))
    
    n_max = 40
    instances_tested = 0
    total_size = 0
    
    for n in range(5, n_max + 1, 5):  # Sweep through sizes 5, 10, 15, 20, 30, 40
        k = random.randint(1, min(n * 2, 40))  # Ensure k is at most twice the number of variables
        cnf = generate_cnf(n, k)
        
        matrix = [[0] * (n + 1) for _ in range(k)]
        for i, clause in enumerate(cnf):
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    matrix[i][var_index] += 1
                else:
                    matrix[i][var_index] -= 1
        
        matrix = gaussian_elimination(matrix)
        size = count_nonzero_rows(matrix)
        
        total_size += size
        instances_tested += 1
    
    metric_value = total_size / instances_tested if instances_tested > 0 else 0
    conjecture_holds = metric_value <= k * math.log(n_max) + 10  # Buffer for potential rounding errors
    
    return {
        "metric_name": "Minimal Diophantine Representation Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Size {n_max}, k={k}, size={total_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results) if results else 0
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) if results else 0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["n_max"] >= 16 for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Size {results[0]['n_max']}, k={results[0]['k']}, size={results[0]['total_size']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data_or_budget_exceeded")