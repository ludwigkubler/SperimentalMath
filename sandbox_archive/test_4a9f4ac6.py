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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_tropical_generating_series(f):
        n = len(f)
        T = Fraction(1)
        for i in range(n):
            T *= (Fraction(1) + Fraction(1, 2**(i+1)))
        return T
    
    def compute_coxeter_diagram(f):
        n = len(f)
        C = 0
        for i in range(n):
            if f[i] == 1:
                C += 1
        return C
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        x_sorted = sorted(range(n), key=lambda i: x[i])
        y_sorted = sorted(range(n), key=lambda i: y[i])
        rank_x = [x_sorted.index(i) for i in range(n)]
        rank_y = [y_sorted.index(i) for i in range(n)]
        d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        T = compute_tropical_generating_series(f)
        C = compute_coxeter_diagram(f)
        if T <= 0:
            continue
        results.append((C, T**(3/2)))
    
    if not results:
        return {
            "metric_name": "spearman_rank_correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    x, y = zip(*results)
    rho = spearman_rank_correlation(x, y)
    return {
        "metric_name": "spearman_rank_correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": rho >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        rho_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: FALSIFIED counterexample=\"spearman_rank_correlation\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}"
    else:
        rho_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        RESULT = f"RESULT: SUPPORTED mean={sum(rho_values) / len(rho_values):.4f} std={'{:.4f}'.format(math.sqrt(sum((x - (sum(rho_values) / len(rho_values)))**2 for x in rho_values) / len(rho_values))) if rho_values else 'N/A'} support_fraction={support_fraction:.2f}"
    
    print(RESULT)