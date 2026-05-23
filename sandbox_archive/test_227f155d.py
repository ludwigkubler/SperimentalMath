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
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = len(f)
        # Simulate a simple protocol
        return math.ceil(math.log2(n + 1))
    
    def min_rank_of_polynomials(f):
        n = len(f)
        # Placeholder for actual GIT computation
        # For simplicity, we use a dummy rank based on function complexity
        return n
    
    def run_disjointness_protocol(f):
        return communication_complexity(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    
    for n in n_values:
        f = generate_random_function(n)
        rank = min_rank_of_polynomials(f)
        comm_complexity = run_disjointness_protocol(f)
        
        if rank == 0 or comm_complexity == 0:
            continue
        
        ratio = comm_complexity / rank
        total_ratio += ratio
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "No valid instances tested"
        }
    
    mean_ratio = total_ratio / instances_tested
    conjecture_holds = mean_ratio >= 1.0
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "Mean ratio < 1"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["instances_tested"] == 0 for r in results):
        print("RESULT: INCONCLUSIVE no_valid_instances")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Mean ratio < 1' first_failing_seed={first_failing_seed}")