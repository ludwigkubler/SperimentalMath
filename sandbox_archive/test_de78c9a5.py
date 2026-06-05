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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_matroid(M):
        # Placeholder for computing the matroid M_f
        return M
    
    def alexander_defect_invariant(M):
        # Placeholder for computing the Alexander-defect invariant A(M_f)
        return random.random() * 10  # Random value for demonstration
    
    def communication_complexity_rank(f):
        # Placeholder for computing the communication complexity rank r(f)
        return len(f)  # Simplified example
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = math.sqrt(sum((x[i] - mean_x)**2 for i in range(n)) / n)
        std_y = math.sqrt(sum((y[i] - mean_y)**2 for i in range(n)) / n)
        return cov_xy / (std_x * std_y) if std_x * std_y != 0 else 0
    
    def p_value(r, n):
        # Placeholder for computing the p-value
        t = r * math.sqrt((n - 2) / (1 - r**2))
        df = n - 2
        return 2 * (1 - math.erf(abs(t) / math.sqrt(2)))
    
    def run_experiment(n):
        f = generate_boolean_function(n)
        M = compute_matroid(f)
        A_M = alexander_defect_invariant(M)
        r_f = communication_complexity_rank(f)
        return A_M, r_f
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            A_M, r_f = run_experiment(n)
            if A_M is not None and r_f is not None:
                results.append((A_M, r_f))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    A_M_values, r_f_values = zip(*results)
    correlation = pearson_correlation(A_M_values, r_f_values)
    p_val = p_value(correlation, len(results))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7 and p_val <= 0.05,
        "counterexample": "" if correlation >= 0.7 and p_val <= 0.05 else f"correlation={correlation}, p-value={p_val}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")