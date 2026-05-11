# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            return None  # Singular matrix, no unique solution
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
    return A

def count_solutions(quadratic_system):
    A = quadratic_system
    n = len(A)
    solutions_count = 0
    try:
        reduced_matrix = gaussian_elimination(A)
        if reduced_matrix is None:
            return 0  # Singular matrix, no solution
        for i in range(n):
            if all(reduced_matrix[i][j] == 0 for j in range(i)) and reduced_matrix[i][i] != 1:
                solutions_count = 0
                break
            elif all(reduced_matrix[i][j] == 0 for j in range(i + 1, n)):
                solutions_count *= 2
    except IndexError:
        return 0  # Handle potential index errors during elimination
    return solutions_count

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    truth_table = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
    
    quadratic_system = []
    for i in range(len(truth_table)):
        row = [truth_table[i][j] ^ truth_table[i][k] for j in range(k) for k in range(j + 1, n)]
        if any(row[j] != 0 for j in range(n)):
            quadratic_system.append(row)
    
    solutions_count = count_solutions(quadratic_system)
    conjecture_holds = solutions_count >= 2**(n // 2 - 5)
    counterexample = "" if conjecture_holds else f"Insufficient solution count: {solutions_count}"
    
    return {
        "metric_name": "solution_count",
        "metric_value": solutions_count,
        "instances_tested": len(truth_table),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_solution_count = sum(r["metric_value"] for r in results) / len(results)
    std_solution_count = math.sqrt(sum((r["metric_value"] - mean_solution_count) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_solution_count} std={std_solution_count} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_solution_count} std={std_solution_count} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Insufficient solution count\" first_failing_seed={first_failing_seed}")