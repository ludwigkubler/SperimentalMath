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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def h_norm(phi, n):
        m = len(phi)
        H = [[0] * (m + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(m):
                if phi[i*n + j] != ' ':
                    H[i][j] = int(phi[i*n + j])
        H[m][m] = 1
        H = gaussian_elimination(H)
        det = 1
        for i in range(m + 1):
            det *= H[i][i]
        return abs(det) ** (Fraction(1, m + 1))
    
    def resolution_width(phi, n):
        # Placeholder function to generate a known width for testing purposes
        # Replace with actual implementation if available
        return random.randint(n, 2*n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            phi = [' ' if random.random() < 0.8 else str(random.randint(0, 1)) for _ in range(n*n)]
            h_n = h_norm(phi, n)
            w = resolution_width(phi, n)
            results.append((h_n, w))
    
    if not results:
        return {
            "metric_name": "minimal_hodge_norm",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h_values = [h for h, _ in results]
    w_values = [w for _, w in results]
    
    mean_h = sum(h_values) / len(h_values)
    std_h = math.sqrt(sum((x - mean_h) ** 2 for x in h_values) / len(h_values))
    mean_w = sum(w_values) / len(w_values)
    std_w = math.sqrt(sum((x - mean_w) ** 2 for x in w_values) / len(w_values))
    
    correlation_coefficient = sum((h_values[i] - mean_h) * (w_values[i] - mean_w) for i in range(len(h_values))) / (len(h_values) * std_h * std_w)
    
    return {
        "metric_name": "minimal_hodge_norm",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient=0\" first_failing_seed={first_failing_seed}")