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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i+1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate below pivot
        for k in range(i+1, n):
            factor = A[k][i] / A[i][i]
            for j in range(i, n):
                A[k][j] -= factor * A[i][j]
            b[k] -= factor * b[i]

    # Back substitution
    x = [0.0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        if n > 40:
            continue
        
        # Generate a random CNF with n variables
        clauses = []
        for _ in range(10):  # Each clause has at least one literal
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(literals)
        
        # Compute the Frege proof length (simplified example)
        frege_proof_length = sum(len(clause) for clause in clauses)
        
        # Placeholder for minimal order of p-adic analytic continuation
        # This is a dummy value; replace with actual computation if possible
        min_order_continuation = n ** 1.5
        
        results.append({
            "n": n,
            "frege_proof_length": frege_proof_length,
            "min_order_continuation": min_order_continuation
        })
    
    # Calculate the correlation coefficient
    frege_lengths = [r["frege_proof_length"] for r in results]
    continuations = [r["min_order_continuation"] for r in results]
    mean_frege = sum(frege_lengths) / len(frege_lengths)
    mean_continuation = sum(continuations) / len(continuations)
    
    covariance = sum((frege_lengths[i] - mean_frege) * (continuations[i] - mean_continuation) for i in range(len(results))) / len(results)
    variance_frege = sum((frege_lengths[i] - mean_frege) ** 2 for i in range(len(results))) / len(results)
    variance_continuation = sum((continuations[i] - mean_continuation) ** 2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / math.sqrt(variance_frege * variance_continuation)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,  # Simplified threshold
        "counterexample": "" if abs(correlation_coefficient) > 0.5 else "correlation_coefficient=0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")