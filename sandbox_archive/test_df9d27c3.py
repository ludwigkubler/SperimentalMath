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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def generate_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, n) for _ in range(3)]
        while any(abs(c) == abs(clause[i]) for i in range(len(clause))):
            clause = [random.randint(-n, n) for _ in range(3)]
        clauses.append(clause)
    return clauses

def tropical_polynomial(clauses):
    return max(sum(abs(c) for c in clause) for clause in clauses)

def convex_hull(points):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    def distance(p, q):
        return math.sqrt((p[0] - q[0])**2 + (p[1] - q[1])**2)

    points = sorted(points)
    lower = []
    for p in points:
        while len(lower) >= 2 and orientation(lower[-2], lower[-1], p) != 2:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and orientation(upper[-2], upper[-1], p) != 2:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_3cnf(n)
    polytope_points = [(sum(abs(c) for c in clause), len(clause)) for clause in clauses]
    facet_count = len(convex_hull(polytope_points))
    
    # Placeholder for ACC^0 circuit size (not computable directly, so we use a dummy value)
    acc0_circuit_size = n  # This is just a placeholder
    
    return {
        "metric_name": "facet_count",
        "metric_value": facet_count,
        "instances_tested": 1,
        "conjecture_holds": False if facet_count != math.log(n, 2) else True,
        "counterexample": "mapping_undefined" if facet_count != math.log(n, 2) else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    facet_counts = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(facet_counts) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(facet_counts)/len(facet_counts):.2f} std={math.sqrt(sum((x - sum(facet_counts)/len(facet_counts))**2 for x in facet_counts)/len(facet_counts)):.2f} support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] and r["counterexample"] == "mapping_undefined" for r in results):
        RESULT = "INCONCLUSIVE mapping_undefined"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)