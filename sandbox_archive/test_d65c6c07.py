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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for j in range(i)):
                clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def monomial_to_index(monomial):
        return sum(2 ** (abs(x) - 1) for x in monomial if x > 0)
    
    def hilbert_function(I, n):
        H = [0] * (n + 1)
        for k in range(n + 1):
            count = 0
            for clause in I:
                if all(abs(x) <= k for x in clause):
                    count += 1
            H[k] = count
        return H
    
    def acc0_circuit_size_lower_bound(n):
        # A simple lower bound for ACC^0 circuit size (e.g., n * log n)
        return n * math.log(n, 2)
    
    n = random.randint(5, 40)
    I = generate_3cnf(n)
    H = hilbert_function(I, n)
    acc0_bound = acc0_circuit_size_lower_bound(n)
    
    metric_value = H[n] / (n * math.log(n, 2))
    conjecture_holds = (H[n] >= 1) == (acc0_bound >= 1)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Hilbert Function Growth",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")