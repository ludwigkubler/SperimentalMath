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
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version for demonstration
        return n
    
    def quasi_parseval_space_dimension(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Simplified version for demonstration
        return n + 1
    
    dimensions = []
    ranks = []
    
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        dim = quasi_parseval_space_dimension(f)
        rank = communication_complexity_rank(f)
        dimensions.append(dim)
        ranks.append(rank)
    
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
    
    covariance = sum((dim - mean_dim) * (rank - mean_rank) for dim, rank in zip(dimensions, ranks))
    variance_dim = sum((dim - mean_dim)**2 for dim in dimensions)
    variance_rank = sum((rank - mean_rank)**2 for rank in ranks)
    
    if variance_dim == 0 or variance_rank == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(dimensions),
            "n_max": max(len(f) for f in [generate_boolean_function(n) for n in range(5, 41)]),
            "conjecture_holds": False,
            "counterexample": "variance_zero"
        }
    
    pearson_coefficient = covariance / (math.sqrt(variance_dim) * math.sqrt(variance_rank))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_coefficient,
        "instances_tested": len(dimensions),
        "n_max": max(len(f) for f in [generate_boolean_function(n) for n in range(5, 41)]),
        "conjecture_holds": pearson_coefficient >= 0.7 and pearson_coefficient < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None]))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(r["conjecture_holds"] for r in results) and all(r["metric_value"] < 0.5 for r in results):
            first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    else:
        print("RESULT: INCONCLUSIVE missing_data")