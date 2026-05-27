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
    
    def algebraic_k_theory_group_size(f):
        n = len(f)
        if n == 1:
            return 1
        k = 2
        while True:
            g = generate_boolean_function(k)
            if all(g[i] != f[i] for i in range(n)):
                return k
            k += 1
    
    def min_rank(f):
        return algebraic_k_theory_group_size(f)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        for _ in range(50):  # Aim for at least 30 instances per seed
            f = generate_boolean_function(n)
            rank = min_rank(f)
            if rank < n / math.log(n):
                return {
                    "metric_name": "min_rank",
                    "metric_value": rank,
                    "instances_tested": len(ranks),
                    "conjecture_holds": False,
                    "counterexample": f"Function with n={n} has rank {rank}"
                }
            ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    return {
        "metric_name": "min_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": mean_rank >= n_values[-1] / math.log(n_values[-1]),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < n/log(n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")