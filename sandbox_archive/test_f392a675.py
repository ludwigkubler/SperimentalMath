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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def calculate_entropy(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        p = sum(clauses) / n
        return -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
    
    def min_deg_poly(f):
        n = len(f)
        if n == 1:
            return 1
        
        # Generate a system of linear equations
        A = []
        b = []
        for i in range(2**n):
            row = [f[i]] + [i >> j & 1 for j in range(n)]
            A.append(row)
            b.append(i & 1)
        
        # Gaussian elimination to find the minimal degree polynomial
        rows, cols = len(A), len(A[0])
        for i in range(rows):
            max_row = i
            for k in range(i + 1, rows):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            
            factor = A[i][i]
            for j in range(i, cols):
                A[i][j] /= factor
            b[i] /= factor
            
            for k in range(rows):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, cols):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        
        # Count the number of non-zero coefficients
        min_deg = sum(1 for row in A if any(row[j] != 0 for j in range(n + 1)))
        return min_deg
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_metric_value = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            f = generate_random_boolean_function(n)
            clauses = [i for i, val in enumerate(f) if val == 1]
            entropy = calculate_entropy(clauses)
            min_deg = min_deg_poly(f)
            
            instances_tested += 1
            total_metric_value += min_deg
            max_n = max(max_n, n)
            
            # Check correlation with entropy
            if len(clauses) > 0:
                corr = (min_deg - entropy) / math.sqrt(min_deg**2 + entropy**2)
                if abs(corr) < 0.7:
                    conjecture_holds = False
                    counterexample = f"n={n}, min_deg={min_deg}, Entropy={entropy}"
    
    mean_metric_value = total_metric_value / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in range(instances_tested))) / instances_tested
    
    return {
        "metric_name": "min_deg",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results) or support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")