# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def geometric_quantization(f):
        n = len(f)
        Q = [[Fraction(0)] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    Q[i][j] = Fraction(1)
        return Q
    
    def acc0_complexity(f):
        n = len(f)
        # Simplified DPLL solver to estimate ACC⁰ complexity
        count = 0
        for assignment in itertools.product([0, 1], repeat=n):
            if f[assignment.index(1)] == 1:
                count += 1
        return count
    
    def is_in_p(f):
        # Placeholder function to check if f is in P
        # This should be replaced with actual logic based on the problem definition
        return True
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(2**n)]
    
    if not is_in_p(f):
        return {
            "metric_name": "ACC⁰ Complexity",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "f_not_in_P"
        }
    
    Q = geometric_quantization(f)
    acc0_bound = acc0_complexity(f)
    
    rank = sum(1 for row in Q if any(x != Fraction(0) for x in row))
    
    return {
        "metric_name": "ACC⁰ Complexity",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= acc0_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        # Generate a list of 30 prime numbers as default seeds
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean)**2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='f_not_in_P' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")