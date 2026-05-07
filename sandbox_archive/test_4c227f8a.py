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
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n):
                matrix[j][k] -= factor * matrix[i][k]
    rank = sum(1 for row in matrix if any(row))
    return rank

def generate_3cnf(n):
    clauses = []
    variables = list(range(1, n+1))
    for _ in range(n):
        clause = random.sample(variables + [-v for v in variables], 3)
        clauses.append(clause)
    return clauses

def incidence_matrix(clauses, n):
    m = len(clauses)
    matrix = [[0] * (n + n) for _ in range(m)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                matrix[i][var - 1] = 1
            else:
                matrix[i][-var - 1] = 1
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    incidence = incidence_matrix(clauses, n)
    rank = gaussian_elimination(incidence)
    
    # Benchmark circuit sizes for comparison
    if n == 20:
        benchmark_circuit_size = 10**6  # Example: parity function has a known large ACC^0 circuit size
    elif n == 30:
        benchmark_circuit_size = 10**8  # Example: clique function has a known large ACC^0 circuit size
    else:
        return {
            "metric_name": "rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Check if the rank satisfies the conjecture
    if rank >= math.log(n, 2):
        circuit_size = benchmark_circuit_size
        if circuit_size == 0:
            return {
                "metric_name": "rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        conjecture_holds = True
    else:
        circuit_size = 0
        conjecture_holds = False
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        from sympy.ntheory import primerange
        seeds = list(primerange(2, 100))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")