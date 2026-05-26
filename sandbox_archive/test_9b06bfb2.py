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
    
    def generate_monomial_ideal(n):
        if n == 1:
            return {0}
        else:
            ideal = set()
            for i in range(1, n):
                for j in range(i+1, n):
                    ideal.add((i, j))
            return ideal
    
    def complexity(I):
        return len(I)
    
    def minimal_rank(I):
        if not I:
            return 0
        rank = float('inf')
        for i in range(1, len(I) + 1):
            for subset in itertools.combinations(I, i):
                if all(x < y for x, y in subset):
                    rank = min(rank, i)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        I = generate_monomial_ideal(n)
        c_I = complexity(I)
        rank = minimal_rank(I)
        
        if rank > c_I**(2/3) * (1 + 0.1):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, c(I)={c_I}, rank={rank}"
            }
        
        results.append({
            "n": n,
            "c_I": c_I,
            "rank": rank
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["rank"] >= n**(3/5)) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank exceeds upper bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")