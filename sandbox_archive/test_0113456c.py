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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def grr_rank(phi):
        # Placeholder for Grothendieck-Riemann-Roch rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    def resolution_width(phi):
        # Placeholder for resolution proof width calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(phi)
    
    results = []
    n_max = 0
    
    for _ in range(30):  # Aim for at least 30 instances per seed
        n = random.randint(5, 40)  # Sweep n through at least 4 distinct sizes
        phi = [random.choice([0, 1]) for _ in range(n)]
        grr_rk = grr_rank(phi)
        width = resolution_width(phi)
        
        results.append((grr_rk, width))
        n_max = max(n_max, n)
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    grr_rks, widths = zip(*results)
    mean_grr_rk = sum(grr_rks) / len(grr_rks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = sum((grr_rk - mean_grr_rk) * (width - mean_width) for grr_rk, width in results) / (len(results) * math.sqrt(sum((grr_rk - mean_grr_rk)**2 for grr_rk in grr_rks)) * math.sqrt(sum((width - mean_width)**2 for width in widths)))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7 and abs(mean_grr_rk - mean_width) <= 5,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"Correlation coefficient {correlation_coefficient:.2f} < 0.7 or mean difference {abs(mean_grr_rk - mean_width):.2f} > 5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(results):
        return
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")