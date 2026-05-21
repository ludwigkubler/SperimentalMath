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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(x == -y for x, y in zip(clause, clause[1:])):
                clauses.append(clause)
        return clauses
    
    def tropical_polynomial(clauses):
        tp = max(abs(sum(c)) for c in clauses)
        return tp
    
    def convex_hull(points):
        if len(points) < 3:
            return points
        hull = sorted(points, key=lambda p: (p[0], p[1]))
        lower = []
        for point in hull:
            while len(lower) >= 2 and orientation(lower[-2], lower[-1], point) <= 0:
                lower.pop()
            lower.append(point)
        upper = []
        for point in reversed(hull):
            while len(upper) >= 2 and orientation(upper[-2], upper[-1], point) <= 0:
                upper.pop()
            upper.append(point)
        return lower[:-1] + upper[:-1]
    
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
    
    def facet_count(hull):
        return len(hull)
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    tp = tropical_polynomial(clauses)
    hull = convex_hull([(x, y) for x in range(-n, n + 1) for y in range(-tp, tp + 1)])
    
    if len(hull) == 0:
        return {
            "metric_name": "facet_count",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Empty hull"
        }
    
    facet_count = len(hull)
    expected_facet_count = math.log(n, 2)
    
    return {
        "metric_name": "facet_count",
        "metric_value": facet_count,
        "instances_tested": 1,
        "conjecture_holds": abs(facet_count - expected_facet_count) <= 0.5 * expected_facet_count,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    total_metric_value = 0
    count_supporting_conjecture = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            count_supporting_conjecture += 1
        
        results.append(trial_result)
    
    mean_metric_value = total_metric_value / len(results)
    support_fraction = count_supporting_conjecture / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='facet_count does not match expected' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")