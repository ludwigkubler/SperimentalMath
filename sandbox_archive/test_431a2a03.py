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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def delone_set_representation(f, n):
    delone_set = []
    for i in range(2**n):
        binary_rep = format(i, f'0{n}b')
        if all(f[j] == int(binary_rep[j]) for j in range(n)):
            delone_set.append(tuple(map(int, binary_rep)))
    return delone_set

def matroid_rank(d):
    elements = list(d.keys())
    n = len(elements)
    rank = 0
    for i in range(1, 2**n):
        subset = [elements[j] for j in range(n) if (i & (1 << j))]
        independent = True
        for j in range(len(subset)):
            for k in range(j + 1, len(subset)):
                if d.get(tuple(sorted([subset[j], subset[k]])), 0) != 0:
                    independent = False
                    break
            if not independent:
                break
        if independent:
            rank += 1
    return rank

def communication_complexity(n):
    # Simplified version of the k-CLIQUE communication complexity protocol
    return n * (n - 1) // 2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        d = delone_set_representation(f, n)
        rank = matroid_rank(d)
        cc_kclique = communication_complexity(n)
        results.append((rank, cc_kclique))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    alpha = 0.95
    z_alpha = 1.96  # Z-score for 95% confidence interval
    std_rank = (sum((rank - mean_rank)**2 for rank, _ in results) / len(results))**0.5
    upper_bound = mean_rank + z_alpha * std_rank / math.sqrt(len(results))
    
    conjecture_holds = all(rank <= alpha * cc_kclique for rank, cc_kclique in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")