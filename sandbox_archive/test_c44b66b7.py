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
    
    def tropical_convex_hull(points):
        n = len(points[0])
        hull = []
        for point in points:
            if all(point[i] >= q[i] for q in hull):
                hull.append(point)
        return hull
    
    def count_extreme_points(hull):
        return len(hull)
    
    def generate_3cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            clause.append(random.choice([1, -1]))
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses, n):
        poly = [0] * (2 ** n)
        for clause in clauses:
            monomial = 1
            for var in clause[:-1]:
                if clause[-1] == 1:
                    monomial *= max(0, var)
                else:
                    monomial *= -max(0, var)
            poly[sum([1 << (var - 1) for var in clause[:-1]])] += monomial
        return poly
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_3cnf(n, m)
    poly = clause_indicator_polynomial(clauses, n)
    
    hull = tropical_convex_hull(poly)
    extreme_points_count = count_extreme_points(hull)
    
    conjecture_holds = extreme_points_count >= math.log2(n)
    counterexample = "" if conjecture_holds else f"n={n}, extreme_points_count={extreme_points_count}"
    
    return {
        "metric_name": "Extreme Points Count",
        "metric_value": extreme_points_count,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={seeds[0]}, extreme_points_count={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")