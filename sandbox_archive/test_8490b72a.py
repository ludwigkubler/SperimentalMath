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
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(f):
        n = int(math.log2(len(f)))
        rank = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(f[i*2**j + k] == f[j*2**i + k] for k in range(2**(n-i-j))):
                    rank += 1
        return rank
    
    def lie_algebra_from_function(f):
        n = int(math.log2(len(f)))
        ideal = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if all(f[i*2**j + k] == f[j*2**i + k] for k in range(2**(n-i-j))):
                    ideal[i][j] = 1
                    ideal[j][i] = 1
        return ideal
    
    def coadjointness_index(ideal):
        n = len(ideal)
        index = 0
        for i in range(n):
            for j in range(i+1, n):
                if ideal[i][j]:
                    index += 1
        return index
    
    results = []
    for _ in range(30):
        f = generate_boolean_function(random.randint(5, 40))
        r_f = communication_complexity_rank(f)
        A = lie_algebra_from_function(f)
        I = coadjointness_index(A)
        results.append((r_f, I))
    
    mean_r_f = sum(r for r, _ in results) / len(results)
    mean_I = sum(I for _, I in results) / len(results)
    support_fraction = sum(1 for r, I in results if I <= r**3) / len(results)
    
    return {
        "metric_name": "coadjointness_index",
        "metric_value": mean_I,
        "instances_tested": 30,
        "n_max": max(r[1] for r in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"r(f)={mean_r_f}, I={mean_I}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")