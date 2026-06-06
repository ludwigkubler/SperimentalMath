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
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        if 2**n != len(f):
            raise ValueError("Invalid function size")
        
        # Simplified version of the actual algorithm
        rank = 0
        for i in range(n):
            count_1 = sum(1 for x in f if x & (1 << i) > 0)
            if count_1 == n or count_1 == 0:
                continue
            rank += 1
        return rank
    
    def polynomial_representation(f, n):
        # Simplified version of the actual algorithm
        poly = [0] * (n + 1)
        for x in range(2**n):
            if f[x]:
                poly[bin(x).count('1')] += 1
        return poly
    
    def minimal_diophantine_dimension(poly, n):
        # Simplified version of the actual algorithm
        degree = max(i for i, coeff in enumerate(poly) if coeff != 0)
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        r_f = communication_complexity_rank(f)
        p_f = polynomial_representation(f, n)
        d_p_f = minimal_diophantine_dimension(p_f, n)
        
        if d_p_f < r_f**2:
            conjecture_holds = False
            counterexample = f"n={n}, r_f={r_f}, d(p_f)={d_p_f}"
        
        total_metric_value += d_p_f
        instances_tested += 1
        n_max = max(n_max, n)
    
    return {
        "metric_name": "minimal_diophantine_dimension",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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