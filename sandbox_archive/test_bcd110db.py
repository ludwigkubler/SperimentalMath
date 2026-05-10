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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(n):
    total = 0
    for i in range(n):
        for j in range(n - i):
            total += (n - i - j) * (n - i)
    return factorial(n) ** 2 // total

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        T_permanent = hook_length_formula(n - 1)
        T_determinant = hook_length_formula(n)
        ratio = math.log2(T_permanent / T_determinant)
        
        if ratio < n / 2:
            return {
                "metric_name": "log2(T_permanent / T_determinant)",
                "metric_value": ratio,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, log2(T_permanent / T_determinant)={ratio}"
            }
    
    return {
        "metric_name": "log2(T_permanent / T_determinant)",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["conjecture_holds"])
    
    support_fraction = sum(results) / len(results)
    if all(results):
        print(f"RESULT: SUPPORTED mean={sum([r['metric_value'] for r in results]) / len(results)} std=0.0 support_fraction=1.0")
    elif any(not r for r in results):
        first_failing_seed = seeds[results.index(False)]
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")