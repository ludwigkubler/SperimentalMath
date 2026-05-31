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
    
    def count_satisfying_assignments(f, n):
        count = 0
        for i in range(2**n):
            if sum(x * y for x, y in zip(bin(i)[2:].zfill(n), f)) == len([x for x in f if x == 1]):
                count += 1
        return count
    
    def shannon_entropy(p):
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    n_values = [5, 10, 15, 20, 30, 40]
    g_n = []
    E_f = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        g_n.append(count_satisfying_assignments(f, n))
        p = Fraction(g_n[-1], 2**n)
        E_f.append(shannon_entropy(p))
    
    if len(E_f) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(E_f),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov / (std_x * std_y)
    
    correlation_coefficient = correlation(E_f, [math.log(g_n_i) for g_n_i in g_n])
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(E_f),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(v <= 4 for v in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["metric_value"] is not None for res in results):
        RESULT = f"SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if res["conjecture_holds"] is False)
        RESULT = f"FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)