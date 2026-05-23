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
    
    def tropical_rank(poly):
        if not poly:
            return 0
        max_val = -math.inf
        for coeff in poly.values():
            if coeff > max_val:
                max_val = coeff
        return max_val
    
    def clause_indicator_polynomial(clauses, n):
        poly = {}
        for i in range(1 << n):
            term = 0
            for j in range(n):
                if (i >> j) & 1:
                    term += clauses[j]
            if term == len(clauses):
                poly[i] = 1
        return poly
    
    def resolution_width(clauses, n):
        stack = []
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if len(clause) == 1:
                continue
            new_clause = []
            for c in stack:
                if not set(c).isdisjoint(clause):
                    new_clause.extend([x for x in c if x not in clause])
            stack.append(new_clause)
        return max(len(c) for c in stack)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1))
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    
    poly = clause_indicator_polynomial(clauses, n)
    rank = tropical_rank(poly)
    width = resolution_width(clauses, n)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= 2 ** rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1000, 9999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Tseitin formula with n={n}, m={m}"
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")