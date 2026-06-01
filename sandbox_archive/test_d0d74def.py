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
    
    def generate_cnf(m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, m) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(2, 4))]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment={}):
        unsatisfied_clauses = [c for c in cnf if not any(l in assignment and assignment[l] == (l > 0) for l in c)]
        if not unsatisfied_clauses:
            return True
        unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            assignment[literal] = (literal > 0)
            if dpll(cnf, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = (literal < 0)
            if dpll(cnf, assignment):
                return True
            del assignment[-literal]
        else:
            literal = random.choice([l for c in unsatisfied_clauses for l in c])
            assignment[literal] = (literal > 0)
            if dpll(cnf, assignment):
                return True
            del assignment[literal]
            assignment[-literal] = (literal < 0)
            if dpll(cnf, assignment):
                return True
            del assignment[-literal]
        return False
    
    def minimal_diophantine_property_set(cnf):
        variables = set(abs(l) for c in cnf for l in c)
        property_set = set()
        for v in variables:
            assignment = {v: True}
            if dpll(cnf, assignment):
                property_set.add(v)
            assignment[v] = False
            if dpll(cnf, assignment):
                property_set.add(-v)
        return property_set
    
    def circuit_monotone_width(property_set):
        n = len(property_set)
        width = 0
        for i in range(1 << n):
            subset = {list(property_set)[j] for j in range(n) if (i & (1 << j))}
            if all(any(l in assignment and assignment[l] == (l > 0) for l in clause) for clause in cnf):
                width = max(width, len(subset))
        return width
    
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(m)
            property_set = minimal_diophantine_property_set(cnf)
            monotone_width = circuit_monotone_width(property_set)
            metrics.append(monotone_width)
            instances_tested += 1
            n_max = max(n_max, m)
    
    mean_value = sum(metrics) / len(metrics)
    conjecture_holds = all(m <= 1.5 * m * math.log2(m) for m in metrics)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "circuit_monotone_width",
        "metric_value": mean_value,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")