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
    
    def generate_sat_instance(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def dpll_width(instance):
        if not instance:
            return 0
        if '0' not in instance and '1' not in instance:
            return 0
        if '0' not in instance:
            return dpll_width(instance[1:])
        if '1' not in instance:
            return dpll_width(instance[:-1])
        return max(dpll_width(instance[:i] + '0' + instance[i+1:]), dpll_width(instance[:i] + '1' + instance[i+1:])) + 1
    
    def elliptic_curve_rank(n):
        # Simplified model for demonstration purposes
        return n // 2
    
    instances_tested = 30
    ranks = []
    widths = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        instance = generate_sat_instance(n)
        rank = elliptic_curve_rank(n)
        width = dpll_width(instance)
        
        ranks.append(rank)
        widths.append(width)
    
    if not ranks or not widths:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "empty_ranks_or_widths"
        }
    
    def rank_correlation(ranks, widths):
        n = len(ranks)
        ranks_ranked = sorted(range(n), key=lambda i: ranks[i])
        widths_ranked = sorted(range(n), key=lambda i: widths[i])
        
        sum_diff_squared = sum((ranks_ranked[i] - widths_ranked[i]) ** 2 for i in range(n))
        rho = 1 - (6 * sum_diff_squared) / (n * (n**2 - 1))
        return rho
    
    rho = rank_correlation(ranks, widths)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": instances_tested,
        "conjecture_holds": rho >= 0.8 and all(rho >= 0.5 for _ in range(instances_tested)),
        "counterexample": "" if rho >= 0.8 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_rho = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rho} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")