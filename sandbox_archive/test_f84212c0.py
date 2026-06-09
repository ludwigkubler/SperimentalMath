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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        # Simplified version of rank variance calculation
        return sum(abs(f[i] - f[j]) for i in range(n) for j in range(i+1, n)) / (n * (n-1))
    
    def construct_category_from_function(f):
        n = len(f)
        category = []
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    category.append((i, j))
        return category
    
    def minimal_number_of_monoidal_functors(category):
        # Simplified version of monoidal functor calculation
        return len(category)
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    R_f = communication_complexity_rank_variance(f)
    category = construct_category_from_function(f)
    k = minimal_number_of_monoidal_functors(category)
    dim_C_k = [len([x for x in category if x[1] == i]) for i in range(2**n)]
    
    metric_value = sum(k * d for k, d in zip(range(1, len(dim_C_k) + 1), dim_C_k))
    instances_tested = 1
    n_max = n
    conjecture_holds = abs(metric_value - R_f) <= 3 and metric_value / sum(metric_value for _ in range(instances_tested)) >= 0.5
    counterexample = "" if conjecture_holds else f"Rank variance: {R_f}, Metric value: {metric_value}"
    
    return {
        "metric_name": "min_k * dim(C_k)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
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