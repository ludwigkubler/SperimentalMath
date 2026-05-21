# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n: int):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses: list, assignment: dict = {}):
        if not clauses:
            return True
        clause = next((c for c in clauses if any(l in assignment and assignment[l] == v for l, v in zip(c, [1, -1]))), None)
        if not clause:
            return False
        literal = random.choice(clause)
        var = abs(literal)
        assignment[var] = 1 if literal > 0 else -1
        if dpll([c for c in clauses if all(l not in c or assignment[l] == v for l, v in zip(c, [1, -1]))], assignment):
            return True
        del assignment[var]
        assignment[var] = -1 if literal > 0 else 1
        if dpll([c for c in clauses if all(l not in c or assignment[l] == v for l, v in zip(c, [1, -1]))], assignment):
            return True
        del assignment[var]
        return False
    
    def resolution_width(clauses: list):
        width = 0
        while True:
            new_clauses = []
            found_resolvent = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(abs(l) == abs(m) and l != m for l in clauses[i] for m in clauses[j]):
                        resolvent = [l for l in clauses[i] if l not in clauses[j]] + [m for m in clauses[j] if m not in clauses[i]]
                        new_clauses.append(resolvent)
                        found_resolvent = True
            if not found_resolvent:
                break
            width += 1
            clauses.extend(new_clauses)
        return width
    
    def toric_polytope_facets(clauses: list):
        monomials = set()
        for clause in clauses:
            for l in clause:
                monomials.add(tuple(sorted([abs(l)])))
        facets = len(monomials)
        return facets
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_3cnf(n)
            facets = toric_polytope_facets(clauses)
            width = resolution_width(clauses)
            if width == 0:
                continue
            results.append((facets, n, width))
    
    if not results:
        return {
            "metric_name": "facet_count_resolution_width",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    mean_facets = sum(f for f, _, _ in results) / len(results)
    mean_width = sum(w for _, _, w in results) / len(results)
    ratio_mean = mean_facets / (mean_width * math.log(len(n_values)))
    
    return {
        "metric_name": "facet_count_resolution_width",
        "metric_value": ratio_mean,
        "instances_tested": len(results),
        "conjecture_holds": abs(ratio_mean - 1) < 0.2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    if all(r["metric_value"] is None for r in results):
        print("RESULT: INCONCLUSIVE reason=no_valid_instances")
    elif support_fraction / len(results) >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=NA support_fraction={support_fraction / len(results):.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed + 1}")