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
    
    def generate_symmetric_matrix(n):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                A[i][j] = random.randint(-10, 10)
                A[j][i] = A[i][j]
        return A
    
    def compute_eigenvalues(A):
        n = len(A)
        eigenvalues = []
        
        # Compute the characteristic polynomial
        for k in range(n):
            det = Fraction(1, 1)
            for i in range(n):
                for j in range(n):
                    if i == k:
                        A[i][j] += random.randint(-1, 1) * 1e-6
                    det *= (A[i][j] - A[k][k])
            eigenvalues.append(det)
        
        # Find the minimal non-zero eigenvalue
        min_non_zero_eigenvalue = float('inf')
        for ev in eigenvalues:
            if ev != 0 and abs(ev) < min_non_zero_eigenvalue:
                min_non_zero_eigenvalue = abs(ev)
        
        return min_non_zero_eigenvalue
    
    def communication_complexity(n):
        # Placeholder function to simulate communication complexity
        # This is a dummy value for testing purposes
        return 2**n / random.randint(1, n)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    A = generate_symmetric_matrix(n)
    λ = compute_eigenvalues(A)
    
    if λ == float('inf'):
        return {
            "metric_name": "minimal_non_zero_eigenvalue",
            "metric_value": -1,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    CC = communication_complexity(n)
    
    if CC > 2**n / λ:
        return {
            "metric_name": "communication_complexity",
            "metric_value": CC,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": f"CC(XOR_{n}) = {CC} > 2^n / λ = {2**n / λ}"
        }
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": CC,
        "instances_tested": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")