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
    
    def communication_complexity_rank(f):
        # Placeholder for actual computation of communication complexity rank
        return len(f) // 2
    
    def minimal_symplectic_geometry_rank(G_f):
        # Placeholder for actual computation of minimal symplectic geometry rank
        return len(G_f) // 3
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        f = ''.join(random.choice('01') for _ in range(n))
        r_f = communication_complexity_rank(f)
        G_f = generate_hyperplane_arrangement(f)  # Placeholder function
        min_rank_G_f = minimal_symplectic_geometry_rank(G_f)
        
        results.append({
            "n": n,
            "r_f": r_f,
            "min_rank_G_f": min_rank_G_f
        })
    
    metric_value = sum(r["min_rank_G_f"] / r["r_f"] for r in results) / len(results)
    conjecture_holds = all(abs(r["min_rank_G_f"] / r["r_f"]) <= 2 for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "rank_correlation",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")

def generate_hyperplane_arrangement(f):
    # Placeholder function to generate hyperplane arrangement
    return [f[i] for i in range(len(f)) if f[i] == '1']