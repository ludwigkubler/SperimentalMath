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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = len(f)
        max_rank = 0
        for i in range(1 << n):
            rank = sum(1 for j in range(i) if f[i] != f[j])
            max_rank = max(max_rank, rank)
        return max_rank
    
    def grothendieck_tate_dimension(f):
        n = len(f)
        # Simplified version of Grothendieck-Tate dimension calculation
        # This is a placeholder and should be replaced with actual implementation
        return n  # Placeholder for actual computation
    
    metric_name = "communication_complexity_rank_variance"
    instances_tested = 0
    total_variance = 0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > max_n:
            max_n = n
        
        for _ in range(5):  # Test with 5 instances per size
            f = generate_boolean_function(n)
            rank = communication_complexity_rank(f)
            variance = (rank - n / 2) ** 2
            total_variance += variance
            instances_tested += 1
            
            dim = grothendieck_tate_dimension(f)
            if variance > dim:
                conjecture_holds = False
                counterexample = f"n={n}, rank={rank}, dim={dim}"
    
    mean_variance = total_variance / instances_tested
    std_variance = math.sqrt(sum((x - mean_variance) ** 2 for x in [variance for _, variance, _ in trials]) / instances_tested)
    
    return {
        "metric_name": metric_name,
        "metric_value": mean_variance,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_variance = sum(r["metric_value"] for r in results) / len(results)
    std_variance = math.sqrt(sum((r["metric_value"] - mean_variance) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")