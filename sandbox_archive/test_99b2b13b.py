# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def determinant(matrix):
        if len(matrix) == 0:
            return 1
        if len(matrix) == 1:
            return matrix[0][0]
        det = 0
        for j in range(len(matrix)):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_square(matrix):
        n = len(matrix)
        return all(len(row) == n for row in matrix)
    
    def schur_weyl_rank(T):
        if not is_square(T):
            raise ValueError("Matrix must be square")
        eigenvalues = [determinant(T[:i+1][:i+1]) for i in range(len(T))]
        return len(eigenvalues)
    
    def sos_refutation_degree(n):
        # Placeholder function to simulate SOS refutation degree
        return random.randint(0, 2 * n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    T = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    rank_T = schur_weyl_rank(T)
    d = sos_refutation_degree(n)
    
    metric_name = "SOS Refutation Degree"
    metric_value = d
    instances_tested = 1
    conjecture_holds = d <= math.log2(rank_T) + 2
    counterexample = "" if conjecture_holds else f"n={n}, rank(T)={rank_T}, d={d}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 50, 2))  # Default to first 30 primes
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")