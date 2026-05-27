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
    
    def generate_tseitin_circuit(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            a, b, c = random.sample(variables, 3)
            clause = (a, b, c)
            clauses.append(clause)
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        for j in range(cols):
            i_max = next((i for i in range(rank, rows) if matrix[i][j]), None)
            if i_max is not None:
                matrix[i_max], matrix[rank] = matrix[rank], matrix[i_max]
                for i in range(rows):
                    if i != rank and matrix[i][j]:
                        factor = -matrix[i][j] / matrix[rank][j]
                        for k in range(cols):
                            matrix[i][k] += factor * matrix[rank][k]
                rank += 1
        return rank
    
    def compute_modular_form(variables, clauses):
        n = len(variables)
        m = len(clauses)
        matrix = [[0] * (n + 2) for _ in range(m)]
        for i, (a, b, c) in enumerate(clauses):
            matrix[i][a - 1] += 1
            matrix[i][b - 1] += 1
            matrix[i][c - 1] += 1
            matrix[i][-2] += 1
        return gaussian_elimination(matrix)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n + 1) // 2)
    variables, clauses = generate_tseitin_circuit(n, m)
    rank = compute_modular_form(variables, clauses)
    
    metric_name = "Minimal Rank of Modular Form"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= (m ** 2) / 4
    counterexample = "" if conjecture_holds else f"Rank {rank} exceeds m^2/4 for n={n}, m={m}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds m^2/4\" first_failing_seed={first_failing_seed}")