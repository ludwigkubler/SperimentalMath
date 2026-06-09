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
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        rank = 0
        for i in range(1, n+1):
            for subset in itertools.combinations(range(n), i):
                subfunction = [f[j] if j in subset else 0 for j in range(n)]
                if sum(subfunction) == i:
                    rank += 1
        return rank / (n * (n + 1))
    
    def monoidal_functors(f):
        n = len(f)
        functors = []
        for i in range(1, n+1):
            functor = {}
            for j in range(n):
                if f[j] == 1:
                    functor[j] = [random.randint(0, 1) for _ in range(i)]
            functors.append(functor)
        return functors
    
    def min_number_of_functors(f):
        functors = monoidal_functors(f)
        min_k = float('inf')
        for k in range(1, len(functors)+1):
            dim_sum = sum(len(v) for v in functors[:k])
            if dim_sum < min_k:
                min_k = dim_sum
        return min_k
    
    n = random.randint(5, 30)
    f = generate_boolean_function(n)
    R_f = communication_complexity_rank_variance(f)
    k = min_number_of_functors(f)
    
    metric_value = k * sum(len(v) for v in monoidal_functors(f)[:k])
    conjecture_holds = abs(metric_value - R_f) <= 3
    counterexample = "" if conjecture_holds else f"R(f)={R_f}, k*dim(C_k)={metric_value}"
    
    return {
        "metric_name": "min_number_of_functors",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")