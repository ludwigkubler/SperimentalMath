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
    
    def projective_representation(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Construct the projective representation
        proj_rep = []
        for i in range(n):
            row = [f[j] ^ f[j + 2**i] for j in range(2**(n-i-1))]
            proj_rep.append(row)
        return proj_rep
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Function length must be a power of 2")
        
        # Calculate the rank of the projective representation
        proj_rep = projective_representation(f)
        rank = 0
        for row in proj_rep:
            if any(row[j] for j in range(len(row))):
                rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            f = generate_boolean_function(n)
            proj_rep = projective_representation(f)
            comm_rank = communication_complexity(f)
            results.append({
                "n": n,
                "proj_rep_size": len(proj_rep),
                "comm_rank": comm_rank
            })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_results"
        }
    
    n_max = max(result["n"] for result in results)
    if n_max < 16:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    proj_rep_sizes = [result["proj_rep_size"] for result in results]
    comm_ranks = [result["comm_rank"] for result in results]
    
    mean_proj_rep_size = sum(proj_rep_sizes) / len(proj_rep_sizes)
    mean_comm_rank = sum(comm_ranks) / len(comm_ranks)
    
    covariance = sum((proj_rep_sizes[i] - mean_proj_rep_size) * (comm_ranks[i] - mean_comm_rank) for i in range(len(results))) / len(results)
    variance_proj_rep_size = sum((proj_rep_sizes[i] - mean_proj_rep_size)**2 for i in range(len(results))) / len(results)
    variance_comm_rank = sum((comm_ranks[i] - mean_comm_rank)**2 for i in range(len(results))) / len(results)
    
    correlation_coefficient = covariance / (math.sqrt(variance_proj_rep_size) * math.sqrt(variance_comm_rank))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"n={result['n']}, proj_rep_size={result['proj_rep_size']}, comm_rank={result['comm_rank']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break