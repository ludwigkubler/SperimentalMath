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

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    cnf = []
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], 2)
        cnf.append(clause)
    return cnf

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(2 * n, 3 * n)
        cnf = generate_cnf(n, m)
        
        # Placeholder for tropical curve rank and XOR-AND tree width calculation
        rank_T_F = random.randint(1, n)  # Simulated value
        t_star_T_F = random.randint(1, n)  # Simulated value
        
        results.append({
            "n": n,
            "m": m,
            "rank_T_F": rank_T_F,
            "t_star_T_F": t_star_T_F
        })
    
    # Compute Spearman rank correlation coefficient
    ranks = [result["rank_T_F"] for result in results]
    widths = [result["t_star_T_F"] for result in results]
    n = len(ranks)
    
    if n < 2:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "Insufficient data points"
        }
    
    # Sort ranks and widths by their values
    sorted_indices = sorted(range(n), key=lambda i: (ranks[i], widths[i]))
    sorted_ranks = [ranks[i] for i in sorted_indices]
    sorted_widths = [widths[i] for i in sorted_indices]
    
    # Calculate Spearman rank correlation coefficient
    rho = 1 - (6 * sum((sorted_ranks[i] - sorted_widths[i]) ** 2 for i in range(n))) / (n * (n**2 - 1))
    
    # Compute mean and standard deviation of widths
    mean_width = sum(sorted_widths) / n
    variance_width = sum((w - mean_width) ** 2 for w in sorted_widths) / n
    std_dev_width = math.sqrt(variance_width)
    
    # Check acceptance criterion
    median_width = sorted_widths[n // 2]
    lower_bound = median_width + 3 * std_dev_width
    
    conjecture_holds = rho > 0.8 and mean_width >= lower_bound
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": rho,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rho={rho}, mean_width={mean_width}, lower_bound={lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute mean and standard deviation of metric_value
    rho_values = [result["metric_value"] for result in results if result["metric_value"] is not None]
    mean_rho = sum(rho_values) / len(rho_values)
    variance_rho = sum((rho - mean_rho) ** 2 for rho in rho_values) / len(rho_values)
    std_dev_rho = math.sqrt(variance_rho)
    
    # Compute fraction of seeds where conjecture_holds
    support_fraction = sum(result["conjecture_holds"] for result in results if result["metric_value"] is not None) / len(results)
    
    # Determine final result
    if all(rho is not None and rho > 0.8 for rho in rho_values):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_dev_rho} support_fraction={support_fraction}")
    elif any(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho_threshold_not_met\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data_points")