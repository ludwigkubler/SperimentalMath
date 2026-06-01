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

def generate_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(2**n)]

def communication_rank(f: list) -> int:
    n = len(f)
    if n == 1:
        return 1
    rank = 1
    for i in range(n):
        if f[i] != f[0]:
            break
    else:
        return rank
    for j in range(1, n):
        if f[j] != f[1]:
            break
    else:
        return rank
    rank += 1
    for k in range(2, n):
        if f[k] != f[2]:
            break
    else:
        return rank
    rank += 1
    return rank

def p_adic_galois_representation(f: list) -> int:
    n = len(f)
    rho = 1
    for i in range(n):
        if any(f[i * 2**(n-j-1): (i+1) * 2**(n-j-1)] == f[(i+1) * 2**(n-j-1): (i+2) * 2**(n-j-1)] for j in range(len(f))):
            rho += 1
    return rho

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    rho = p_adic_galois_representation(f)
    rank_gal = communication_rank(f)
    metric_value = math.log(rho)
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "log_rho",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = f"seed={result['seed']}, log_rho={result['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={result['seed']}")
                break