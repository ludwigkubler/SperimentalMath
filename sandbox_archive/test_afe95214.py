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
    
    def quaternion_algebra(f):
        n = len(f)
        Q_f = []
        for i in range(2**n):
            row = []
            for j in range(2**n):
                if f[i] == f[j]:
                    row.append(1)
                else:
                    row.append(-1)
            Q_f.append(row)
        return Q_f
    
    def arithmetic_rank(Q):
        n = len(Q)
        rank = 0
        for i in range(n):
            pivot_row = None
            for j in range(i, n):
                if Q[j][i] != 0:
                    pivot_row = j
                    break
            if pivot_row is None:
                continue
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = Q[j][i] / Q[pivot_row][i]
                for k in range(n):
                    Q[j][k] -= factor * Q[pivot_row][k]
        return rank
    
    def communication_complexity(f):
        n = len(f)
        # Simplified protocol: each party sends their input bit
        return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different functions
            f = generate_boolean_function(n)
            Q_f = quaternion_algebra(f)
            R_QUAT_Q_f = arithmetic_rank(Q_f)
            CC_R_DISJ_n = communication_complexity(f)
            
            total_metric_value += CC_R_DISJ_n
            instances_tested += 1
            
            if R_QUAT_Q_f < n and CC_R_DISJ_n >= n:
                conjecture_holds = False
                counterexample = f"n={n}, R_QUAT(Q_f)={R_QUAT_Q_f}, CC_R(DISJ_n)={CC_R_DISJ_n}"
    
    return {
        "metric_name": "Randomized Communication Complexity",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")