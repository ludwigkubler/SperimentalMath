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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tropicalized_quaternion_algebra(cnf):
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        matrix = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i, lit1 in enumerate(clause):
                for j, lit2 in enumerate(clause):
                    if i != j and abs(lit1) == abs(lit2):
                        matrix[i][j] = 1
        rank = gaussian_elimination(matrix)
        return rank
    
    def gaussian_elimination(matrix):
        n = len(matrix)
        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                    max_row = k
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            if matrix[i][i] == 0:
                continue
            pivot = matrix[i][i]
            for j in range(i, n):
                matrix[i][j] /= pivot
            for k in range(n):
                if k != i and matrix[k][i] != 0:
                    factor = matrix[k][i]
                    for j in range(i, n):
                        matrix[k][j] -= factor * matrix[i][j]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def f(n):
        return int(n ** 1.5)
    
    n_values = [10, 20, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        rank = tropicalized_quaternion_algebra(cnf)
        results.append({"n": n, "rank": rank})
    
    max_rank = max(result["rank"] for result in results)
    conjecture_holds = all(rank <= f(n) for result in results for n in n_values if result["rank"] == max_rank)
    counterexample = "" if conjecture_holds else f"max_rank={max_rank} > f(n) for some n"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_rank > f(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")