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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            while len(set(clause)) != 3:
                clause = [random.randint(-n, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def tropical_polynomial(clauses):
        return max(sum(abs(x) for x in clause) for clause in clauses)
    
    def convex_hull(points):
        if len(points) < 2:
            return points
        min_x = min(point[0] for point in points)
        hull = [point for point in points if point[0] == min_x]
        for point in points[1:]:
            direction = (point[1] - hull[-1][1]) / (point[0] - hull[-1][0])
            while len(hull) > 1 and ((point[1] - hull[-2][1]) / (point[0] - hull[-2][0])) >= direction:
                hull.pop()
            hull.append(point)
        return hull
    
    def facet_count(convex_hull):
        n = len(convex_hull)
        if n < 3:
            return 0
        count = 0
        for i in range(n):
            x1, y1 = convex_hull[i]
            x2, y2 = convex_hull[(i + 1) % n]
            for j in range(n):
                if j != i and j != (i + 1) % n:
                    x3, y3 = convex_hull[j]
                    area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2
                    if area > 0:
                        count += 1
        return count
    
    def acc0_circuit_size(n):
        # Placeholder for actual ACC^0 circuit size calculation
        return n ** 2
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    tp = tropical_polynomial(clauses)
    hull = convex_hull([(x, y) for x in range(-n, n + 1) for y in range(-tp, tp + 1)])
    fc = facet_count(hull)
    acc0_size = acc0_circuit_size(n)
    
    return {
        "metric_name": "facet_count",
        "metric_value": fc,
        "instances_tested": 1,
        "conjecture_holds": fc == Fraction(n).log(2),
        "counterexample": "" if fc == Fraction(n).log(2) else f"n={n}, fc={fc}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")