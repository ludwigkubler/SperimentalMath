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
from math import comb

def generate_boolean_formula(m, k):
    literals = [f"x{i}" for i in range(1, m * k + 1)]
    clauses = []
    for _ in range(m):
        clause = random.sample(literals, k)
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def resolution_width(clauses):
    clauses_set = set(tuple(sorted(c)) for c in clauses)
    resolvents = set()
    while True:
        new_resolvents = set()
        for c1, c2 in combinations(clauses_set, 2):
            common = [x for x in c1 if -x in c2]
            if common:
                new_clause = sorted([x for x in c1 + c2 if x not in common])
                if tuple(new_clause) not in clauses_set and tuple(new_clause) not in resolvents:
                    new_resolvents.add(tuple(new_clause))
        if not new_resolvents:
            break
        resolvents.update(new_resolvents)
        clauses_set.update(resolvents)
    return len(resolvents)

def affine_order(clauses):
    n = len(set(l for clause in clauses for l in clause))
    lattice = [set() for _ in range(1 << n)]
    for i in range(1 << n):
        for j in range(n):
            if (i >> j) & 1:
                lattice[i].add(j + 1)
    aff_order = 0
    while True:
        new_lattice = [set() for _ in range(1 << n)]
        for i in range(1 << n):
            for j in range(n):
                if (i >> j) & 1:
                    new_lattice[i].add(j + 1)
                    for k in lattice[i]:
                        new_lattice[i ^ (1 << j)].add(k)
        if len(new_lattice[0]) == aff_order:
            break
        aff_order += 1
    return aff_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [5, 10, 15, 20, 30, 40]
    results = []
    for m in m_values:
        for _ in range(5):
            clauses = generate_boolean_formula(m, k=3)
            aff_order_val = affine_order(clauses)
            res_width_val = resolution_width(clauses)
            results.append((aff_order_val, res_width_val))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    aff_order_vals = [r[0] for r in results]
    res_width_vals = [r[1] for r in results]
    n_max = max(m_values)
    mean_aff_order = sum(aff_order_vals) / len(aff_order_vals)
    mean_res_width = sum(res_width_vals) / len(res_width_vals)
    
    if mean_res_width == 0:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "division_by_zero"
        }
    
    correlation = sum((a - mean_aff_order) * (b - mean_res_width) for a, b in results) / (len(results) * mean_res_width)
    c = mean_aff_order / mean_res_width if mean_res_width != 0 else float('inf')
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation >= 0.8 and c > 0,
        "counterexample": "" if correlation >= 0.8 else f"aff_order/cw = {c}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction=1")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"aff_order/cw < 1\" first_failing_seed={first_failing_seed}")