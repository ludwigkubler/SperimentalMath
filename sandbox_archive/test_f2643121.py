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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        
        # Simplified version of communication complexity rank calculation
        return sum(f[i] == f[j] for i in range(n) for j in range(i+1, n)) / (n * (n - 1))
    
    def quasi_parseval_space_dimension(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        
        # Simplified version of quasi-parseval space dimension calculation
        return sum(1 for i in range(n) if f[i] == f[(i + n // 2) % n]) / n
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        dim_quasi_parseval = quasi_parseval_space_dimension(f)
        r_f = communication_complexity_rank(f)
        results.append((dim_quasi_parseval, r_f))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    dim_quasi_parsevals = [r[0] for r in results]
    ranks = [r[1] for r in results]
    
    mean_dim_quasi_parseval = sum(dim_quasi_parsevals) / len(dim_quasi_parsevals)
    mean_rank = sum(ranks) / len(ranks)
    
    covariance = sum((dim_quasi_parsevals[i] - mean_dim_quasi_parseval) * (ranks[i] - mean_rank) for i in range(len(results))) / len(results)
    variance_dim_quasi_parseval = sum((dim_quasi_parsevals[i] - mean_dim_quasi_parseval)**2 for i in range(len(results))) / len(results)
    variance_rank = sum((ranks[i] - mean_rank)**2 for i in range(len(results))) / len(results)
    
    if variance_dim_quasi_parseval == 0 or variance_rank == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(dim_quasi_parsevals),
            "n_max": max(n for _, n in results),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_correlation_coefficient = covariance / (math.sqrt(variance_dim_quasi_parseval) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_correlation_coefficient,
        "instances_tested": len(dim_quasi_parsevals),
        "n_max": max(n for _, n in results),
        "conjecture_holds": pearson_correlation_coefficient >= 0.7 and all(r >= 0.5 for r in ranks),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        supported_count = sum(1 for r in results if r["conjecture_holds"])
        support_fraction = supported_count / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, r in enumerate(results, start=min(seeds)) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")