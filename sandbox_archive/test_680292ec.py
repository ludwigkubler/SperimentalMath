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
    
    def generate_phi(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank(phi):
        n = len(phi)
        rank = 0
        for i in range(n):
            if phi[i] == 1:
                rank += 1
        return rank
    
    def generalized_exponential_sum(phi, k):
        n = len(phi)
        sum_val = 0
        for i in range(2**n):
            term = 1
            for j in range(n):
                if phi[j] == 1:
                    term *= (i >> j) % k + 1
                else:
                    term *= (i >> j) % k
            sum_val += term % k
        return sum_val
    
    def min_order(phi, k):
        n = len(phi)
        for i in range(1, k+1):
            if generalized_exponential_sum(phi, i) == 0:
                return i
        return k
    
    def compute_metric(n):
        phi = generate_phi(n)
        r_f = communication_complexity_rank(phi)
        k_f = min_order(phi, 2**n)
        return {"metric_name": "min_order", "metric_value": k_f, "instances_tested": 1, "n_max": n, "conjecture_holds": False, "counterexample": ""}
    
    metric_values = []
    for n in [5, 10, 15, 20, 30, 40]:
        result = compute_metric(n)
        metric_values.append(result["metric_value"])
    
    mean_value = sum(metric_values) / len(metric_values)
    support_fraction = sum(1 for val in metric_values if val <= (math.sqrt(r_f))**3) / len(metric_values)
    
    return {"seed": seed, "mean_metric_value": mean_value, "support_fraction": support_fraction}

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["mean_metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["support_fraction"] >= 0.8) / len(results)
    
    if all(res["support_fraction"] >= 0.8 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")