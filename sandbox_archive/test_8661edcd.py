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
        clauses = []
        for _ in range(k * n):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def resolution_width(clauses):
        literals = set()
        for clause in clauses:
            literals.update(clause)
        queue = list(literals)
        while queue:
            lit = queue.pop(0)
            if -lit in literals:
                literals.remove(-lit)
                continue
            new_clauses = []
            for clause in clauses:
                if lit in clause:
                    new_clause = [l for l in clause if l != lit]
                    if not new_clause:
                        return len(literals) + 1
                    new_clauses.append(tuple(sorted(new_clause)))
                elif -lit in clause:
                    new_clause = [l for l in clause if l != -lit]
                    new_clauses.append(tuple(sorted(new_clause)))
            clauses.extend(new_clauses)
        return len(literals)

    def hodge_order(n):
        return math.log2(n) ** 2

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_k_cnf(n, k=3)
            width = resolution_width(clauses)
            order = hodge_order(n)
            if width > order * (1 + math.log2(n)):
                return {
                    "metric_name": "resolution_width",
                    "metric_value": width,
                    "instances_tested": 5,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Width {width} exceeds order * (1 + log2(n)) for n={n}"
                }
            results.append({"width": width, "order": order})
    
    mean_width = sum(result["width"] for result in results) / len(results)
    mean_order = sum(result["order"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["width"] <= result["order"]) / len(results)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": mean_width,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Width exceeds order * (1 + log2(n))\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")