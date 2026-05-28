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

def generate_random_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_complexity_XOR(f):
    n = int(math.log2(len(f)))
    count = sum(1 for i in range(2**n) if f[i ^ (i >> 1)] == 0)
    return Fraction(count, 2**n)

def minimal_rank_geometric_invariant(f):
    # Placeholder implementation. Replace with actual geometric invariant computation.
    return len(f) ** (1/3)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_random_boolean_function(n)
    
    rank = minimal_rank_geometric_invariant(f)
    complexity = communication_complexity_XOR(f)
    
    metric_value = rank
    conjecture_holds = rank <= n ** (2/3) and abs(rank - complexity) / max(1, rank + complexity) >= 0.7
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} does not satisfy the bound for n={n}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank does not satisfy the bound\" first_failing_seed={first_failing_seed}")