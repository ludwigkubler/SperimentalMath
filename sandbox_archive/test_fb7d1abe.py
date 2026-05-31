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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clause = random.sample(literals, n // 2)
            clauses.append(clause)
        return clauses

    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literals = [l for l in set(lit for clause in cnf for lit in clause) if (not any(l in clause for clause in cnf)) or (not any(-l in clause for clause in cnf))]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(list(set(lit for clause in cnf for lit in clause)))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return False

    def mter(cnf):
        n = len(cnf)
        rank = [0] * (n + 1)
        for clause in cnf:
            for lit in clause:
                rank[abs(lit)] += 1
        return max(rank)

    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = generate_cnf(n)
        mter_value = mter(cnf)
        path_length = dpll(cnf)
        results.append((mter_value, path_length))

    mean_mter = sum(m for m, _ in results) / len(results)
    mean_path_length = sum(p for _, p in results) / len(results)
    correlation_coefficient = (sum((m - mean_mter) * (p - mean_path_length) for m, p in results) /
                               math.sqrt(sum((m - mean_mter) ** 2 for m, _ in results) *
                                         sum((p - mean_path_length) ** 2 for _, p in results)))

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "correlation_coefficient_not_sufficiently_high"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")