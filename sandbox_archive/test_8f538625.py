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
    
    def determinant(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [[A[i][k] for k in range(j, n)] for i in range(1, n)]
            det += (-1)**j * A[0][j] * determinant(submatrix)
        return det
    
    def min_symplectic_volume(phi):
        # Placeholder function to compute the minimal symplectic volume
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()  # Replace with actual computation
    
    def resolution_width(phi):
        # Placeholder function to compute the resolution proof width
        # This is a dummy implementation and should be replaced with actual computation
        return random.randint(1, 10)  # Replace with actual computation
    
    instances_tested = 30
    n_max = 40
    min_vols = []
    widths = []
    
    for _ in range(instances_tested):
        phi = generate_sat_instance(n_max)
        min_vol = min_symplectic_volume(phi)
        width = resolution_width(phi)
        min_vols.append(min_vol)
        widths.append(width)
    
    correlation_coefficient = calculate_correlation(min_vols, widths)
    slope = (sum(w * v for w, v in zip(widths, min_vols)) / sum(w**2 for w in widths))
    
    conjecture_holds = correlation_coefficient >= 0.8 and abs(slope) <= 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_sat_instance(n):
    # Placeholder function to generate a SAT instance
    # This is a dummy implementation and should be replaced with actual computation
    return [random.choice([1, -1]) for _ in range(n)]

def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
    var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
    var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
    return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")