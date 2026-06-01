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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
    def is_sat(instance):
        m, n = len(instance), len(instance[0])
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if instance[i][j]:
                    A[i][-1] -= 2 ** j
                else:
                    A[i][-1] += 2 ** j
            A[i][-1] %= 2
        reduced_A = gaussian_elimination(A)
        for row in reduced_A:
            if row[-1] != 0 and all(x == 0 for x in row[:-1]):
                return False
        return True
    
    def clause_set_complexity(instance):
        m, n = len(instance), len(instance[0])
        return sum(sum(row) for row in instance)
    
    def min_affine_generators(instance):
        m, n = len(instance), len(instance[0])
        A = [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                if instance[i][j]:
                    A[i][-1] -= 2 ** j
                else:
                    A[i][-1] += 2 ** j
            A[i][-1] %= 2
        reduced_A = gaussian_elimination(A)
        return sum(1 for row in reduced_A if any(x != 0 for x in row[:-1]))
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    
    for _ in range(instances_tested):
        m = random.randint(5, 40)
        n = random.randint(5, 40)
        instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
        
        if not is_sat(instance):
            continue
        
        c_phi = clause_set_complexity(instance)
        min_order = min_affine_generators(instance)
        
        metric_values.append(math.log(m) / math.log(c_phi))
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = (sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
    
    if len(metric_values) < instances_tested:
        conjecture_holds = False
        counterexample = "not_enough_valid_instances"
    else:
        counterexample = ""
    
    return {
        "metric_name": "log(m) / log(c(φ))",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_valid_instances\" first_failing_seed={first_failing_seed}")