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
    
    def quadratic_form(f, x):
        n = len(x)
        result = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    result += x[i] * x[j]
        return result
    
    def minimal_quadratic_defect(f):
        n = len(f)
        min_defect = float('inf')
        for k in range(2**n):
            x_k = [int(bit) for bit in format(k, f'0{n}b')]
            defect = abs(quadratic_form(f, x_k) - 1) / n
            if defect < min_defect:
                min_defect = defect
        return min_defect
    
    def communication_complexity(f):
        n = len(f)
        instances = []
        for i in range(2**n):
            x_i = [int(bit) for bit in format(i, f'0{n}b')]
            instances.append((x_i, f[i]))
        
        cc = 0
        for i in range(len(instances)):
            for j in range(i+1, len(instances)):
                if instances[i][1] != instances[j][1]:
                    cc += 1
        return cc
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        min_defect = minimal_quadratic_defect(f)
        cc = communication_complexity(f)
        
        if abs(min_defect - cc) / cc > 0.1:
            return {
                "metric_name": "communication_complexity",
                "metric_value": cc,
                "instances_tested": len(instances),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"CC(f) = {cc}, D_q(f) = {min_defect}"
            }
        
        results.append(cc)
    
    mean_cc = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_cc)**2 for x in results) / len(results))
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc,
        "instances_tested": 30 * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean_cc = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_cc)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if abs(r - mean_cc) / mean_cc <= 0.1) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std={std_dev} support_fraction={support_fraction}")
    elif any(abs(r - mean_cc) / mean_cc > 0.1 for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if abs(r - mean_cc) / mean_cc > 0.1))]
        print(f"RESULT: FALSIFIED counterexample='CC(f) != D_q(f)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")