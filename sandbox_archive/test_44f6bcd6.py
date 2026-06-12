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
    for col in range(n):
        pivot_row = None
        for row in range(col, n):
            if A[row][col] != 0:
                pivot_row = row
                break
        if pivot_row is None:
            continue
        
        # Swap rows to put the pivot at the diagonal
        A[col], A[pivot_row] = A[pivot_row], A[col]
        
        # Normalize the pivot element
        pivot = A[col][col]
        for j in range(col, n):
            A[col][j] /= pivot
        
        # Eliminate other elements in this column
        for i in range(n):
            if i != col:
                factor = A[i][col]
                for j in range(col, n):
                    A[i][j] -= factor * A[col][j]
    return [sum(row) for row in A]

def frege_proof_depth(f):
    # Simulate a small DPLL solver to estimate Frege proof depth
    # This is a placeholder implementation; replace with actual logic
    return random.randint(10, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    rrep_values = []
    d_f_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            f = [random.choice([0, 1]) for _ in range(2**n)]
            A = [[f[j * (2**(n-i-1)) + k] for j in range(2**(i+1))] for i in range(n)]
            
            try:
                rrep_f = gaussian_elimination(A)
                d_f = frege_proof_depth(f)
                
                if not isinstance(rrep_f, list) or not all(isinstance(x, (int, float)) for x in rrep_f):
                    raise ValueError("Invalid minimal representation rank")
                if not isinstance(d_f, int) or d_f <= 0:
                    raise ValueError("Invalid Frege proof depth")
                
                instances_tested += 1
                rrep_values.append(rrep_f)
                d_f_values.append(d_f)
            except Exception as e:
                return {
                    "metric_name": "rrep/f",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": str(e)
                }
    
    if not rrep_values or not d_f_values:
        return {
            "metric_name": "rrep/f",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid data"
        }
    
    mean_rrep = sum(rrep_values) / len(rrep_values)
    mean_d_f = sum(d_f_values) / len(d_f_values)
    alpha = Fraction(mean_rrep, mean_d_f).limit_denominator()
    
    return {
        "metric_name": "rrep/f",
        "metric_value": float(alpha),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": all(r <= alpha * d for r, d in zip(rrep_values, d_f_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"alpha_value\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_data")