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
    
    # Generate a random knot of size n
    def generate_knot(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    # Compute the tropicalized homology group |HK(tropical)|
    def tropicalized_homology(knot):
        # Simplified model: sum of elements in the knot
        return sum(knot)
    
    # Compute the BP_readtwice circuit size C(K)
    def bp_readtwice_complexity(knot):
        # Simplified model: length of the knot
        return len(knot)
    
    n_values = [5, 10, 15, 20, 30, 40]
    HK_tropical_values = []
    C_K_values = []
    
    for n in n_values:
        knot = generate_knot(n)
        HK_tropical = tropicalized_homology(knot)
        C_K = bp_readtwice_complexity(knot)
        
        if C_K == 0:
            continue
        
        HK_tropical_values.append(HK_tropical)
        C_K_values.append(C_K)
    
    if not HK_tropical_values or not C_K_values:
        return {
            "metric_name": "E[|HK(tropical)|]",
            "metric_value": None,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    # Polynomial fit to estimate E[|HK(tropical)|]
    def polynomial_fit(x, y):
        n = len(x)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        B = [0] * (n + 1)
        
        for i in range(n):
            for j in range(n + 1):
                A[j][i] = x[i] ** j
            B[i] = y[i]
        
        def gaussian_elimination(A, B):
            n = len(B)
            for i in range(n):
                max_row = i
                for k in range(i+1, n):
                    if abs(A[k][i]) > abs(A[max_row][i]):
                        max_row = k
                A[i], A[max_row] = A[max_row], A[i]
                B[i], B[max_row] = B[max_row], B[i]
                
                factor = Fraction(A[i][i], 1)
                for j in range(i, n + 1):
                    A[i][j] /= factor
                B[i] /= factor
                
                for k in range(n):
                    if k != i:
                        factor = Fraction(A[k][i], 1)
                        for j in range(i, n + 1):
                            A[k][j] -= factor * A[i][j]
                        B[k] -= factor * B[i]
            
            return [B[i] / A[i][i] for i in range(n)]
        
        coefficients = gaussian_elimination(A, B)
        return coefficients
    
    coefficients = polynomial_fit(C_K_values, HK_tropical_values)
    
    # Estimate E[|HK(tropical)|] using the fitted polynomial
    def estimate_expected_value(coefficients, C_K):
        n = len(coefficients) - 1
        value = sum(coefficients[i] * (C_K ** i) for i in range(n + 1))
        return value
    
    expected_values = [estimate_expected_value(coefficients, C_K) for C_K in C_K_values]
    
    # Statistical analysis
    mean = sum(expected_values) / len(expected_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in expected_values) / len(expected_values))
    
    return {
        "metric_name": "E[|HK(tropical)|]",
        "metric_value": mean,
        "instances_tested": len(n_values),
        "conjecture_holds": all(abs(mean - value) <= std_dev for value in expected_values),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")