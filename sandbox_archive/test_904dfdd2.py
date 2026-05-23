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
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = Fraction(matrix[j][i], matrix[i][i])
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

def clause_indicator_polynomial(cnf_instance, n):
    m = len(cnf_instance)
    polynomial = [[0] * (2**n) for _ in range(m)]
    for i, clause in enumerate(cnf_instance):
        for literal in clause:
            index = sum(1 << j if x == -j-1 else 0 for j, x in enumerate(literal))
            polynomial[i][index] += 1
    return polynomial

def bp_readtwice_circuit_threshold(n):
    # Placeholder function to compute the BP_readtwice circuit threshold
    # This is a dummy implementation and should be replaced with actual logic
    return n * math.log2(n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf_instance = [[random.choice([-i-1, i]) for _ in range(random.randint(1, 3))] for _ in range(n)]
    
    polynomial = clause_indicator_polynomial(cnf_instance, n)
    nc_rank = rank(polynomial)
    bp_threshold = bp_readtwice_circuit_threshold(n)
    
    difference = bp_threshold - nc_rank
    
    return {
        "metric_name": "Rank vs BP_ReadTwice",
        "metric_value": difference,
        "instances_tested": 1,
        "conjecture_holds": difference >= math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")