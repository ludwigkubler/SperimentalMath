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
    
    def agm(a, b):
        if a == 0 or b == 0:
            return 0
        a, b = abs(a), abs(b)
        while abs(a - b) > 1e-9:
            if a > b:
                a = (a + b) / 2
            else:
                b = (a + b) / 2
        return a
    
    def generate_clauses(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def resolution_depth(clauses):
        depth = 0
        while True:
            new_clauses = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if abs(clauses[i][0]) == abs(clauses[j][1]):
                        new_clause = [clauses[i][1], clauses[j][0]]
                        if new_clause not in new_clauses:
                            new_clauses.add(new_clause)
            if not new_clauses:
                break
            clauses.extend(new_clauses)
            depth += 1
        return depth
    
    n_values = [30, 35, 40]
    k = 0.75
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(30):
            clauses = generate_clauses(n, random.randint(1, n))
            agm_value = math.prod(agm(abs(clause[0]), abs(clause[1])) ** k for clause in clauses)
            depth = resolution_depth(clauses)
            total_depth += depth
            instances_tested += 1
    
    avg_depth = total_depth / instances_tested
    conjecture_holds = avg_depth <= agm_value * 2 and avg_depth >= agm_value / 2
    counterexample = "" if conjecture_holds else "resolution_depth_exceeds_bound"
    
    return {
        "metric_name": "average_resolution_depth",
        "metric_value": avg_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    avg_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and "resolution_depth_exceeds_bound" in r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"resolution_depth_exceeds_bound\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")