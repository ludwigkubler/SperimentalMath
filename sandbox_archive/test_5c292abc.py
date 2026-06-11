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
    
    def generate_cnf(m, n):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(c) for c in cnf)
        new_clauses = set()
        while True:
            added = False
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1).intersection(set(clause2))) == 1:
                        lit = list(set(clause1) - set(clause2))[0]
                        new_clause = tuple(sorted([x for x in clause1 + clause2 if x != lit and -x not in clause1 + clause2]))
                        if new_clause not in clauses and new_clause not in new_clauses:
                            new_clauses.add(new_clause)
                            added = True
            if not added:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def geometric_group_order(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        assignments = [tuple(sorted([1 if i+1 in assignment else -1 for i in range(n)])) for assignment in itertools.product([True, False], repeat=n)]
        group_elements = set()
        for assignment in assignments:
            for perm in itertools.permutations(assignment):
                group_elements.add(tuple(perm))
        return len(group_elements)
    
    m_values = [5, 10, 15, 20, 30, 40]
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for m in m_values:
        for n in n_values:
            cnf = generate_cnf(m, n)
            proof_depth = resolution(cnf)
            group_order = geometric_group_order(cnf)
            results.append((m, n, proof_depth, group_order))
    
    if not results:
        return {
            "metric_name": "resolution_proof_depth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_depth = sum(result[2] for result in results) / len(results)
    std_depth = math.sqrt(sum((result[2] - mean_depth) ** 2 for result in results) / len(results))
    upper_bound = max(m * n * n * math.log(n) for m, n, _, _ in results)
    
    support_fraction = sum(1 for _, _, depth, _ in results if abs(depth - upper_bound) <= 0.3 * upper_bound) / len(results)
    
    return {
        "metric_name": "resolution_proof_depth",
        "metric_value": mean_depth,
        "instances_tested": len(results),
        "n_max": max(n for _, n, _, _ in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_depth={mean_depth}, upper_bound={upper_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_depth={r['metric_value']}, upper_bound={upper_bound}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")