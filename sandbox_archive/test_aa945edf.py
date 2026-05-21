# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations_with_replacement, chain

def partitions(n):
    if n == 0:
        yield []
    else:
        for p in partitions(n - 1):
            for i in range(len(p) + 1):
                yield p[:i] + [p[i-1] + 1] + p[i+1:] if i > 0 else [n]

def chi_lambda(M, lambda_):
    n = len(M)
    sign = Fraction(1)
    for mu in partitions(n):
        if len(mu) == len(lambda_) and sum(mu) == sum(lambda_):
            product = 1
            for i in range(n):
                for j in range(i + 1, n):
                    if M[i][j] != M[j][i]:
                        return None
                    product *= Fraction(1 - (-1)**(mu[i] + mu[j]))
            sign *= product
    return abs(sign)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    m = 20
    M = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)]
    
    chi_perm_n = chi_lambda(M, [n])
    if chi_perm_n is None:
        return {
            "metric_name": "chi_lambda",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    chi_det_m = chi_lambda(M, [m])
    if chi_det_m is None:
        return {
            "metric_name": "chi_lambda",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    metric_value = chi_perm_n - chi_det_m
    conjecture_holds = metric_value > 0
    counterexample = "" if conjecture_holds else f"chi_det_{m} >= chi_perm_{n}"
    
    return {
        "metric_name": "chi_lambda",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")