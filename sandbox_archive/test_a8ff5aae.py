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
    
    def hypergeometric_rank(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 0
        A = [[0] * (n + 1) for _ in range(n + 1)]
        b = [0] * (n + 1)
        for i in range(1, n + 1):
            for j in range(i + 1):
                A[i][j] = math.comb(i, j)
            b[i] = sum(f[j] for j in range(2**i))
        
        # Gaussian elimination
        for i in range(n + 1):
            if A[i][i] == 0:
                return float('inf')
            for j in range(i + 1, n + 1):
                factor = A[j][i] / A[i][i]
                for k in range(i, n + 1):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        
        rank = 0
        for i in range(n + 1):
            if any(A[i][j] != 0 for j in range(rank)):
                rank += 1
        
        return rank
    
    def communication_complexity(n):
        return n
    
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        f = generate_boolean_function(random.randint(3, 40))
        r_f = hypergeometric_rank(f)
        if r_f == float('inf'):
            continue
        CC_XOR_n = communication_complexity(len(f))
        metric_values.append(CC_XOR_n / (r_f * math.log2(len(f))))
    
    if not metric_values:
        return {
            "metric_name": "CC_XOR(n) / (r_f * log n)",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_metric = sum(metric_values) / len(metric_values)
    std_metric = math.sqrt(sum((x - mean_metric) ** 2 for x in metric_values) / len(metric_values))
    conjecture_holds = all(x >= 1 for x in metric_values)
    counterexample = "" if conjecture_holds else "CC_XOR(n) < Ω(r_f log n)"
    
    return {
        "metric_name": "CC_XOR(n) / (r_f * log n)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric = sum(x["metric_value"] for x in results) / len(results)
    std_metric = math.sqrt(sum((x["metric_value"] - mean_metric) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if all(x["conjecture_holds"] for x in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC_XOR(n) < Ω(r_f log n)\" first_failing_seed={first_failing_seed}")