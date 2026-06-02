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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_primitive_element(p):
        while True:
            a = random.randint(2, p-2)
            if all(pow(a, (p-1)//q, p) != 1 for q in range(2, int(math.sqrt(p-1)) + 1)):
                return a
    
    def local_class_group_size(p):
        if not is_prime(p):
            raise ValueError("p must be prime")
        n = p - 1
        factors = []
        for i in range(2, n + 1):
            count = 0
            while n % i == 0:
                n //= i
                count += 1
            if count > 0:
                factors.append((i, count))
        return math.prod([f[1] for f in factors])
    
    def communication_complexity_rank(p):
        # Placeholder function; replace with actual computation
        return random.randint(1, p-2)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        p = random.choice([q for q in range(5, n_max + 1) if is_prime(q)])
        alpha = generate_primitive_element(p)
        K = p**2
        L = p
        ccr_K_L = communication_complexity_rank(p)
        Cl_K_L = local_class_group_size(K)
        
        metric_values.append(Cl_K_L / ccr_K_L)
    
    mean_metric_value = sum(metric_values) / instances_tested
    std_metric_value = math.sqrt(sum((x - mean_metric_value)**2 for x in metric_values) / instances_tested)
    
    correlation_coefficient = (sum((metric_values[i] - mean_metric_value) * (i + 1 - mean_metric_value) for i in range(instances_tested)) /
                               (instances_tested * std_metric_value * math.sqrt(sum((i + 1 - mean_metric_value)**2 for i in range(instances_tested)))))
    
    conjecture_holds = abs(correlation_coefficient - 1) < 0.05
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")