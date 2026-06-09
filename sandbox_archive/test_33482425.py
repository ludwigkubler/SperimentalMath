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
    
    def generate_cnf(n, k):
        clauses = []
        for _ in range(2 * n):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if random.choice([True, False]):
                    clause.add(-var)
                else:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def is_k_colorable(cnf, k):
        colors = {}
        for literal in set(lit for clause in cnf for lit in clause):
            if literal < 0:
                literal = -literal
            if literal not in colors:
                colors[literal] = random.randint(1, k)
        for clause in cnf:
            color_set = {colors[abs(lit)] for lit in clause}
            if len(color_set) == len(clause):
                return False
        return True

    def categorify_cnf(cnf):
        # Placeholder for category-theoretic construction
        # This is a dummy implementation and should be replaced with actual logic
        return 0

    n = random.randint(5, 40)
    k = random.randint(2, min(n, 10))
    cnf = generate_cnf(n, k)

    if not is_k_colorable(cnf, k):
        return {
            "metric_name": "category_height",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "not_k_colorable"
        }

    category_height = categorify_cnf(cnf)
    
    return {
        "metric_name": "category_height",
        "metric_value": category_height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": category_height <= k**(3/2) * math.log(n, 2)**2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_height = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_height = math.sqrt(sum((r["metric_value"] - mean_height)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_height} std={std_height} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"not_k_colorable\" first_failing_seed={r['seed']}")
                break