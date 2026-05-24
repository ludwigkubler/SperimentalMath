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
    rank = 0
    for i in range(n):
        if A[i][rank] == 0:
            swap_found = False
            for k in range(i+1, n):
                if A[k][rank] != 0:
                    A[i], A[k] = A[k], A[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        factor = Fraction(A[i][rank], A[rank][rank])
        for k in range(rank, n):
            A[i][k] -= factor * A[rank][k]
        rank += 1
    return rank

def characteristic_polynomial(truth_table):
    n = len(truth_table)
    poly = [0] * (n + 1)
    poly[0] = 1
    for i in range(1, n + 1):
        poly[i % n] += truth_table[i - 1]
    return poly

def rank_of_variety(poly, n):
    A = []
    for i in range(n):
        row = [poly[j] * (-1)**(j & (1 << i)) for j in range(n)]
        A.append(row)
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        s = random.randint(1, n)
        truth_table = [random.choice([0, 1]) for _ in range(n)]
        poly = characteristic_polynomial(truth_table)
        rank = rank_of_variety(poly, n)
        g = math.ceil(math.sqrt(s))
        
        results.append({
            "n": n,
            "s": s,
            "g": g,
            "rank": rank
        })
    
    if not results:
        return {
            "metric_name": "R(f)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    R_values = [result["rank"] for result in results]
    s_values = [result["s"] for result in results]
    g_values = [result["g"] for result in results]
    
    mean_R = sum(R_values) / len(R_values)
    std_R = math.sqrt(sum((x - mean_R)**2 for x in R_values) / len(R_values))
    slope = (mean_R * s_values[0]) / g_values[0]**2
    
    correlation_coefficient = sum((R_values[i] - mean_R) * (s_values[i] - mean(s_values)) for i in range(len(R_values))) / (len(R_values) * std_R * math.sqrt(sum((x - mean(s_values))**2 for x in s_values)))
    
    conjecture_holds = correlation_coefficient >= 0.9 and abs(slope - g_values[0]**2 / s_values[0]) <= 0.1 * g_values[0]**2 / s_values[0]
    
    return {
        "metric_name": "R(f)",
        "metric_value": mean_R,
        "instances_tested": len(R_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}, slope={slope}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
    
    results = [run_trial(seed) for seed in seeds]
    R_values = [result["metric_value"] for result in results if result["instances_tested"] > 0]
    support_fraction = sum(result["conjecture_holds"] for result in results if result["instances_tested"] > 0) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(R_values)/len(R_values)} std={math.sqrt(sum((x - sum(R_values)/len(R_values))**2 for x in R_values) / len(R_values))} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")