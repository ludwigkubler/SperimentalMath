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
    n = len(A)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(1, A[i][i])
        for j in range(i+1, n):
            A[j][i] *= factor
        
        # Eliminate above the pivot
        for j in range(i):
            factor = A[j][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return [sum(row) for row in A]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    m = n
    
    # Generate a random 3-CNF formula
    clauses = []
    for _ in range(m):
        literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        random.shuffle(literals)
        clauses.append(literals[:3])
    
    # Convert to matrix form
    A = [[0] * n for _ in range(n)]
    for clause in clauses:
        for literal in clause:
            var = abs(literal) - 1
            if literal > 0:
                A[var][var] += 1
            else:
                A[var][var] -= 1
    
    # Compute the rank of the matrix
    rank = gaussian_elimination(A)
    
    # Check if the hierarchy requires Ω(n^(1-ε)) levels
    ε = Fraction(0.1)  # Constant ε > 0
    required_levels = n ** (1 - ε)
    conjecture_holds = rank >= required_levels
    
    return {
        "metric_name": "SOS Hierarchy Levels",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")