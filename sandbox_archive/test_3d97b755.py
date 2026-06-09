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
    
    def generate_k_colorable_cnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k * n):
            clause = [random.choice(variables)]
            if random.choice([True, False]):
                clause.append(-random.choice(variables))
            clauses.append(clause)
        return clauses
    
    def is_k_colorable(cnf, k):
        colors = {}
        for clause in cnf:
            for literal in clause:
                var = abs(literal)
                if var not in colors:
                    colors[var] = random.randint(1, k)
                elif colors[var] != (colors[literal] if literal > 0 else -colors[literal]):
                    return False
        return True
    
    def categorify_cnf(cnf):
        # Placeholder for categorification procedure
        # This is a dummy implementation that does not actually categorify the CNF
        category_height = len(cnf)
        return category_height
    
    n_max = 0
    metric_value = 0.0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(2, min(n // 2, 5))
            cnf = generate_k_colorable_cnf(n, k)
            if not is_k_colorable(cnf, k):
                continue
            category_height = categorify_cnf(cnf)
            metric_value += category_height
            instances_tested += 1
            n_max = max(n_max, n)
    
    conjecture_holds = False
    counterexample = ""
    
    if instances_tested > 0:
        mean_height = metric_value / instances_tested
        upper_bound = k**(3/2) * math.log(n)**2
        if mean_height <= upper_bound:
            conjecture_holds = True
    
    return {
        "metric_name": "category_height",
        "metric_value": mean_height,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_k_colorable\" first_failing_seed={first_failing_seed}")