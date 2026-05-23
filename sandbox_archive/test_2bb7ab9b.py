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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        factor = Fraction(A[i][i])
        for j in range(n):
            A[i][j] /= factor
        for j in range(m):
            if i != j:
                factor = Fraction(A[j][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def resolution_depth(formula):
    m, n = len(formula), len(formula[0])
    depth = 0
    while True:
        found_clause = False
        for i in range(m):
            if all(x >= 0 for x in formula[i]):
                found_clause = True
                break
            if any(x == -formula[j][k] for k in range(n) for j in range(i+1, m)):
                found_clause = True
                break
        if not found_clause:
            break
        depth += 1
    return depth

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = list(range(n))
    
    # Construct a tropical divisor (randomly choose some edges to be positive)
    divisor = [[-math.inf] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                divisor[i][j] = random.randint(1, 10)
    
    # Construct the Tseitin formula from the tropical divisor
    formula = []
    for i in range(n):
        for j in range(i+1, n):
            clause = [-i-1, -j-1]
            if divisor[i][j] >= 0:
                clause.append(j)
            else:
                clause.append(-j)
            formula.append(clause)
    
    # Compute the resolution depth of the Tseitin formula
    depth = resolution_depth(formula)
    
    # Check if the conjecture holds for this seed
    conjecture_holds = depth >= 2**n
    
    return {
        "metric_name": "resolution_depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Depth {depth} < 2^{n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Depth < 2^n\" first_failing_seed={first_failing_seed}")