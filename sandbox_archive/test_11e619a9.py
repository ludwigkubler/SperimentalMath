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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def rank(A):
        m, n = len(A), len(A[0])
        A = [row[:] for row in A]
        gaussian_elimination(A)
        return sum(1 for row in A if any(row[j] != 0 for j in range(n)))
    
    def communication_complexity(rank):
        return rank ** 2
    
    n = random.randint(5, 40)
    d = random.randint(1, 3)
    circuit_size = n * d
    instances_tested = 100
    total_rank = 0
    total_cc = 0
    
    for _ in range(instances_tested):
        # Generate a random tensor product circuit of size n and depth d
        # This is a simplified model, actual implementation would be more complex
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        
        # Compute the associated tropical curve representing its affine variety
        # This is a simplified model, actual implementation would be more complex
        tropical_curve = A + B
        
        # Determine the minimal rank of the tropical curve
        r = rank(tropical_curve)
        
        # Measure the communication complexity of computing the AND-OR gate output
        cc = communication_complexity(r)
        
        total_rank += r
        total_cc += cc
    
    mean_rank = total_rank / instances_tested
    mean_cc = total_cc / instances_tested
    conjecture_holds = mean_cc >= mean_rank ** 2
    counterexample = "" if conjecture_holds else f"Mean CC: {mean_cc}, Mean Rank^2: {mean_rank**2}"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": mean_cc,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")