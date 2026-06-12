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
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = 0
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def variance(lst):
        mean = sum(lst) / len(lst)
        return sum((x - mean) ** 2 for x in lst) / len(lst)
    
    p = 7  # Fixed prime p
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        bits_communicated = []
        for _ in range(30):
            protocol = ''.join(random.choice('01') for _ in range(n))
            bits_communicated.append(protocol.count('1'))
        
        p_adic_expansion = [[int(x) for x in bin(int.from_bytes(bytes.fromhex(hex(p)[2:]), 'big'))[2:].zfill(n)]]
        rank = gaussian_elimination(p_adic_expansion)
        variance_bits = variance(bits_communicated)
        
        results.append({
            "n": n,
            "rank": rank,
            "variance_bits": variance_bits
        })
    
    correlation_coefficient = 0.0
    for i in range(len(n_values)):
        for j in range(i+1, len(n_values)):
            x1, y1 = results[i]["rank"], results[j]["rank"]
            x2, y2 = results[i]["variance_bits"], results[j]["variance_bits"]
            correlation_coefficient += (x1 - x2) * (y1 - y2)
    
    n_max = max(n_values)
    metric_value = correlation_coefficient / len(results)
    conjecture_holds = abs(correlation_coefficient) >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")