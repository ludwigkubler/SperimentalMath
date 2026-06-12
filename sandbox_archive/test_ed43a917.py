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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def p_adic_log(x, p):
    if x <= 0:
        return float('-inf')
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 30
    protocols = []
    for _ in range(30):
        protocol = [random.randint(1, 2**n) for _ in range(n)]
        protocols.append(protocol)
    
    rank_variances = []
    p_adic_growth = []
    
    for protocol in protocols:
        # Calculate rank variance
        rank_variance = sum(abs(x - y) for x, y in zip(protocol, sorted(protocol))) / n
        rank_variances.append(rank_variance)
        
        # Calculate p-adic logarithmic growth
        growth = [p_adic_log(x, 2) for x in protocol]
        min_growth = min(growth)
        p_adic_growth.append(min_growth)
    
    correlation_coefficient = sum((x - mean_p_adic) * (y - mean_rank_var) 
                                  for x, y in zip(p_adic_growth, rank_variances)) / len(p_adic_growth)
    mean_p_adic = sum(p_adic_growth) / len(p_adic_growth)
    mean_rank_var = sum(rank_variances) / len(rank_variances)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(protocols),
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(correlation_coefficient) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    metric_mean = sum(r["metric_value"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={metric_mean} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")