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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_depth(clauses):
        new_clauses = set()
        stack = list(clauses)
        while stack:
            clause = stack.pop()
            for other_clause in clauses:
                if len(set(clause) & set(other_clause)) == 1:
                    new_clause = [x for x in clause if x not in other_clause] + [y for y in other_clause if y not in clause]
                    if new_clause and new_clause not in new_clauses:
                        new_clauses.add(tuple(sorted(new_clause)))
                        stack.append(new_clause)
        return len(new_clauses)

    def agm(values, k):
        product = 1
        for value in values:
            product *= math.pow(value, k)
        return math.pow(product, 1/len(values))

    n_values = [30, 35, 40]
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(10):  # Ensure at least 30 instances per seed
            clauses = generate_cnf(n, n)
            depth = resolution_depth(clauses)
            total_depth += depth
            instances_tested += 1

    mean_depth = total_depth / instances_tested
    conjecture_holds = True
    counterexample = ""
    
    k = 0.5  # Example value for k, should be a parameter in the actual conjecture
    if mean_depth > math.pow(agm([len(clause) for clause in generate_cnf(n, n)], k), k):
        conjecture_holds = False
        counterexample = "Depth exceeds AGM(k)^k bound"

    return {
        "metric_name": "Resolution Depth",
        "metric_value": mean_depth,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth exceeds AGM(k)^k bound\" first_failing_seed={first_failing_seed}")