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
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        # Generate a random communication complexity problem instance
        instance = [random.randint(1, n) for _ in range(n)]
        
        # Construct the quandle representation using tropicalization (simplified)
        quandle_rep = [[min(a, b) for b in instance] for a in instance]
        
        # Compute the minimal index of the quandle representation
        min_index = sum(min(row) for row in quandle_rep)
        
        # Compute the communication complexity rank
        comm_complexity_rank = len(set(instance))
        
        results.append({
            "n": n,
            "min_index": min_index,
            "comm_complexity_rank": comm_complexity_rank
        })
    
    if not results:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_indices = [r["min_index"] for r in results]
    comm_complexity_ranks = [r["comm_complexity_rank"] for r in results]
    
    # Compute Pearson correlation coefficient
    n = len(min_indices)
    mean_min_index = sum(min_indices) / n
    mean_comm_complexity_rank = sum(comm_complexity_ranks) / n
    
    cov = sum((min_indices[i] - mean_min_index) * (comm_complexity_ranks[i] - mean_comm_complexity_rank) for i in range(n))
    var_min_index = sum((min_indices[i] - mean_min_index) ** 2 for i in range(n)) / n
    var_comm_complexity_rank = sum((comm_complexity_ranks[i] - mean_comm_complexity_rank) ** 2 for i in range(n)) / n
    
    if var_min_index == 0 or var_comm_complexity_rank == 0:
        return {
            "metric_name": "minimal_index",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearson_corr = cov / (math.sqrt(var_min_index) * math.sqrt(var_comm_complexity_rank))
    
    # Compute mean absolute difference
    mean_abs_diff = sum(abs(min_indices[i] - comm_complexity_ranks[i]) for i in range(n)) / n
    
    return {
        "metric_name": "minimal_index",
        "metric_value": pearson_corr,
        "instances_tested": n,
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": pearson_corr >= 0.8 and mean_abs_diff <= 3,
        "counterexample": "" if pearson_corr >= 0.8 and mean_abs_diff <= 3 else f"pearson_corr={pearson_corr}, mean_abs_diff={mean_abs_diff}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE reason=empty_results")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")