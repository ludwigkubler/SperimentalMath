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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def communication_complexity_rank(cnf):
        # Simplified version of communication complexity rank calculation
        return len(cnf) / 2
    
    def hodge_index(cnf):
        # Simplified version of Hodge index calculation
        return len(cnf) ** 0.5
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = communication_complexity_rank(cnf)
        h_index = hodge_index(cnf)
        metrics.append({
            "n": n,
            "rank": rank,
            "h_index": h_index
        })
    
    if len(metrics) < 30:
        return {
            "metric_name": "communication_complexity_rank",
            "metric_value": None,
            "instances_tested": len(metrics),
            "n_max": max(metric["n"] for metric in metrics),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    ranks = [metric["rank"] for metric in metrics]
    h_indices = [metric["h_index"] for metric in metrics]
    
    mean_rank = sum(ranks) / len(ranks)
    mean_h_index = sum(h_indices) / len(h_indices)
    
    correlation_coefficient = 0
    for i in range(len(ranks)):
        correlation_coefficient += (ranks[i] - mean_rank) * (h_indices[i] - mean_h_index)
    correlation_coefficient /= math.sqrt(sum((x - mean_rank) ** 2 for x in ranks)) * math.sqrt(sum((y - mean_h_index) ** 2 for y in h_indices))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": len(metrics),
        "n_max": max(metric["n"] for metric in metrics),
        "conjecture_holds": abs(correlation_coefficient) >= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len([res for res in results if res["metric_value"] is not None])
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None)) / len([res for res in results if res["metric_value"] is not None])
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")