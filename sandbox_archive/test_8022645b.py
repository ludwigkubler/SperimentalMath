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
    
    def monotone_complexity(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input must be a boolean function of n bits")
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[2**i] > f[2**j]:
                    count += 1
        return count
    
    def twisted_differential_forms_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Input must be a boolean function of n bits")
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                diff = f[2**i] - f[2**j]
                if diff != 0:
                    rank += 1
        return rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        var_x = sum((xi - mean_x)**2 for xi in x) / len(x)
        var_y = sum((yi - mean_y)**2 for yi in y) / len(y)
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        rank = twisted_differential_forms_rank(f)
        complexity = monotone_complexity(f)
        if rank == 0 or complexity == 0:
            continue
        ranks.append(rank)
        complexities.append(complexity)
    
    if not ranks or not complexities:
        return {
            "metric_name": "Correlation Coefficient",
            "metric_value": None,
            "instances_tested": len(ranks),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(ranks, complexities)
    ratio_mean = sum(rank / complexity for rank, complexity in zip(ranks, complexities)) / len(ranks)
    ratio_min = min(rank / complexity for rank, complexity in zip(ranks, complexities))
    ratio_max = max(rank / complexity for rank, complexity in zip(ranks, complexities))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation,
        "instances_tested": len(ranks),
        "conjecture_holds": 0.5 <= ratio_min and ratio_max <= 1.5 and correlation > 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")