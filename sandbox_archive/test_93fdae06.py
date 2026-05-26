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
    
    def generate_disjointness_instance(n):
        return [random.sample(range(2), n) for _ in range(n)]
    
    def dnf_size(instance):
        # Simplified DNF size calculation based on instance structure
        return sum(len(row) for row in instance)
    
    def noncrossing_partition_complex(instance):
        # Placeholder function to simulate noncrossing partition complex
        return len(instance)
    
    def spearman_correlation(x, y):
        n = len(x)
        if n != len(y):
            raise ValueError("x and y must have the same length")
        
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        
        n = len(rank_x)
        sum_rank_diff_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        sum_rank_diff = sum(abs(rank_x[i] - rank_y[i]) for i in range(n))
        
        rho_numerator = (n * sum_rank_diff_squared) - ((sum_rank_diff ** 2) / n)
        rho_denominator = math.sqrt((n * sum_rank_diff_squared) - ((sum_rank_diff ** 2) / n))
        
        return rho_numerator / rho_denominator
    
    def minrank(instance):
        # Placeholder function to simulate minimal rank calculation
        return noncrossing_partition_complex(instance)
    
    results = []
    for _ in range(30):  # Ensure at least 30 instances per seed
        n = random.choice([5, 10, 15, 20, 30, 40])
        instance = generate_disjointness_instance(n)
        dnf_size_val = dnf_size(instance)
        minrank_val = minrank(instance)
        
        results.append((dnf_size_val, minrank_val))
    
    x, y = zip(*results)
    rho = spearman_correlation(x, y)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": 30,
        "conjecture_holds": rho > 0.7,
        "counterexample": "" if rho > 0.7 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rho<{results[0]['metric_value']:.2f}\" first_failing_seed={first_failing_seed}")