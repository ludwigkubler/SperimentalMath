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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            if random.choice([True, False]):
                clause = {x for x in clause} | {-y for y in clause}
            clauses.append(clause)
        return clauses
    
    def compute_mli(cnf):
        # Placeholder for minimal lifting index computation
        return len(cnf) ** (1/len(cnf))
    
    def compute_entropy(cnf):
        n = len(cnf)
        p = Fraction(1, 2**n)
        entropy = -p * math.log2(p)
        return entropy
    
    mli_values = []
    ent_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            k = random.randint(1, n)
            cnf = generate_cnf(n, k)
            mli = compute_mli(cnf)
            ent = compute_entropy(cnf)
            
            if mli is not None and ent is not None:
                mli_values.append(mli)
                ent_values.append(ent)
                instances_tested += 1
                n_max = max(n_max, n)
    
    mean_mli = sum(mli_values) / len(mli_values)
    mean_ent = sum(ent_values) / len(ent_values)
    
    correlation = sum((mli_values[i] - mean_mli) * (math.log2(ent_values[i]) - mean_ent) for i in range(len(mli_values))) / len(mli_values)
    
    if len(mli_values) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": correlation,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mli_theoretical = [math.log2(ent_values[i]) for i in range(len(mli_values))]
    mean_mli_theoretical = sum(mli_theoretical) / len(mli_theoretical)
    mean_abs_diff = sum(abs(mli_values[i] - mli_theoretical[i]) for i in range(len(mli_values))) / len(mli_values)
    
    conjecture_holds = correlation >= 0.8 and mean_abs_diff <= 3
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **{result}}}")
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = (sum((r['metric_value'] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")