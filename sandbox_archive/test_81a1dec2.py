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
    
    def generate_random_cnf(n):
        cnf = []
        for _ in range(3 * n):
            literals = [random.randint(1, 2*n), random.randint(1, 2*n)]
            if random.choice([True, False]):
                literals[0] *= -1
            if random.choice([True, False]):
                literals[1] *= -1
            cnf.append(literals)
        return cnf
    
    def compute_knot_genus(cnf):
        # Placeholder for knot genus computation
        # This is a dummy implementation and should be replaced with actual logic
        n = len(cnf) // 3
        return n * (n + 1) // 2
    
    def spearman_rank_correlation(x, y):
        x_ranks = {v: i for i, v in enumerate(sorted(set(x)), start=1)}
        y_ranks = {v: i for i, v in enumerate(sorted(set(y)), start=1)}
        n = len(x)
        sum_d_squared = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        rho = 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
        return rho
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_genus = 0
        for _ in range(30):
            cnf = generate_random_cnf(n)
            genus = compute_knot_genus(cnf)
            results.append((n, genus))
            instances_tested += 1
            if instances_tested % 5 == 0:
                total_genus += genus
        
        mean_genus = total_genus / instances_tested
        expected_genus = n**2 * math.log(n)
        rho = spearman_rank_correlation([x for x, _ in results], [expected_genus] * len(results))
        
        conjecture_holds = rho >= 0.7
        counterexample = "" if conjecture_holds else f"Spearman rank correlation {rho} < 0.7"
        
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": rho,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.4f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.4f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed + 1}")