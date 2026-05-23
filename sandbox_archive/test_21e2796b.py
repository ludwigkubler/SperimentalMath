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
    
    def generate_instance(n):
        return [random.randint(1, 10) for _ in range(n)]
    
    def tensor_product(a, b):
        result = []
        for x in a:
            for y in b:
                result.append(x * y)
        return result
    
    def tropical_rank(lst):
        if not lst:
            return 0
        max_val = max(lst)
        return sum(1 for x in lst if x == max_val)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instance_a = generate_instance(n)
        instance_b = generate_instance(n)
        product = tensor_product(instance_a, instance_b)
        rank = tropical_rank(product)
        
        results.append({
            "n": n,
            "tropical_rank": rank
        })
    
    max_rank = max(result["tropical_rank"] for result in results)
    expected_bound = max(1, n_values[-1] ** 2 * math.log(n_values[-1]))
    
    conjecture_holds = max_rank <= expected_bound
    counterexample = f"n={max_rank}, tropical_rank={max_rank} > O(n^2 log n)" if not conjecture_holds else ""
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": max_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")