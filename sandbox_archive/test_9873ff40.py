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
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def hyperplane_arrangement(f):
        n = len(f)
        arrangement = []
        for i in range(n):
            if f[i] == 1:
                arrangement.append([i])
        return arrangement
    
    def log_capacitance(arrangement, p=2):
        n = len(arrangement)
        if n == 0:
            return 0
        sum_log = 0
        for subset in combinations(range(n), n-1):
            product_val = 1
            for i in subset:
                product_val *= (i + 1)
            sum_log += math.log(product_val, p)
        return sum_log / n
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank_var = 0
        for k in range(1, n+1):
            subsets = list(combinations(range(n), k))
            for subset in subsets:
                count_ones = sum(f[i] for i in subset)
                if count_ones == 0 or count_ones == k:
                    continue
                rank_var += (count_ones - k/2)**2 / k
        return rank_var
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_log_cap = 0
        total_rank_var = 0
        
        for _ in range(30):
            f = [random.randint(0, 1) for _ in range(n)]
            arrangement = hyperplane_arrangement(f)
            log_cap = log_capacitance(arrangement)
            rank_var = communication_complexity_rank_variance(f)
            
            if log_cap <= 0 or rank_var <= 0:
                continue
            
            instances_tested += 1
            total_log_cap += log_cap
            total_rank_var += rank_var
        
        if instances_tested == 0:
            continue
        
        mean_log_cap = total_log_cap / instances_tested
        mean_rank_var = total_rank_var / instances_tested
        correlation_coefficient = (instances_tested * mean_log_cap * mean_rank_var - 
                                   total_log_cap * total_rank_var) / (
                                       math.sqrt(instances_tested * 
                                                 (total_log_cap**2 - instances_tested * mean_log_cap**2)) *
                                       math.sqrt(instances_tested * 
                                                 (total_rank_var**2 - instances_tested * mean_rank_var**2)))
        
        results.append({
            "n": n,
            "mean_log_cap": mean_log_cap,
            "mean_rank_var": mean_rank_var,
            "correlation_coefficient": correlation_coefficient
        })
    
    if not results:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_corr_coeff = sum(result["correlation_coefficient"] for result in results) / len(results)
    std_corr_coeff = math.sqrt(sum((result["correlation_coefficient"] - mean_corr_coeff)**2 for result in results) / len(results))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_corr_coeff,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": mean_corr_coeff >= 0.8 and std_corr_coeff <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_corr_coeff = sum(result["metric_value"] for result in results) / len(results)
    std_corr_coeff = math.sqrt(sum((result["metric_value"] - mean_corr_coeff)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr_coeff} std={std_corr_coeff} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient did not meet threshold\" first_failing_seed={first_failing_seed}")