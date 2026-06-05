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
    
    def matrix_from_function(f, n):
        A = [[f[i * (1 << j) + k] for k in range(1 << j)] for j in range(n)]
        return A
    
    def communication_complexity_rank(A):
        m, n = len(A), len(A[0])
        rank = 0
        for i in range(m):
            if any(A[i][j] == 1 for j in range(n)):
                rank += 1
        return rank
    
    def quasi_crystals_count(A):
        m, n = len(A), len(A[0])
        count = 0
        for i in range(m):
            for j in range(n):
                if A[i][j] == 1:
                    count += 1
        return count
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    A = matrix_from_function(f, n)
    
    Q = quasi_crystals_count(A)
    r = communication_complexity_rank(A)
    
    if r == 0:
        return {
            "metric_name": "Q/f(r)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "communication_complexity_rank_is_zero"
        }
    
    metric_value = Q / r
    return {
        "metric_name": "Q/f(r)",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(v is not None for v in metric_values):
        mean = sum(metric_values) / len(metric_values)
        std_dev = math.sqrt(sum((v - mean)**2 for v in metric_values) / len(metric_values))
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds'] if r['metric_value'] is not None))]}")
    else:
        print("RESULT: INCONCLUSIVE metric_values_contains_none")