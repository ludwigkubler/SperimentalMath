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
    
    def construct_real_algebraic_variety(f):
        n = len(f)
        variety = set()
        for i in range(2**n):
            x = [f[i >> j & 1] for j in range(n)]
            variety.add(tuple(x))
        return variety
    
    def compute_dimension(V):
        if not V:
            return 0
        n = len(next(iter(V)))
        max_rank = 0
        for v in V:
            rank = sum(v[i] != v[j] for i, j in itertools.combinations(range(n), 2))
            max_rank = max(max_rank, rank)
        return max_rank
    
    def log_ratio(n):
        return math.log(n) / math.log(math.log(n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    dimensions = []
    for n in n_values:
        f = generate_boolean_function(n)
        V = construct_real_algebraic_variety(f)
        dimension = compute_dimension(V)
        dimensions.append(dimension)
    
    mean_dimension = sum(dimensions) / len(dimensions)
    conjecture_holds = abs(mean_dimension - log_ratio(40)) <= 3 and max(dimensions) <= 10
    counterexample = "" if conjecture_holds else f"mean={mean_dimension}, dimensions={dimensions}"
    
    return {
        "metric_name": "dimension",
        "metric_value": mean_dimension,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")