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
    
    def circuit_depth(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        depth = 0
        while any(x > 1 for x in f):
            new_f = []
            for i in range(0, len(f), 2):
                new_f.append(int(f[i] != f[i + 1]))
            f = new_f
            depth += 1
        return depth
    
    def geometric_realizations(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function length")
        realizations = []
        for i in range(2**n):
            realization = [f[i]]
            while len(realization) < n:
                next_val = (realization[-1] + 1) % 2
                if next_val not in realization:
                    realization.append(next_val)
            realizations.append(realization)
        return len(set(tuple(r) for r in realizations))
    
    results = []
    for _ in range(100):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        depth = circuit_depth(f)
        realizations = geometric_realizations(f)
        results.append((realizations, depth))
    
    if not results:
        return {
            "metric_name": "Spearman rank correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "empty_results"
        }
    
    realizations = [r for r, _ in results]
    depths = [d for _, d in results]
    
    def spearman_rank_correlation(realizations, depths):
        n = len(realizations)
        rank_realizations = sorted(range(n), key=lambda i: realizations[i])
        rank_depths = sorted(range(n), key=lambda i: depths[i])
        rho_numerator = sum((rank_realizations[i] - rank_depths[i]) ** 2 for i in range(n))
        rho_denominator = n * (n**2 - 1) / 6
        return 1 - 6 * rho_numerator / rho_denominator
    
    rho = spearman_rank_correlation(realizations, depths)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "n_max": max(n for _, n in results),
        "conjecture_holds": rho >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
        exit(0)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")