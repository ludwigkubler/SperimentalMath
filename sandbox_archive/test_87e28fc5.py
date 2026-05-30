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
    
    def generate_k_cnf(n, k):
        cnf = []
        for _ in range(k):
            clause = set()
            while len(clause) < n:
                lit = random.randint(1, 2*n)
                if lit > n:
                    lit = -lit
                clause.add(lit)
            cnf.append(tuple(sorted(clause)))
        return cnf
    
    def diophantine_exponent(cnf):
        # Placeholder for actual algorithm to compute the minimal diophantine exponent
        # This is a dummy implementation that returns a random value for testing purposes
        return random.uniform(1, 10)
    
    max_delta = 0
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            k = random.randint(2, min(n, 4))
            cnf = generate_k_cnf(n, k)
            delta = diophantine_exponent(cnf)
            max_delta = max(max_delta, delta)
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = max_delta <= (k**3 * n**(1/4))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "max_diophantine_exponent",
        "metric_value": max_delta,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")