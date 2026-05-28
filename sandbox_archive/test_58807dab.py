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
    
    def construct_sheaf(f):
        n = len(f)
        sheaf = []
        for i in range(n):
            row = [f[j] if j & (1 << i) else 0 for j in range(2**n)]
            sheaf.append(row)
        return sheaf
    
    def compute_minimal_rank(sheaf):
        n = len(sheaf)
        rank = 0
        for i in range(n):
            row = sheaf[i]
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return rank
    
    def compute_acc0_circuit_weight(f):
        n = len(f)
        weight = 0
        for i in range(2**n):
            if f[i]:
                weight += 1
        return weight
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        sheaf = construct_sheaf(f)
        minimal_rank = compute_minimal_rank(sheaf)
        acc0_weight = compute_acc0_circuit_weight(f)
        
        if minimal_rank < math.log(n) or minimal_rank > 2 * math.log(n):
            return {
                "metric_name": "minimal_rank",
                "metric_value": minimal_rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={minimal_rank}"
            }
        
        results.append(minimal_rank)
    
    mean_rank = sum(results) / len(results)
    std_rank = math.sqrt(sum((x - mean_rank)**2 for x in results) / len(results))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= math.log(n_values[-1]) and r <= 2 * math.log(n_values[-1])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r < math.log(n_values[-1]) or r > 2 * math.log(n_values[-1]) for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < math.log(n_values[-1]) or r > 2 * math.log(n_values[-1])))]
        print(f"RESULT: FALSIFIED counterexample='rank_out_of_bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")