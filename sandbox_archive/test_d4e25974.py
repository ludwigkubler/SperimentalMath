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
    
    def construct_matroid(f):
        n = len(f)
        matroid = []
        for i in range(1 << n):
            subset = [j for j in range(n) if (i & (1 << j)) != 0]
            if all(f[i] == f[j] for j in subset):
                matroid.append(subset)
        return matroid
    
    def minimal_rank(matroid):
        rank = 0
        for cycle in matroid:
            if len(cycle) > rank:
                rank = len(cycle)
        return rank
    
    def communication_complexity(f):
        n = len(f)
        max_bits = math.ceil(math.log2(n + 1))
        return max_bits
    
    n_values = [10, 15, 20, 30]
    ranks = []
    complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        matroid = construct_matroid(f)
        rank = minimal_rank(matroid)
        complexity = communication_complexity(f)
        
        ranks.append(rank)
        complexities.append(complexity)
    
    correlation_coefficient = sum((ranks[i] - mean_ranks) * (complexities[i] - mean_complexities) for i in range(len(n_values))) / len(n_values)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")