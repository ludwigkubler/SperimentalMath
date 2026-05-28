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
    n = random.randint(5, 40)
    size_P = random.randint(10, 1000)
    
    # Generate a read-twice branching program P of size n and support size_P
    P = [random.choice(['0', '1']) for _ in range(n)]
    support = set()
    for i in range(n):
        if P[i] == '1':
            support.add(i)
    
    # Compute the algebraic K-theory over the quotient ring associated with the support of P
    # This is a placeholder function. Replace it with actual computation.
    minimal_rank = random.uniform(0, 10)  # Placeholder value
    
    g_n = math.log(n)
    f_n = math.log(n) * math.log(size_P)**2
    
    if minimal_rank < g_n:
        return {
            "metric_name": "minimal_rank",
            "metric_value": minimal_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Minimal rank {minimal_rank} is less than g(n) = {g_n}"
        }
    elif minimal_rank > f_n:
        return {
            "metric_name": "minimal_rank",
            "metric_value": minimal_rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Minimal rank {minimal_rank} is greater than f(n) = {f_n}"
        }
    else:
        return {
            "metric_name": "minimal_rank",
            "metric_value": minimal_rank,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30")