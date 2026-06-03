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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of communication complexity rank calculation
        return sum(f[i] == f[j] for i in range(n) for j in range(i+1, n))
    
    def quasi_parseval_space_dimension(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version of quasi-parseval space dimension calculation
        return sum(1 for i in range(n) if f[i] == f[(i + n // 2) % n])
    
    dimensions = []
    ranks = []
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_boolean_function(n)
        dimensions.append(quasi_parseval_space_dimension(f))
        ranks.append(communication_complexity_rank(f))
    
    if not dimensions or not ranks:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_data"
        }
    
    mean_dim = sum(dimensions) / len(dimensions)
    mean_rank = sum(ranks) / len(ranks)
    numerator = sum((d - mean_dim) * (r - mean_rank) for d, r in zip(dimensions, ranks))
    denominator = math.sqrt(sum((d - mean_dim)**2 for d in dimensions)) * math.sqrt(sum((r - mean_rank)**2 for r in ranks))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(dimensions),
            "n_max": max(n for n, _ in zip([5, 10, 15, 20, 30, 40], [dimensions.count(d) for d in dimensions])),
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation_coefficient = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(dimensions),
        "n_max": max(n for n, _ in zip([5, 10, 15, 20, 30, 40], [dimensions.count(d) for d in dimensions])),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else f"correlation={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE no_data")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_below_0.7\" first_failing_seed={first_failing_seed}")