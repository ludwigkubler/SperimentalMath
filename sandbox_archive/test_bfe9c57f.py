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
    
    def characteristic_vector(dnf, n):
        vec = [0] * (2**n)
        for clause in dnf:
            index = 0
            for var in range(n):
                if var + 1 in clause:
                    index |= 1 << (n - var - 1)
                elif -(var + 1) in clause:
                    index &= ~(1 << (n - var - 1))
            vec[index] += 1
        return [v / len(dnf) for v in vec]
    
    def convex_hull_volume(vec):
        n = len(vec)
        points = [(i, vec[i]) for i in range(n)]
        hull = []
        for point in sorted(points):
            while len(hull) >= 2 and orientation(hull[-2], hull[-1], point) <= 0:
                hull.pop()
            hull.append(point)
        return area_of_polygon(hull)
    
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2
    
    def area_of_polygon(points):
        n = len(points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        return abs(area) / 2.0
    
    def discrepancy(vec):
        max_diff = 0
        for i in range(1, len(vec)):
            diff = abs(vec[i] - 0.5)
            if diff > max_diff:
                max_diff = diff
        return max_diff
    
    n = random.randint(5, 40)
    dnf = []
    for _ in range(random.randint(1, n)):
        clause = set()
        while len(clause) == 0 or len(clause) == n:
            clause = {random.randint(-n, -1), random.randint(1, n)}
        dnf.append(clause)
    
    vec = characteristic_vector(dnf, n)
    V_F = convex_hull_volume(vec)
    D_F = discrepancy(vec)
    
    c = 1 / math.log(n)
    if D_F < c * V_F / math.log(n):
        return {
            "metric_name": "discrepancy",
            "metric_value": D_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"n={n}, V(F)={V_F}, D(F)={D_F}"
        }
    else:
        return {
            "metric_name": "discrepancy",
            "metric_value": D_F,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"])
    
    mean = total_metric_value / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results if "metric_value" in r) / len(results))
    
    if support_fraction >= 0.8 * len(results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction/len(results)}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"discrepancy\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")