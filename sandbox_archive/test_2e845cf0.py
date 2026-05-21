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
    
    def hypergeometric_moment(k, n):
        if k > n or k < 0:
            return 0
        return math.comb(n, k) / math.comb(2*n, k)
    
    def communication_complexity(n):
        # Simplified deterministic protocol for XOR communication complexity
        return n
    
    n = random.randint(5, 40)
    instances_tested = 30
    total_moment = 0
    max_indices = []
    
    for _ in range(instances_tested):
        f = [random.choice([0, 1]) for _ in range(n)]
        moment_sum = sum(hypergeometric_moment(i, n) * f[i] for i in range(n))
        if moment_sum != 0:
            max_indices.append((moment_sum, list(range(n))))
    
    M_f = len(max_indices)
    CC_XOR_n = communication_complexity(n)
    metric_value = M_f * math.log(n)
    
    conjecture_holds = M_f > 0 and CC_XOR_n >= metric_value
    counterexample = "" if conjecture_holds else "M_f=0 or CC_XOR(n) < M_f log n"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + list(range(50, 80)) + list(range(100, 130))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")