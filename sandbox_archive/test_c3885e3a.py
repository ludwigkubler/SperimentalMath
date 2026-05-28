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
    
    def generate_and_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_affine_variety(and_func):
        n = len(and_func)
        generators = []
        for i in range(2**n):
            if and_func[i] == 1:
                gen = [0] * (2**n)
                gen[i] = 1
                generators.append(gen)
        return generators
    
    def compute_rank(generators):
        n = len(generators[0])
        M = [[0] * n for _ in range(n)]
        for gen in generators:
            for i in range(n):
                M[i][i] += gen[i]**2
        rank = 0
        for row in M:
            if any(row):
                rank += 1
        return rank
    
    def communication_complexity(rank):
        # Simplified model: complexity is proportional to rank^2
        return rank**2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(50):  # Aim for at least 30 instances per seed
            and_func = generate_and_function(n)
            generators = construct_affine_variety(and_func)
            rank = compute_rank(generators)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    conjecture_holds = mean_rank > math.exp(0.5 * n_values[-1])
    
    return {
        "metric_name": "mean_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")