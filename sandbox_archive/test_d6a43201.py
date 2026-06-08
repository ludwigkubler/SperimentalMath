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
    
    def generate_quandle(n):
        quandle = []
        for i in range(n):
            row = [random.randint(0, n-1) for _ in range(n)]
            quandle.append(row)
        return quandle
    
    def calculate_mci(quandle):
        n = len(quandle)
        mci = 0
        for i in range(n):
            for j in range(i+1, n):
                if all(quandle[i][k] == quandle[j][k] for k in range(n)):
                    mci += 1
        return mci
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(0, n-1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def max_clauses_satisfiable(clauses):
        n = len(clauses)
        max_sat = 0
        for i in range(1 << n):
            satisfied = True
            for clause in clauses:
                if all((i >> j) & 1 == (x < 0 and -x or x) % n in clause for x in clause):
                    continue
                satisfied = False
                break
            if satisfied:
                max_sat += 1
        return max_sat
    
    def exponential_bound(max_sat):
        return 2 ** max_sat
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        quandle = generate_quandle(n)
        clauses = generate_sat_instance(n)
        mci = calculate_mci(quandle)
        max_sat = max_clauses_satisfiable(clauses)
        bound = exponential_bound(max_sat)
        
        metric_values.append(mci <= bound)
    
    mean_metric_value = sum(metric_values) / instances_tested
    conjecture_holds = all(metric_values)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "mci <= 2^(max_clauses_satisfiable)",
        "metric_value": mean_metric_value,
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
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")