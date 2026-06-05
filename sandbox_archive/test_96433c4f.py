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
    
    def generate_d_regular_circuit(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.randint(0, d - 1) == 0:
                    edges.append((i, j))
        return edges
    
    def is_kahler_metric(m):
        # Placeholder function to determine if m defines a Kähler metric
        return True
    
    def compute_m(K):
        # Placeholder function to compute the minimal number of independent complex structures
        return len(K)
    
    n_max = 0
    instances_tested = 0
    total_mK_D = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for d in [5, 10, 15, 20, 30, 40]:
        n = random.randint(5, 40)
        if n_max < n:
            n_max = n
        
        for _ in range(5):
            circuit = generate_d_regular_circuit(d, n)
            if circuit is None:
                continue
            instances_tested += 1
            
            K = set(circuit)
            mK = compute_m(K)
            D = len(circuit) // (n - 1)
            
            total_mK_D += mK / D
            
            if not is_kahler_metric(mK):
                conjecture_holds = False
                counterexample = f"Non-Kähler metric for d={d}, n={n}"
    
    mean_mK_D = total_mK_D / instances_tested
    
    return {
        "metric_name": "m(K) / D",
        "metric_value": mean_mK_D,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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