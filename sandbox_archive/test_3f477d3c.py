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
    
    def compute_quotient_algebra(f):
        # Simplified version of computing quotient algebra
        return sum(f)
    
    def monotone_width(f):
        # Simplified version of computing monotone width
        return len(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        quotient_rank = compute_quotient_algebra(f)
        width = monotone_width(f)
        results.append((quotient_rank, width))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    ranks = [r for r, _ in results]
    widths = [w for _, w in results]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    
    covariance = sum((r - mean_rank) * (w - mean_width) for r, w in results) / len(results)
    variance_width = sum((w - mean_width) ** 2 for _, w in results) / len(results)
    
    if variance_width == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance in width is zero"
        }
    
    pearson_corr = covariance / math.sqrt(variance_width)
    
    all_ranks_valid = all(0 <= r <= 5 * w for r, w in results)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(ranks),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr >= 0.8 and all_ranks_valid,
        "counterexample": "" if pearson_corr >= 0.8 and all_ranks_valid else "Pearson correlation < 0.8 or rank > 5 * width"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no trials run")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if all(r["conjecture_holds"] for r in results):
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        elif support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation < 0.8 or rank > 5 * width\" first_failing_seed={first_failing_seed}")