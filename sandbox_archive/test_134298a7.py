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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * i for i in range(1, n+1)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll_width(phi):
        # Placeholder function to simulate DPLL proof width computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi) * n
    
    def geometric_entropy(cnf, n):
        # Box counting method for geometric entropy
        box_size = 1.0
        boxes = [[False] * (2**n) for _ in range(2**n)]
        
        for clause in cnf:
            index = sum((2**(i-1) if x > 0 else 0) for i, x in enumerate(clause))
            boxes[index][index] = True
        
        count = 0
        while box_size > 0.01:  # Decrease box size until it's small enough
            new_boxes = [[False] * (2**n) for _ in range(2**n)]
            for i in range(2**n):
                for j in range(2**n):
                    if boxes[i][j]:
                        for di in range(-1, 2):
                            for dj in range(-1, 2):
                                ni = i + di
                                nj = j + dj
                                if 0 <= ni < 2**n and 0 <= nj < 2**n:
                                    new_boxes[ni][nj] = True
            boxes = new_boxes
            count += 1
            box_size /= 2
        
        return math.log(count, 2) / n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        entropy = geometric_entropy(cnf, n)
        width = dpll_width(cnf)
        results.append((entropy, width))
    
    if len(results) < 30:
        return {
            "metric_name": "geometric_entropy_dpll_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    entropies = [r[0] for r in results]
    widths = [r[1] for r in results]
    
    mean_entropy = sum(entropies) / len(entropies)
    mean_width = sum(widths) / len(widths)
    
    var_entropy = sum((e - mean_entropy)**2 for e in entropies) / len(entropies)
    var_width = sum((w - mean_width)**2 for w in widths) / len(widths)
    
    cov_xy = sum((entropies[i] - mean_entropy) * (widths[i] - mean_width) for i in range(len(entropies))) / len(entropies)
    
    if var_entropy == 0 or var_width == 0:
        return {
            "metric_name": "geometric_entropy_dpll_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    correlation_coefficient = cov_xy / math.sqrt(var_entropy * var_width)
    
    return {
        "metric_name": "geometric_entropy_dpll_width",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(cc >= 0.5 for cc in [correlation_coefficient]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_less_than_0.5\" first_failing_seed={first_failing_seed}")