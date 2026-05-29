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
            pivot = Q[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = -Q[j][i] / pivot
                for k in range(n):
                    Q[j][k] += factor * Q[i][k]
            rank += 1
        return rank
    
    def communication_complexity(f):
        n = len(f)
        if n == 1:
            return 0
        else:
            # Simplified protocol: each party sends its input bit and the other listens
            return 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        Q_f = quaternion_algebra(f)
        R_QUAT_Q_f = arithmetic_rank(Q_f)
        CC_R_DISJ_n = communication_complexity(f)
        
        results.append({
            "n": n,
            "R_QUAT_Q_f": R_QUAT_Q_f,
            "CC_R_DISJ_n": CC_R_DISJ_n
        })
    
    total_r_quat = sum(result["R_QUAT_Q_f"] for result in results)
    total_cc_disj = sum(result["CC_R_DISJ_n"] for result in results)
    mean_r_quat = total_r_quat / len(results)
    mean_cc_disj = total_cc_disj / len(results)
    
    conjecture_holds = all(result["R_QUAT_Q_f"] >= n and result["CC_R_DISJ_n"] >= n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc_disj,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")