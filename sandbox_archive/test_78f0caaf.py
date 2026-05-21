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
    
    def generate_monotone_dnf(n):
        dnf = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([0, 1]) for _ in range(n)]
            if any(clause[i] == 1 for i in range(n)):
                dnf.append(clause)
        return dnf
    
    def characteristic_vectors(dnf):
        vectors = []
        for x in range(2**n):
            vector = [int(x & (1 << i)) for i in range(n)]
            if all(vector[i] == 0 or vector[i] == 1 for i in range(n)):
                vectors.append(vector)
        return vectors
    
    def convex_hull_volume(vectors):
        n = len(vectors[0])
        points = []
        for v in vectors:
            points.append(tuple(v))
        hull = ConvexHull(points)
        return hull.volume ** (1/n)
    
    def discrepancy(dnf, n):
        max_diff = 0
        for S in range(2**n):
            count = sum(all(dnf[j][i] == v[i] for i in range(n)) for j in range(len(dnf)))
            diff = abs(count / len(dnf) - 0.5)
            if diff > max_diff:
                max_diff = diff
        return max_diff
    
    n = random.randint(5, 40)
    dnf = generate_monotone_dnf(n)
    vectors = characteristic_vectors(dnf)
    V_F = convex_hull_volume(vectors)
    D_F = discrepancy(dnf, n)
    
    if V_F == 0:
        return {
            "metric_name": "discrepancy",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    c = 1 / (n * math.log(n))
    if D_F >= c * V_F:
        return {
            "metric_name": "discrepancy",
            "metric_value": D_F,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "discrepancy",
            "metric_value": D_F,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"V(F) = {V_F}, D(F) = {D_F}"
        }

if __name__ == "__main__":
    import sys
    import math
    from scipy.spatial import ConvexHull

    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(r)]}")