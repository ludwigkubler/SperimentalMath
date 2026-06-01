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
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 1
        complexity = 0
        for i in range(1, n):
            complexity += (i + 1) * (1 << (n - i))
        return complexity
    
    def projective_representations(f):
        n = len(f)
        if n == 1:
            return 1
        representations = 0
        for i in range(1, n):
            representations += (i + 1) * (1 << (n - i))
        return representations
    
    metric_name = "communication_complexity"
    instances_tested = 30
    n_max = 40
    conjecture_holds = True
    counterexample = ""
    
    results = []
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        f = generate_boolean_function(n)
        c_f = communication_complexity(f)
        N_f = projective_representations(f)
        results.append((c_f, N_f))
    
    if len(results) < instances_tested:
        return {
            "metric_name": metric_name,
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    c_values = [c for c, _ in results]
    N_values = [N for _, N in results]
    
    mean_c = sum(c_values) / len(c_values)
    mean_N = sum(N_values) / len(N_values)
    
    correlation_coefficient = 0
    if mean_c != 0 and mean_N != 0:
        numerator = sum((c - mean_c) * (N - mean_N) for c, N in results)
        denominator = math.sqrt(sum((c - mean_c)**2 for c in c_values)) * math.sqrt(sum((N - mean_N)**2 for N in N_values))
        correlation_coefficient = numerator / denominator
    
    if correlation_coefficient < 0.7:
        conjecture_holds = False
        counterexample = f"correlation_coefficient={correlation_coefficient:.4f}"
    
    return {
        "metric_name": metric_name,
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["counterexample"] != "")
        counterexample_desc = next(result["counterexample"] for result in results if not result["conjecture_holds"] and result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")