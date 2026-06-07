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
    
    def generate_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n - 1))
    
    def resolution_length(formula):
        stack = []
        for char in formula:
            if char == '0':
                if not stack or stack[-1] != '1':
                    return 1
                stack.pop()
            else:
                stack.append(char)
        return len(stack) + 1
    
    def local_cohomology_rank(formula):
        n = int(math.log2(len(formula) + 1))
        if n == 0: return 0
        rank = 0
        for i in range(n):
            count = formula.count('0' * (n - i) + '1')
            rank += count
        return rank
    
    instances_tested = 30
    metric_values = []
    n_max = 5
    
    for _ in range(instances_tested):
        n = random.choice([5, 10, 15, 20, 30, 40])
        if n > n_max: n_max = n
        
        formula = generate_formula(n)
        h_0 = local_cohomology_rank(formula)
        L = resolution_length(formula)
        
        metric_values.append((h_0, L))
    
    if len(metric_values) < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(metric_values),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    h_0s, Ls = zip(*metric_values)
    mean_h_0 = sum(h_0s) / len(h_0s)
    mean_L = sum(Ls) / len(Ls)
    
    correlation_coefficient = 0
    for h_0, L in metric_values:
        correlation_coefficient += (h_0 - mean_h_0) * (L - mean_L)
    correlation_coefficient /= math.sqrt(sum((h_0 - mean_h_0)**2 for h_0 in h_0s)) * math.sqrt(sum((L - mean_L)**2 for L in Ls))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={r['seed']}")
                break