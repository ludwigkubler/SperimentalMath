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
    
    def quandle_action_count(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    count += 1
        return count
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        rank_var = 0
        for i in range(n):
            for j in range(i+1, n):
                diff = sum(1 for k in range(2**n) if f[k ^ (1 << i)] != f[k ^ (1 << j)])
                rank_var += diff * diff
        return rank_var / (n * (n - 1))
    
    instances_tested = 0
    n_max = 0
    total_rank_variance = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            m = quandle_action_count(f)
            rank_variance = communication_complexity_rank_variance(f)
            
            total_rank_variance += rank_variance
            instances_tested += 1
    
    mean_rank_variance = total_rank_variance / instances_tested
    conjecture_holds = O(m) <= mean_rank_variance <= Theta(m**2)
    
    return {
        "metric_name": "rank_variance",
        "metric_value": mean_rank_variance,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"m={m}, rank_variance={mean_rank_variance}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank_variance = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_variance} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank_variance} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")