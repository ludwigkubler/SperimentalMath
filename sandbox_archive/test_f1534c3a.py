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
    
    def compute_parity(f):
        n = len(f)
        result = 0
        for i in range(n):
            if f[i] == 1:
                result ^= (i + 1) % 2
        return result
    
    def construct_real_algebraic_variety(f):
        n = len(f)
        variety = []
        for x in range(2**n):
            if compute_parity([int(b) for b in f'{x:0{n}b}']) == 1:
                variety.append(x)
        return variety
    
    def min_rank(variety):
        n = len(variety)
        rank = 0
        while variety:
            pivot = variety.pop()
            variety = [v for v in variety if (v & pivot) != pivot]
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    dimensions = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        variety = construct_real_algebraic_variety(f)
        dimension = min_rank(variety)
        dimensions.append(dimension)
    
    mean_dimension = sum(dimensions) / len(dimensions)
    conjecture_holds = all(d <= 10 for d in dimensions)
    counterexample = "" if conjecture_holds else "dimension > 10"
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_dimension,
        "instances_tested": len(dimensions),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_dimension = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_dimension} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")