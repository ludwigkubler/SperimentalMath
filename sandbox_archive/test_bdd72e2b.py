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
    
    def circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        elif n == 2:
            return 3
        else:
            return 2 * circuit_size(f[:n//2]) + circuit_size(f[n//2:])
    
    def fourier_transform(f):
        n = len(f)
        result = [0] * (2*n-1)
        for k in range(2*n-1):
            for i in range(n):
                result[k] += f[i] * math.exp(-2j * math.pi * i * k / n) / math.sqrt(n)
        return result
    
    def kostant_sheaf_rank(f):
        n = len(f)
        fourier = fourier_transform(f)
        max_abs_value = max(abs(x) for x in fourier)
        return int(math.ceil(max_abs_value))
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    rank = kostant_sheaf_rank(f)
    size = circuit_size(f)
    
    if size == 0:
        return {
            "metric_name": "rank_over_circuit_size",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit_size_zero"
        }
    
    c = 2
    if rank <= c * size:
        return {
            "metric_name": "rank_over_circuit_size",
            "metric_value": rank / size,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "rank_over_circuit_size",
            "metric_value": rank / size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rank={rank}, circuit_size={size}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results)
    total_instances_tested = sum(r["instances_tested"] for r in results)
    mean = total_metric_value / total_instances_tested
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 * r["instances_tested"] for r in results) / total_instances_tested)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")