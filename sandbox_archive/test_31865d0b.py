# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, permutations

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        
        factor = -A_augmented[i][i] / A_augmented[i][i]
        for j in range(i, n+1):
            A_augmented[i][j] *= factor
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j] * x[j] for j in range(i+1, n))) / A_augmented[i][i]
    
    return x

def hodge_order(CNF, n):
    # Placeholder function to compute the minimal order of Hodge classes
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 10)

def dpll_search_tree_width(CNF):
    # Placeholder function to determine the DPLL search tree width
    # This is a dummy implementation and should be replaced with actual logic
    return random.randint(1, 20)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    hord_values = []
    w_dpll_values = []
    
    for n in n_values:
        CNF = [[random.randint(1, n) for _ in range(random.randint(1, n))] for _ in range(n)]
        hord_value = hodge_order(CNF, n)
        w_dpll_value = dpll_search_tree_width(CNF)
        
        hord_values.append(hord_value)
        w_dpll_values.append(w_dpll_value)
    
    correlation_coefficient = sum((hord_values[i] - mean_hord) * (w_dpll_values[i] - mean_w_dpll) for i in range(len(n_values))) / len(n_values)
    mean_hord = sum(hord_values) / len(hord_values)
    mean_w_dpll = sum(w_dpll_values) / len(w_dpll_values)
    mean_abs_diff = sum(abs(hord_values[i] - w_dpll_values[i]) for i in range(len(n_values))) / len(n_values)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or mean_abs_diff > 3"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")