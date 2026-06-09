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
    
    # Generate an instance φ of a language L in NP (e.g., a boolean formula)
    n = 10  # Number of variables
    clauses = [random.sample(range(n), 2) for _ in range(5)]  # Example: 5 clauses with 2 literals each
    
    # Construct the Cayley graph of φ
    generators = []
    for clause in clauses:
        generators.append((clause[0], 1))
        generators.append((clause[1], -1))
    
    # Calculate the minimum number of generators g(L)
    g_L = len(set(generators))
    
    # Calculate the maximum order of an element in the Cayley graph
    max_order = 2 ** n
    
    # Measure the communication complexity rank r(φ)
    # For simplicity, assume r(φ) is proportional to the number of clauses
    r_phi = len(clauses)
    
    # Compute the correlation coefficient between g(L) and r(φ)
    if r_phi == 0:
        corr_g_r = 0
    else:
        mean_g_L = g_L
        mean_r_phi = r_phi
        sum_diffs_g_L = sum((g - mean_g_L) ** 2 for g in [g_L] * 10)
        sum_diffs_r_phi = sum((r - mean_r_phi) ** 2 for r in [r_phi] * 10)
        corr_g_r = (sum((g - mean_g_L) * (r - mean_r_phi) for g, r in zip([g_L] * 10, [r_phi] * 10)) / math.sqrt(sum_diffs_g_L * sum_diffs_r_phi))
    
    # Compute the mean difference between o(φ) and r(φ)
    mean_diff_o_r = abs(max_order - r_phi)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": corr_g_r,
        "instances_tested": 10,
        "n_max": n,
        "conjecture_holds": corr_g_r >= 0.7 and mean_diff_o_r <= 2,
        "counterexample": "" if corr_g_r >= 0.7 and mean_diff_o_r <= 2 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr_g_r = sum(result["metric_value"] for result in results) / len(results)
    std_corr_g_r = math.sqrt(sum((result["metric_value"] - mean_corr_g_r) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_g_r:.4f} std={std_corr_g_r:.4f} support_fraction={support_fraction:.2f}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")