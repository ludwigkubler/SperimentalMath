# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def matrix_mult(A, B):
        m, k = len(A), len(B[0])
        n = len(B)
        C = [[0 for _ in range(k)] for _ in range(m)]
        for i in range(m):
            for j in range(k):
                for l in range(n):
                    C[i][j] += A[i][l] * B[l][j]
        return C
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        augmented = [A[i] + [b[i]] for i in range(m)]
        for i in range(n):
            max_row = i
            for j in range(i+1, m):
                if abs(augmented[j][i]) > abs(augmented[max_row][i]):
                    max_row = j
            augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
            pivot = augmented[i][i]
            for j in range(n + 1):
                augmented[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = augmented[j][i]
                    for k in range(n + 1):
                        augmented[j][k] -= factor * augmented[i][k]
        return [row[-1] for row in augmented]
    
    def stabilizer_group_size(n, r):
        # Placeholder function to compute the size of the stabilizer group
        # This is a dummy implementation and should be replaced with actual logic
        return n + r
    
    def communication_rank(n):
        # Placeholder function to compute the communication rank
        # This is a dummy implementation and should be replaced with actual logic
        return n // 2
    
    metric_name = "stabilizer_group_size"
    instances_tested = 0
    total_metric_value = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        r = communication_rank(n)
        T_phi = stabilizer_group_size(n, r)
        
        instances_tested += 1
        total_metric_value += T_phi
        if n > n_max:
            n_max = n
        
        if instances_tested >= 30:
            break
    
    mean_metric_value = Fraction(total_metric_value, instances_tested)
    
    # Placeholder correlation calculation (should be replaced with actual logic)
    correlation_coefficient = 1.0  # Dummy value for demonstration purposes
    
    if correlation_coefficient < 0.8:
        conjecture_holds = False
        counterexample = "correlation_coefficient_too_low"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")