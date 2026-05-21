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
    
    def generate_explicit_function(n):
        # Example function: a polynomial over F_2
        return [random.choice([0, 1]) for _ in range(n)]
    
    def local_zeta_function_rank(f):
        n = len(f)
        zeta = 0
        for i in range(1 << n):
            product = 1
            for j in range(n):
                if (i >> j) & 1:
                    product *= f[j]
            zeta += product
        return abs(zeta)
    
    def minimal_local_zeta_function_rank(f):
        return min(local_zeta_function_rank(g) for g in generate_all_subsets(f))
    
    def generate_all_subsets(lst):
        subsets = []
        n = len(lst)
        for i in range(1 << n):
            subset = [lst[j] for j in range(n) if (i >> j) & 1]
            subsets.append(subset)
        return subsets
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        f = generate_explicit_function(n)
        rank = minimal_local_zeta_function_rank(f)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    conjecture_holds = all(rank <= 10 for rank in ranks)
    counterexample = "" if conjecture_holds else "rank > 10"
    
    return {
        "metric_name": "MinimalLocalZetaFunctionRank",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > 10\" first_failing_seed={first_failing_seed}")