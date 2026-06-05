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
    
    def generate_sat_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def nnf(sat_formula):
        # Convert SAT formula to NNF (simplified version)
        return sat_formula
    
    def lid(phi_nnf):
        # Calculate LID by counting the minimum number of variables needed
        n = len(phi_nnf)
        for k in range(1, n + 1):
            if all(any(phi_nnf[i:i+k] == '0' or phi_nnf[i:i+k] == '1' for i in range(n-k+1)) for _ in range(k)):
                return k
        return n
    
    def ccr(phi):
        # Calculate CCR by constructing a truth table and computing the rank
        n = len(phi)
        truth_table = [[phi[i:i+n].count('0') % 2 == i % 2 for i in range(2**n)] for _ in range(n)]
        rank = 0
        for row in truth_table:
            if any(row[j] != truth_table[0][j] for j in range(len(row))):
                rank += 1
        return rank
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        phi = generate_sat_formula(n)
        phi_nnf = nnf(phi)
        lid_value = lid(phi_nnf)
        ccr_value = ccr(phi)
        results.append((lid_value, ccr_value))
    
    if not results:
        return {
            "metric_name": "Pearson Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    lid_values, ccr_values = zip(*results)
    correlation_coefficient = pearson_correlation(lid_values, ccr_values)
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(len(phi) for phi in results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": "" if correlation_coefficient > 0.7 else "correlation_below_0.7"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")