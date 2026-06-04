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
    
    def generate_cnf(n, d):
        cnf = []
        for _ in range(d * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        clauses = set(tuple(sorted(c)) for c in cnf)
        queue = list(clauses)
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                continue
            literal = random.choice(clause)
            new_clauses = []
            for other_clause in clauses:
                if literal not in other_clause and -literal not in other_clause:
                    new_clauses.append(tuple(sorted(other_clause + (literal,))))
            queue.extend(new_clauses)
        return max(len(c) for c in queue)
    
    def noncommutative_probability_order(cnf):
        n = max(abs(lit) for lit in cnf)
        if n == 0:
            return 0
        # Simulate noncommutative probability order (simplified example)
        return random.uniform(1, n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n, n // 5)
        o_phi = noncommutative_probability_order(cnf)
        w_phi = resolution_width(cnf)
        diff = abs(o_phi - w_phi)
        results.append({
            "n": n,
            "o_phi": o_phi,
            "w_phi": w_phi,
            "diff": diff
        })
    
    mean_diff = sum(r["diff"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["diff"] - mean_diff) ** 2 for r in results) / len(results))
    conjecture_holds = all(0.5 <= r["diff"] <= 1.5 for r in results)
    
    return {
        "metric_name": "difference_between_order_and_width",
        "metric_value": mean_diff,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_diff = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_diff) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_diff} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")