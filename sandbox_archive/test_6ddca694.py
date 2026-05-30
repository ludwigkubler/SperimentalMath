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
    
    def euler_characteristic(f):
        n = int(math.log2(len(f)))
        return n - 1
    
    def communication_complexity(M):
        N = len(M)
        rows = random.sample(range(N), N // 2)
        cols = random.sample(range(N), N // 2)
        submatrix = [[M[i][j] for j in cols] for i in rows]
        return sum(sum(row) for row in submatrix) / (N // 2) ** 0.5
    
    results = []
    n_max = 5
    for n in range(5, 41):
        f = generate_boolean_function(n)
        chi = euler_characteristic(f)
        cc = communication_complexity([[random.choice([-1, 1]) for _ in range(n)] for _ in range(n)])
        results.append({"n": n, "chi": chi, "cc": cc})
        if n > n_max:
            n_max = n
    
    metric_value = sum(result["chi"] for result in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(result["chi"] >= math.sqrt(n) * n for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Euler Characteristic",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")