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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(abs(c) == abs(clause[i]) for i in range(len(clause))):
                continue
            clauses.append(clause)
        return clauses

    def tropical_polynomial(clauses):
        n = len(clauses[0])
        poly = [0] * (2**n)
        for clause in clauses:
            index = sum(1 << (abs(x) - 1) if x > 0 else -(1 << (abs(x) - 1)) for x in clause)
            poly[index] += max(clause, key=abs)
        return poly

    def convex_hull(poly):
        n = len(poly)
        points = [(i, poly[i]) for i in range(n)]
        points.sort(key=lambda p: (p[0], -p[1]))
        
        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0
            elif val > 0:
                return 1
            else:
                return 2
        
        def convex_hull(points):
            n = len(points)
            if n < 3:
                return points
            
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
        
        hull = convex_hull(points)
        return len(hull)

    def acc0_circuit_size(n):
        # Placeholder for ACC^0 circuit size calculation
        # This is a dummy implementation and should be replaced with actual logic
        return n

    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    poly = tropical_polynomial(clauses)
    facet_count = convex_hull(poly)
    acc0_size = acc0_circuit_size(n)

    metric_name = "facet_count_vs_acc0_size"
    metric_value = facet_count / (acc0_size + 1)  # Avoid division by zero
    instances_tested = 1
    conjecture_holds = abs(math.log2(n) - facet_count) < 1e-6 and acc0_size <= n**2
    counterexample = "" if conjecture_holds else f"n={n}, facet_count={facet_count}, acc0_size={acc0_size}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"facet_count_vs_acc0_size\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")