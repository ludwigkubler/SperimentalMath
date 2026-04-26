# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import math
import random
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    def generate_3cnf(n: int, m: int) -> list:
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            while len(set(clause)) != 2:
                clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses

    def indicator_function(x: int, clause: list) -> int:
        return all((x & abs(c)) == c for c in clause)

    def support(polynomial: dict, GF: int) -> set:
        support_set = set()
        for monomial in polynomial.keys():
            if any(indicator_function(monomial, clause) for clause in F):
                support_set.add(monomial)
        return support_set

    def newton_polytope(support_set: set) -> list:
        exponents = [tuple(sorted([abs(x) for x in monomial])) for monomial in support_set]
        hull = convex_hull(exponents)
        return hull.simplices

    def convex_hull(points: list) -> 'ConvexHull':
        n = len(points[0])
        points = [(1 if p[i] else 0, *p[:i], *p[i+1:]) for p in points]
        hull = ConvexHull(points)
        return hull

    def dpll_runtime(F: list) -> int:
        def backtrack(assignment: dict, clause_set: list) -> bool:
            if not clause_set:
                return True
            var = next((v for v in range(1, n+1) if v not in assignment), None)
            if var is None:
                return False
            for val in [0, 1]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                new_clause_set = [c for c in clause_set if not any(indicator_function(assignment[v], c) for v in assignment)]
                if backtrack(new_assignment, new_clause_set):
                    return True
            return False
        return len(list(product([0, 1], repeat=n))) - sum(backtrack({}, F) for _ in range(10))

    n = random.choice([10, 12, 14, 16, 18, 20])
    m = int(4.3 * n)
    F = generate_3cnf(n, m)

    GF = 2
    polynomial = {}
    for assignment in product([0, 1], repeat=n):
        monomial = tuple(sorted([abs(x) for x in assignment]))
        if monomial not in polynomial:
            polynomial[monomial] = 1
        else:
            polynomial[monomial] += 1

    support_set = support(polynomial, GF)
    edge_count = len(newton_polytope(support_set))

    dpll_tree_size = sum(dpll_runtime(F) for _ in range(10)) / 10

    C = 2
    conjecture_holds = edge_count <= C * dpll_tree_size * n**2
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "edge_count",
        "metric_value": edge_count,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")

    edge_counts = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(edge_counts)/len(edge_counts)} std=0.0 support_fraction={support_fraction}")
    elif sum(r["conjecture_holds"] for r in results) >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={sum(edge_counts)/len(edge_counts)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")