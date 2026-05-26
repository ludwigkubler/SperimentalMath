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

def generate_boolean_function(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def boolean_tensor_product(f, g):
    n = len(f)
    m = len(g)
    result = []
    for x in range(n):
        for y in range(m):
            if x < n and y < m:
                result.append(f[x] * g[y])
            else:
                result.append(0)  # Handle out-of-range indices by appending 0
    return result

def count_distinct_tensor_product_valuations(boolean_function):
    n = int(math.log2(len(boolean_function)))
    valuations = set()
    for i in range(1 << n):
        f = boolean_function[i:i + n]
        g = boolean_function[n + i:n + 2 * n]
        valuations.add(tuple(boolean_tensor_product(f, g)))
    return len(valuations)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        boolean_function = generate_boolean_function(n)
        M_f = boolean_function
        r_M_f = len(M_f)  # Minimal rank is the length of the function
        num_valuations = count_distinct_tensor_product_valuations(boolean_function)
        
        if r_M_f > 2 * num_valuations:
            return {
                "metric_name": "minimal_rank",
                "metric_value": r_M_f,
                "instances_tested": n,
                "conjecture_holds": False,
                "counterexample": f"n={n}, minimal rank {r_M_f} > 2 * {num_valuations}"
            }
        
        results.append(r_M_f)
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = len([x for x in results if x <= 2 * num_valuations]) / len(results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean,
        "instances_tested": sum(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    all_results = [r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]
    support_fraction = len(all_results) / len(results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in all_results)/len(all_results)} std={math.sqrt(sum((r['metric_value'] - sum(r['metric_value'] for r in all_results)/len(all_results)) ** 2 for r in all_results) / len(all_results))} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={n_values[0]}, minimal rank {results[0]['metric_value']} > 2 * {results[0]['counterexample'].split(',')[1].strip()}\") first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")